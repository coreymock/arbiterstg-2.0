#!/usr/bin/env python3
"""Generate an ArbiterSTG Trace Classification Report from JSON input."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


MODES = {
    "Admission",
    "Limited Admission",
    "Masking",
    "Routing",
    "Shadow",
    "Transfer",
    "Null",
}


RAI_BY_ACCESSIBILITY = {
    "destroyed": 0,
    "none": 1,
    "unknown": 1,
    "minimal": 2,
    "partial": 3,
    "substantial": 4,
    "full": 5,
}


def load_input(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}") from exc
    except OSError as exc:
        raise SystemExit(f"Could not read input file: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("Input must be a JSON object.")
    if not isinstance(data.get("residues"), list) or not data["residues"]:
        raise SystemExit("Input must include a non-empty residues array.")
    return data


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if str(value).strip():
        return [str(value)]
    return []


def classify(residue: dict[str, Any]) -> tuple[str, list[str]]:
    proposed = residue.get("proposed_mode")
    if isinstance(proposed, str) and proposed in MODES:
        return proposed, ["The input supplied an explicit proposed mode."]

    produced = bool(residue.get("produced"))
    accessibility = str(residue.get("accessibility", "unknown"))
    support_limitations = as_list(residue.get("support_limitations"))
    masking_indicators = as_list(residue.get("masking_indicators"))
    bridge_residue = bool(residue.get("bridge_residue"))
    assigned_route = residue.get("assigned_route")
    transfer_target = residue.get("transfer_target")

    if not produced:
        return "Null", ["No produced residue is asserted."]

    if masking_indicators:
        return "Masking", ["Trace handling contains masking indicators."]

    if transfer_target:
        return "Transfer", ["Trace is moved to another route, actor, system, context, or archive."]

    if accessibility in {"destroyed"}:
        return "Null", ["Trace is described as destroyed or structurally unrecoverable."]

    if accessibility in {"none", "unknown"} and not bridge_residue:
        return "Shadow", ["Residue is asserted but remains inaccessible or unresolved."]

    if bridge_residue or support_limitations or accessibility in {"minimal", "partial"}:
        return "Limited Admission", ["Residue exists but access or support is constrained."]

    if assigned_route:
        return "Routing", ["Residue is directed through a named route."]

    if accessibility in {"substantial", "full"}:
        return "Admission", ["Residue is accessible enough to enter the post-execution record."]

    return "Limited Admission", ["Residue requires constrained handling."]


def residue_class(residue: dict[str, Any]) -> str:
    produced = bool(residue.get("produced"))
    accessibility = str(residue.get("accessibility", "unknown"))

    if residue.get("bridge_residue"):
        return "R_b"
    if not produced:
        return "unknown"
    if residue.get("assigned_route"):
        return "R_s"
    if accessibility in {"none", "unknown", "destroyed"}:
        return "R_u"
    return "R_a"


def score_rai(residue: dict[str, Any]) -> int:
    accessibility = str(residue.get("accessibility", "unknown"))
    score = RAI_BY_ACCESSIBILITY.get(accessibility, 1)
    if residue.get("bridge_residue") and score < 5:
        score += 1
    if as_list(residue.get("support_limitations")) and score > 0:
        score -= 1
    return max(0, min(5, score))


def score_rlci(residue: dict[str, Any], mode: str) -> int:
    accessibility = str(residue.get("accessibility", "unknown"))
    base = {
        "full": 1,
        "substantial": 1,
        "partial": 3,
        "minimal": 4,
        "none": 4,
        "unknown": 4,
        "destroyed": 5,
    }.get(accessibility, 3)

    if mode == "Null":
        base = max(base, 4)
    if mode == "Masking":
        base += 1
    if residue.get("bridge_residue"):
        base = max(1, base - 1)
    if as_list(residue.get("support_limitations")):
        base += 1
    return max(0, min(5, base))


def lacunal_trace_present(residue: dict[str, Any]) -> bool:
    if not residue.get("produced"):
        return False
    accessibility = str(residue.get("accessibility", "unknown"))
    if accessibility in {"none", "unknown", "minimal"}:
        return True
    if accessibility == "partial" and residue.get("bridge_residue"):
        return True
    return False


def claim_limits(residue: dict[str, Any], mode: str) -> list[str]:
    limits = [
        "This classification does not determine truth, origin, ownership, legality, morality, safety, or final accountability."
    ]

    claims = " ".join(as_list(residue.get("claims"))).lower()
    if "origin" in claims:
        limits.append("The available trace does not establish origin.")
    if "observer completion" in claims or "full recovery" in claims:
        limits.append("The available trace does not establish full observer completion or full residue recovery.")
    if "no trace" in claims or "no execution" in claims:
        limits.append("Trace absence or access failure does not prove non-execution.")
    if mode == "Routing":
        limits.append("Routing is not truth.")
    if mode == "Transfer":
        limits.append("Transfer is not ownership.")
    if mode == "Admission":
        limits.append("Admission is not validation.")
    if mode == "Limited Admission":
        limits.append("Limited Admission prevents erasure while marking constraint.")
    if mode == "Shadow":
        limits.append("Shadow status preserves unresolved trace without validating it.")
    if mode == "Null":
        limits.append("Null status does not prove non-execution.")

    return list(dict.fromkeys(limits))


def md_list(items: list[str]) -> str:
    if not items:
        return "- None recorded."
    return "\n".join(f"- {item}" for item in items)


def generate_report(data: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Trace Classification Report")
    lines.append("")
    lines.append(f"Case ID: `{data.get('case_id', '')}`")
    lines.append("")
    lines.append(f"Title: {data.get('title', '')}")
    lines.append("")
    lines.append(f"Review date: {data.get('review_date') or date.today().isoformat()}")
    if data.get("reviewer"):
        lines.append("")
        lines.append(f"Reviewer: {data['reviewer']}")
    lines.append("")
    lines.append("## Execution Context")
    lines.append("")
    lines.append(str(data.get("execution_context", "")))
    lines.append("")
    lines.append("## Boundary Statement")
    lines.append("")
    lines.append(
        "ArbiterSTG classifies post-execution trace handling. This report does not "
        "determine truth, meaning, origin, ownership, legality, morality, safety, "
        "or final accountability."
    )

    for residue in data["residues"]:
        mode, rationale = classify(residue)
        rclass = residue_class(residue)
        rai = score_rai(residue)
        rlci = score_rlci(residue, mode)
        authority_flags = as_list(residue.get("authority_laundering_indicators"))
        collapse_risk = bool(residue.get("collapse_by_clarification_risk"))
        lacunal = lacunal_trace_present(residue)

        lines.append("")
        lines.append(f"## Residue {residue.get('residue_id', '')}")
        lines.append("")
        lines.append(f"Description: {residue.get('description', '')}")
        lines.append("")
        lines.append(f"Residue class: `{rclass}`")
        lines.append("")
        lines.append(f"Assigned mode: {mode}")
        lines.append("")
        lines.append("Rationale:")
        lines.append("")
        lines.append(md_list(rationale))
        lines.append("")
        lines.append(f"Accessibility: `{residue.get('accessibility', 'unknown')}`")
        if residue.get("assigned_route"):
            lines.append("")
            lines.append(f"Route: {residue['assigned_route']}")
        if residue.get("transfer_target"):
            lines.append("")
            lines.append(f"Transfer target: {residue['transfer_target']}")
        if residue.get("bridge_residue"):
            lines.append("")
            lines.append(f"Bridge residue: {residue.get('bridge_description') or 'Present'}")
        lines.append("")
        lines.append("Support limitations:")
        lines.append("")
        lines.append(md_list(as_list(residue.get("support_limitations"))))
        lines.append("")
        lines.append("Flags:")
        lines.append("")
        flag_lines: list[str] = []
        if lacunal:
            flag_lines.append("Lacunal Trace: residue persists while access or bridge formation remains incomplete.")
        if authority_flags:
            flag_lines.extend(f"Authority Laundering: {flag}" for flag in authority_flags)
        if collapse_risk:
            flag_lines.append("Collapse by Clarification: clarification may damage or distort the trace condition.")
        lines.append(md_list(flag_lines))
        lines.append("")
        lines.append("Indices:")
        lines.append("")
        lines.append(f"- RLCI: {rlci}")
        lines.append(f"- RAI: {rai}")
        lines.append("")
        lines.append("Claim limits:")
        lines.append("")
        lines.append(md_list(claim_limits(residue, mode)))

    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an ArbiterSTG Trace Classification Report.")
    parser.add_argument("input", type=Path, help="Path to a JSON trace classification input file.")
    args = parser.parse_args(argv)

    data = load_input(args.input)
    sys.stdout.write(generate_report(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

