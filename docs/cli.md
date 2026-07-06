# CLI

The local CLI accepts structured residue input and outputs a Markdown Trace Classification Report.

## Run

```bash
python3 cli/arbiterstg.py examples/residue-input.example.json
```

## Input Shape

The input is a JSON document with a case identifier, title, execution context, and a list of residues.

Each residue may include:

- `residue_id`
- `description`
- `produced`
- `accessibility`
- `assigned_route`
- `transfer_target`
- `bridge_residue`
- `bridge_description`
- `support_limitations`
- `claims`
- `masking_indicators`
- `authority_laundering_indicators`
- `collapse_by_clarification_risk`
- `proposed_mode`

## Classification Behavior

The CLI is intentionally conservative.

It favors Limited Admission when trace exists but support is incomplete, proxy-mediated, bridge-dependent, or otherwise constrained. It flags overclaims but does not decide truth, liability, origin, safety, or final accountability.

