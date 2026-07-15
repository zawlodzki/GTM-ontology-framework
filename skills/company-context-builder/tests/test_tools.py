from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PYTHON = sys.executable


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

    def test_current_example_validates(self) -> None:
        result = self.run_validator(REPO / "company-context")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)

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
