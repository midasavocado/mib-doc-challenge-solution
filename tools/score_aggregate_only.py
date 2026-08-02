#!/usr/bin/env python3
"""Run the official evaluator without exposing case-level validation data."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def load_evaluator(path: Path):
    spec = importlib.util.spec_from_file_location("mib_official_evaluator", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load evaluator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print only aggregate MIB scores and structural validity counts."
    )
    parser.add_argument("--evaluator", required=True, type=Path)
    parser.add_argument("--truth", required=True, type=Path)
    parser.add_argument("--submission", required=True, type=Path)
    args = parser.parse_args()

    evaluator = load_evaluator(args.evaluator)
    truth = evaluator.read_truth(args.truth)
    predictions = evaluator.read_submission(args.submission)
    results, _case_scores = evaluator.build_results(truth, predictions)

    counts = results["counts"]
    allowed = {
        "score_version": results["score_version"],
        "scores": results["scores"],
        "catastrophic_false_approvals": results["raw"][
            "catastrophic_false_approvals"
        ],
        "validity": {
            key: counts[key]
            for key in (
                "truth_cases",
                "submitted_records",
                "scored_predictions",
                "missing_cases",
                "extra_cases",
                "duplicate_case_ids",
                "blank_case_rows",
                "invalid_adjudication_records",
                "invalid_confidence_records",
                "invalid_fee_status_records",
            )
        },
    }
    print(json.dumps(allowed, indent=2, sort_keys=True))

    invalid = sum(
        allowed["validity"][key]
        for key in (
            "extra_cases",
            "duplicate_case_ids",
            "blank_case_rows",
            "invalid_adjudication_records",
            "invalid_confidence_records",
            "invalid_fee_status_records",
        )
    )
    return 2 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
