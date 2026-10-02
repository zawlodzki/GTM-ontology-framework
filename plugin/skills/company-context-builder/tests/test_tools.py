from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import warnings
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PYTHON = sys.executable
LINTER = REPO / "tools" / "lint_ontology.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class ClosedWonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.script = ROOT / "scripts" / "analyze_closed_won.py"
        self.fixture = ROOT / "tests" / "fixtures" / "closed_won.csv"

    def test_filters_cohort_converts_currencies_and_ranks_top(self) -> None:
        result = subprocess.run(
            [
                PYTHON, str(self.script), str(self.fixture), "--timezone", "Europe/Warsaw",
                "--analysis-at", "2026-07-15T12:00:00+02:00",
                "--approved-conversion-method", "CRM base values approved 2026-07-15",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["cohort"]["records"], 3)
        self.assertEqual(report["base_currency"], "EUR")
        self.assertEqual(report["approved_conversion_method"], "CRM base values approved 2026-07-15")
        self.assertEqual(report["base_value_sources"], {"crm-approved": 3})
        self.assertEqual(report["top_opportunities"][0]["opportunity_id"], "D-002")
        self.assertNotIn("D-004", [item["opportunity_id"] for item in report["top_opportunities"]])
        self.assertNotIn("manual failures", result.stdout)

    def test_rejects_multicurrency_without_complete_base_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            broken = Path(directory) / "broken.csv"
            text = self.fixture.read_text(encoding="utf-8").replace("135000,EUR", ",EUR", 1)
            broken.write_text(text, encoding="utf-8")
            result = subprocess.run(
                [PYTHON, str(self.script), str(broken), "--analysis-at", "2026-07-15T10:00:00+00:00"],
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("multiple currencies require base_value", result.stderr)

    def test_rejects_multicurrency_without_explicit_method_approval(self) -> None:
        result = subprocess.run(
            [
                PYTHON, str(self.script), str(self.fixture),
                "--analysis-at", "2026-07-15T10:00:00+00:00",
            ],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--approved-conversion-method", result.stderr)


@unittest.skipUnless(
    importlib.util.find_spec("yaml") and importlib.util.find_spec("jsonschema"),
    "PyYAML or jsonschema is not installed",
)
class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = ROOT / "scripts" / "validate_company_context.py"

    def run_validator(self, context: Path, today: str = "2026-07-15") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, str(self.validator), str(context), "--today", today],
            capture_output=True,
            text=True,
        )

    def copy_example(self, directory: str) -> Path:
        target = Path(directory) / "company-context"
        shutil.copytree(REPO / "company-context", target)
        return target

    def copy_instance(self, directory: str) -> tuple[Path, Path]:
        context = self.copy_example(directory)
        ontology = Path(directory) / "gtm-ontology"
        shutil.copytree(REPO / "gtm-ontology", ontology)
        return ontology, context

    def run_linter(self, ontology: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, str(LINTER), str(ontology)],
            capture_output=True,
            text=True,
        )

    def test_current_example_validates(self) -> None:
        result = self.run_validator(REPO / "company-context")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)

    def test_taste_cannot_select_another_groups_audience(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, context = self.copy_instance(directory)
            taste = context / "product-groups/commerce-analytics/audience/customer-taste.md"
            text = taste.read_text(encoding="utf-8")
            taste.write_text(text.replace(
                "segment:commerce-analytics-core-segment", "segment:data-activation-core-segment"
            ), encoding="utf-8")
            validation = self.run_validator(context)
            lint = self.run_linter(ontology)
        for result in (validation, lint):
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("taste-scope", result.stdout)

    def test_messaging_cannot_select_another_groups_taste(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, context = self.copy_instance(directory)
            messaging = context / "product-groups/commerce-analytics/go-to-market/messaging.md"
            text = messaging.read_text(encoding="utf-8")
            messaging.write_text(text.replace(
                "customer-taste:commerce-analytics-customer-taste",
                "customer-taste:data-activation-customer-taste"
            ), encoding="utf-8")
            validation = self.run_validator(context)
            lint = self.run_linter(ontology)
        for result in (validation, lint):
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("taste-scope", result.stdout)

    def test_confirmed_messaging_cannot_use_draft_taste(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, context = self.copy_instance(directory)
            taste = context / "product-groups/commerce-analytics/audience/customer-taste.md"
            taste.write_text(taste.read_text().replace("status: example", "status: draft", 1))
            messaging = context / "product-groups/commerce-analytics/go-to-market/messaging.md"
            messaging.write_text(messaging.read_text().replace("status: example", "status: confirmed", 1))
            validation = self.run_validator(context)
            lint = self.run_linter(ontology)
        self.assertNotEqual(validation.returncode, 0)
        self.assertIn("confirmed-to-draft", validation.stdout)
        self.assertNotEqual(lint.returncode, 0)
        self.assertIn("draft-ref", lint.stdout)

    def test_taste_schema_rejects_scope_and_reference_kind_errors(self) -> None:
        for relative, old, new in [
            ("company/brand-taste.md", "scope: company", "scope: product-group:commerce-analytics"),
            ("company/brand-taste.md", "company-strategy:company-strategy", "personas:commerce-analytics-personas"),
            ("product-groups/commerce-analytics/audience/customer-taste.md",
             "persona_ref: personas:commerce-analytics-personas", "persona_ref: icp:commerce-analytics-icp"),
        ]:
            with self.subTest(relative=relative, replacement=new), tempfile.TemporaryDirectory() as directory:
                ontology, context = self.copy_instance(directory)
                artifact = context / relative
                artifact.write_text(artifact.read_text().replace(old, new, 1))
                for result in (self.run_validator(context), self.run_linter(ontology)):
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("schema", result.stdout)

    def test_missing_taste_ref_is_detected_in_markdown_body(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, context = self.copy_instance(directory)
            messaging = context / "product-groups/commerce-analytics/go-to-market/messaging.md"
            with messaging.open("a") as stream:
                stream.write("\nSelect customer-taste:missing-profile for this brief.\n")
            result = self.run_linter(ontology)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("customer-taste:missing-profile does not resolve", result.stdout)

    def test_render_includes_taste_nodes_and_selection_edges(self) -> None:
        renderer = load_module("taste_renderer", REPO / "tools/render_ontology.py")
        linter = load_module("taste_linter", LINTER)
        self.assertEqual(renderer.REF_RE.pattern, linter.REF_RE.pattern)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            docs, raws = renderer.collect(str(REPO / "gtm-ontology"))
            context_docs, context_raws = renderer.collect(str(REPO / "company-context"))
        docs.update(context_docs)
        raws.update(context_raws)
        nodes, edges = renderer.build_edges(docs, raws)
        self.assertIn("brand-taste:company-brand-taste", nodes)
        self.assertIn(("messaging:commerce-analytics-messaging",
                       "customer-taste:commerce-analytics-customer-taste"), edges)

    def test_missing_manifest_artifact_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            (context / "company" / "profile.md").unlink()
            result = self.run_validator(context)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing-artifact", result.stdout)

    def test_bad_reference_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            artifact = context / "product-groups" / "commerce-analytics" / "audience" / "icp.md"
            text = artifact.read_text(encoding="utf-8").replace(
                "segment:commerce-analytics-core-segment", "segment:missing-segment", 1
            )
            artifact.write_text(text, encoding="utf-8")
            result = self.run_validator(context)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unresolved-ref", result.stdout)

    def test_confirmed_artifact_cannot_reference_draft(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            group = context / "product-groups" / "commerce-analytics"
            source = group / "audience" / "icp.md"
            target = group / "market" / "segment.md"
            source.write_text(source.read_text(encoding="utf-8").replace("status: example", "status: confirmed", 1), encoding="utf-8")
            target.write_text(target.read_text(encoding="utf-8").replace("status: example", "status: draft", 1), encoding="utf-8")
            result = self.run_validator(context)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("confirmed-to-draft", result.stdout)

    def test_overdue_fact_is_a_warning(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            artifact = context / "company" / "strategy.md"
            artifact.write_text(artifact.read_text(encoding="utf-8").replace("last_verified: 2026-07-14", "last_verified: 2020-01-01", 1), encoding="utf-8")
            result = self.run_validator(context)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN [overdue]", result.stdout)

    def test_missing_frontmatter_field_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            artifact = context / "company" / "profile.md"
            artifact.write_text(artifact.read_text(encoding="utf-8").replace("scope: company\n", "", 1), encoding="utf-8")
            result = self.run_validator(context)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("artifact-field", result.stdout)

    def test_schema_rejects_non_string_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            artifact = context / "company" / "profile.md"
            artifact.write_text(
                artifact.read_text(encoding="utf-8").replace(
                    "  updated: 2026-07-14\n",
                    "  updated: 2026-07-14\n  evidence: []\n",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_validator(context)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR [schema]", result.stdout)

    def test_claim_registry_and_artifact_refs_validate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            artifact = context / "product-groups" / "commerce-analytics" / "market" / "segment.md"
            self.assertIn(
                "claim:commerce-metric-reconciliation-friction",
                artifact.read_text(encoding="utf-8"),
            )
            result = self.run_validator(context)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_claim_ref_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            artifact = context / "product-groups" / "commerce-analytics" / "market" / "segment.md"
            artifact.write_text(
                artifact.read_text(encoding="utf-8").replace(
                    "claim:commerce-metric-reconciliation-friction",
                    "claim:missing-claim",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_validator(context)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unresolved-ref", result.stdout)

    def test_claim_requires_supporting_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            registry = context / "claims.yaml"
            registry.write_text(
                registry.read_text(encoding="utf-8").replace("relation: supports", "relation: contradicts", 1),
                encoding="utf-8",
            )
            result = self.run_validator(context)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("claim-evidence", result.stdout)

    def test_confirmed_artifact_cannot_reference_draft_claim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            registry = context / "claims.yaml"
            artifact = context / "product-groups" / "commerce-analytics" / "market" / "segment.md"
            registry.write_text(
                registry.read_text(encoding="utf-8").replace("    status: example\n", "    status: draft\n", 1),
                encoding="utf-8",
            )
            artifact.write_text(
                artifact.read_text(encoding="utf-8").replace("  status: example\n", "  status: confirmed\n", 1),
                encoding="utf-8",
            )
            result = self.run_validator(context)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("confirmed-to-draft", result.stdout)

    def test_referenced_expired_claim_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            registry = context / "claims.yaml"
            registry.write_text(
                registry.read_text(encoding="utf-8").replace(
                    "    valid_from: 2026-07-14\n",
                    "    valid_from: 2026-07-14\n    valid_until: 2026-07-14\n",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_validator(context)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("claim-expired-ref", result.stdout)

    def test_unreferenced_expired_claim_remains_for_audit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            registry = context / "claims.yaml"
            artifact = context / "product-groups" / "commerce-analytics" / "market" / "segment.md"
            registry.write_text(
                registry.read_text(encoding="utf-8").replace(
                    "    valid_from: 2026-07-14\n",
                    "    valid_from: 2026-07-14\n    valid_until: 2026-07-14\n",
                    1,
                ),
                encoding="utf-8",
            )
            artifact.write_text(
                artifact.read_text(encoding="utf-8").replace(
                    "claim_refs:\n  - claim:commerce-metric-reconciliation-friction\n",
                    "",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_validator(context)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_linter_rejects_confirmed_artifact_ref_to_draft_claim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, context = self.copy_instance(directory)
            registry = context / "claims.yaml"
            artifact = context / "product-groups" / "commerce-analytics" / "market" / "segment.md"
            registry.write_text(
                registry.read_text(encoding="utf-8").replace("    status: example\n", "    status: draft\n", 1),
                encoding="utf-8",
            )
            artifact.write_text(
                artifact.read_text(encoding="utf-8").replace("  status: example\n", "  status: confirmed\n", 1),
                encoding="utf-8",
            )
            result = self.run_linter(ontology)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("draft-ref", result.stdout)

    def test_linter_rejects_artifact_ref_to_expired_claim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, context = self.copy_instance(directory)
            registry = context / "claims.yaml"
            registry.write_text(
                registry.read_text(encoding="utf-8").replace(
                    "    valid_from: 2026-07-14\n",
                    "    valid_from: 2026-07-14\n    valid_until: 2026-07-14\n",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_linter(ontology)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expired-ref", result.stdout)

    def test_linter_allows_unreferenced_expired_claim_for_audit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, context = self.copy_instance(directory)
            registry = context / "claims.yaml"
            artifact = context / "product-groups" / "commerce-analytics" / "market" / "segment.md"
            registry.write_text(
                registry.read_text(encoding="utf-8").replace(
                    "    valid_from: 2026-07-14\n",
                    "    valid_from: 2026-07-14\n    valid_until: 2026-07-14\n",
                    1,
                ),
                encoding="utf-8",
            )
            artifact.write_text(
                artifact.read_text(encoding="utf-8").replace(
                    "claim_refs:\n  - claim:commerce-metric-reconciliation-friction\n",
                    "",
                    1,
                ),
                encoding="utf-8",
            )
            # The decision summary can cite the same claim in prose. Remove every
            # remaining prose citation to make this an actually unreferenced claim.
            for path in context.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                if "`claim:commerce-metric-reconciliation-friction`" in text:
                    path.write_text(text.replace(
                        "`claim:commerce-metric-reconciliation-friction`",
                        "the archived friction observation"
                    ), encoding="utf-8")
            result = self.run_linter(ontology)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_claim_conflict_must_be_reciprocal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            registry = context / "claims.yaml"
            registry.write_text(
                registry.read_text(encoding="utf-8").replace(
                    "    valid_from: 2026-07-14\n",
                    "    conflicts_with: [claim:data-activation-warehouse-readiness]\n    valid_from: 2026-07-14\n",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_validator(context)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("claim-conflict", result.stdout)

    def test_gaps_report_contract_validates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = self.copy_example(directory)
            template = ROOT / "assets" / "artifact-templates" / "GAPS.md"
            (context / "GAPS.md").write_text(
                template.read_text(encoding="utf-8").replace("{{UPDATED}}", "2026-07-15"),
                encoding="utf-8",
            )
            manifest = context / "manifest.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "authoring_guide: ARTIFACT-GUIDE.md\n",
                    "authoring_guide: ARTIFACT-GUIDE.md\ngaps_report: GAPS.md\n",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_validator(context)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


@unittest.skipUnless(
    importlib.util.find_spec("yaml") and importlib.util.find_spec("jsonschema"),
    "PyYAML or jsonschema is not installed",
)
class InitializerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.initializer = ROOT / "scripts" / "init_company_context.py"
        self.validator = ROOT / "scripts" / "validate_company_context.py"

    def test_scaffolds_multiple_groups_without_unresolved_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "company-context"
            result = subprocess.run(
                [
                    PYTHON, str(self.initializer), "--output", str(output),
                    "--company-id", "example", "--company-name", "Example: Co",
                    "--company-domain", "https://example.com", "--language", "pl",
                    "--updated", "2026-07-15", "--product-group", "analytics:Analytics",
                    "--product-group", "activation:Data Activation",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(any("{{" in path.read_text(encoding="utf-8") for path in output.rglob("*") if path.is_file()))
            self.assertFalse(list(output.rglob("*-taste.md")))
            for path in output.rglob("messaging.md"):
                self.assertNotIn("taste_ref:", path.read_text())
            validation = subprocess.run(
                [PYTHON, str(self.validator), str(output), "--today", "2026-07-15"],
                capture_output=True,
                text=True,
            )
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
        self.assertIn("0 error(s)", validation.stdout)

    def test_rejects_invalid_domain_and_date(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    PYTHON, str(self.initializer), "--output", str(Path(directory) / "context"),
                    "--company-id", "example", "--company-name", "Example",
                    "--company-domain", "example.com", "--updated", "15-07-2026",
                ],
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("absolute HTTP(S) URL", result.stderr)

    def test_optional_taste_is_independent_and_group_selective(self) -> None:
        import yaml
        for brand, customer in [(False, True), (True, False), (True, True)]:
            with self.subTest(brand=brand, customer=customer), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "context"
                args = [PYTHON, str(self.initializer), "--output", str(output),
                        "--company-id", "example", "--company-name", "Example",
                        "--company-domain", "https://example.com", "--updated", "2026-10-02",
                        "--product-group", "analytics:Analytics", "--product-group", "activation:Activation"]
                if brand:
                    args += ["--brand-taste"]
                if customer:
                    args += ["--customer-taste", "analytics"]
                result = subprocess.run(args, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual((output / "company/brand-taste.md").exists(), brand)
                self.assertEqual((output / "product-groups/analytics/audience/customer-taste.md").exists(), customer)
                self.assertFalse((output / "product-groups/activation/audience/customer-taste.md").exists())
                for group in ["analytics", "activation"]:
                    path = output / f"product-groups/{group}/go-to-market/messaging.md"
                    head = yaml.safe_load(path.read_text().split("---")[1])
                    self.assertEqual("brand_taste_ref" in head, brand)
                    self.assertEqual("customer_taste_ref" in head, customer and group == "analytics")
                validation = self.run_validator(output)
                self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_rejects_customer_taste_for_unknown_group(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([
                PYTHON, str(self.initializer), "--output", str(Path(directory) / "context"),
                "--company-id", "example", "--company-name", "Example",
                "--company-domain", "https://example.com", "--updated", "2026-10-02",
                "--product-group", "analytics", "--customer-taste", "missing",
            ], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("customer taste references unknown product groups", result.stdout)

    def test_scaffolds_only_explicitly_approved_motion_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "company-context"
            result = subprocess.run(
                [
                    PYTHON, str(self.initializer), "--output", str(output),
                    "--company-id", "example", "--company-name", "Example",
                    "--company-domain", "https://example.com", "--updated", "2026-07-15",
                    "--product-group", "analytics:Analytics", "--motion",
                    "analytics:analytics-inbound:Analytics inbound:Educate and qualify active analytics teams.",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            motion = output / "product-groups" / "analytics" / "go-to-market" / "motions.md"
            self.assertIn("id: analytics-inbound", motion.read_text(encoding="utf-8"))
            validation = self.run_validator(output)
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def run_validator(self, context: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, str(self.validator), str(context), "--today", "2026-07-15"],
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
