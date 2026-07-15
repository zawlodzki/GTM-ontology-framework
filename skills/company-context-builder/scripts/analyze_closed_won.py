#!/usr/bin/env python3
"""Analyze a normalized Closed Won CSV without persisting customer content."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import statistics
import sys
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


DIMENSIONS = (
    "pipeline", "product_group", "offer", "use_case", "segment", "industry",
    "geography", "company_size_band", "source", "sales_owner", "trigger",
    "current_alternative", "buying_roles", "reason_won",
)
ANOMALY_FIELDS = ("is_test", "duplicate_of", "is_cancelled", "is_refunded", "is_correction")
DETAIL_FIELDS = (
    "problem", "workflow", "trigger", "current_alternative", "buying_roles",
    "objections", "selection_criteria", "reason_won", "implementation_evidence",
)


class AnalysisError(ValueError):
    pass


def truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def decimal_value(value: str | None, field: str) -> Decimal | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return Decimal(text.replace(",", "."))
    except InvalidOperation as exc:
        raise AnalysisError(f"invalid decimal in {field}: {value!r}") from exc


def parse_datetime(value: str, timezone: ZoneInfo) -> dt.datetime:
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError as exc:
        raise AnalysisError(f"invalid won_at value: {value!r}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone)
    return parsed.astimezone(timezone)


def one_year_before(value: dt.datetime) -> dt.datetime:
    try:
        return value.replace(year=value.year - 1)
    except ValueError:
        return value.replace(year=value.year - 1, day=28)


def counter(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    values = Counter(row.get(field, "").strip() for row in rows if row.get(field, "").strip())
    return dict(sorted(values.items(), key=lambda item: (-item[1], item[0])))


def analyze(
    rows: list[dict[str, str]],
    analysis_at: dt.datetime,
    top_n: int,
    approved_conversion_method: str | None = None,
) -> dict[str, Any]:
    if not rows:
        raise AnalysisError("input contains no records")
    required = {"opportunity_id", "won_at", "value", "currency"}
    missing_columns = sorted(required - set(rows[0]))
    if missing_columns:
        raise AnalysisError(f"missing required columns: {', '.join(missing_columns)}")

    timezone = analysis_at.tzinfo
    if timezone is None:
        raise AnalysisError("analysis timestamp must have a timezone")
    start = one_year_before(analysis_at)
    cohort: list[dict[str, Any]] = []
    for raw in rows:
        won_at = parse_datetime(raw.get("won_at", ""), timezone)  # type: ignore[arg-type]
        if not start <= won_at <= analysis_at:
            continue
        value = decimal_value(raw.get("value"), "value")
        if value is None:
            raise AnalysisError(f"opportunity {raw.get('opportunity_id')!r} has no value")
        base_value = decimal_value(raw.get("base_value"), "base_value")
        cohort.append({"raw": raw, "won_at": won_at, "value": value, "base_value": base_value})
    if not cohort:
        raise AnalysisError("no records fall inside the trailing 12-month cohort")

    currencies = {item["raw"].get("currency", "").strip() for item in cohort}
    currencies.discard("")
    if not currencies:
        raise AnalysisError("currency is empty for every cohort record")
    if len(currencies) > 1 and any(item["base_value"] is None for item in cohort):
        raise AnalysisError("multiple currencies require base_value for every cohort record")
    if len(currencies) > 1 and not approved_conversion_method:
        raise AnalysisError("multiple currencies require --approved-conversion-method")
    if len(currencies) > 1 and (
        "base_value_source" not in rows[0]
        or any(not item["raw"].get("base_value_source", "").strip() for item in cohort)
    ):
        raise AnalysisError("multiple currencies require base_value_source for every cohort record")

    base_currencies = {item["raw"].get("base_currency", "").strip() for item in cohort}
    base_currencies.discard("")
    if len(base_currencies) > 1:
        raise AnalysisError("base_currency is inconsistent across records")
    base_currency = next(iter(base_currencies), next(iter(currencies)) if len(currencies) == 1 else "UNKNOWN")

    for item in cohort:
        item["comparable_value"] = item["base_value"] if item["base_value"] is not None else item["value"]
    ranked = sorted(cohort, key=lambda item: (item["comparable_value"], item["won_at"]), reverse=True)

    fieldnames = list(rows[0])
    missingness = {
        field: {"missing": sum(not item["raw"].get(field, "").strip() for item in cohort), "total": len(cohort)}
        for field in fieldnames
    }
    anomalies = {
        field: [item["raw"].get("opportunity_id") for item in cohort if truthy(item["raw"].get(field)) or (field == "duplicate_of" and item["raw"].get(field, "").strip())]
        for field in ANOMALY_FIELDS if field in fieldnames
    }
    dimensions = {field: counter([item["raw"] for item in cohort], field) for field in DIMENSIONS if field in fieldnames}
    cycle_days = [float(value) for item in cohort if (value := decimal_value(item["raw"].get("cycle_days"), "cycle_days")) is not None]

    top: list[dict[str, Any]] = []
    for item in ranked[:top_n]:
        raw = item["raw"]
        top.append({
            "opportunity_id": raw.get("opportunity_id"),
            "won_at": item["won_at"].isoformat(),
            "pipeline": raw.get("pipeline") or None,
            "comparable_value": float(item["comparable_value"]),
            "base_currency": base_currency,
            "product_group": raw.get("product_group") or None,
            "offer": raw.get("offer") or None,
            "use_case": raw.get("use_case") or None,
            "segment": raw.get("segment") or None,
            "detail_evidence": {
                field: bool(raw.get(field, "").strip()) for field in DETAIL_FIELDS if field in fieldnames
            },
        })

    result: dict[str, Any] = {
        "cohort": {
            "start": start.isoformat(),
            "end": analysis_at.isoformat(),
            "records": len(cohort),
            "input_records": len(rows),
            "selection": "CRM won_at in trailing 12 months; no anomaly candidates excluded",
        },
        "currencies": counter([item["raw"] for item in cohort], "currency"),
        "base_currency": base_currency,
        "base_value_sources": counter([item["raw"] for item in cohort], "base_value_source"),
        "approved_conversion_method": approved_conversion_method,
        "missingness": missingness,
        "anomaly_candidates": anomalies,
        "dimensions": dimensions,
        "top_opportunities": top,
        "privacy_note": "Working output may contain opportunity IDs; never copy IDs or record-level data into company-context/.",
    }
    if cycle_days:
        result["cycle_days"] = {
            "count": len(cycle_days),
            "mean": statistics.fmean(cycle_days),
            "median": statistics.median(cycle_days),
        }
    return result


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="normalized Closed Won CSV")
    parser.add_argument("--timezone", default="UTC", help="IANA timezone")
    parser.add_argument("--analysis-at", help="ISO timestamp; defaults to now")
    parser.add_argument(
        "--approved-conversion-method",
        help="exact user-approved method; required when the cohort has multiple currencies",
    )
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--output", type=Path, help="write working JSON report")
    args = parser.parse_args(argv)
    if args.top < 1:
        parser.error("--top must be at least 1")
    try:
        timezone = ZoneInfo(args.timezone)
        analysis_at = parse_datetime(args.analysis_at, timezone) if args.analysis_at else dt.datetime.now(timezone)
        result = analyze(read_csv(args.input), analysis_at, args.top, args.approved_conversion_method)
    except (AnalysisError, OSError, ZoneInfoNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    rendered = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
