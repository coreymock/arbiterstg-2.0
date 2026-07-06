# ArbiterSTG 2.0

ArbiterSTG stands for Structural Trace Governance.

ArbiterSTG is a post-execution structural trace-governance framework for classifying, routing, admitting, masking, transferring, shadowing, limiting, or nulling residue after execution has occurred.

It does not authorize execution. It does not determine truth, meaning, origin, value, inheritance, observer completion, legality, morality, safety, or final accountability.

ArbiterSTG classifies what happens to trace after execution.

## Position

Parent architecture:

```text
Machine-Dream Syntax (MDS) -> ArbiterSTG
```

MDS supplies the execution-observer-residue structure. ArbiterSTG supplies post-execution trace classification and routing logic.

MDS governing equation:

```text
S = (F -> O)[Delta T] + D/L +/- R
```

Where:

- `F` = Field
- `O` = Observer
- `Delta T` = structuring interval / non-coincidence between execution and observer stabilization
- `D/L` = density/leak condition
- `+/- R` = residue produced, preserved, inaccessible, degraded, recruited, or lost

## Repository Contents

- [paper](paper/arbiterstg-2.0-draft.md): concise framework draft
- [docs](docs): core model, modes, boundaries, indices, and workflow guidance
- [schemas](schemas): JSON schemas for classification, ledgers, and scoring
- [templates](templates): reusable YAML and Markdown templates
- [examples](examples): worked examples and sample CLI input
- [diagrams](diagrams): Mermaid diagrams for transitions and architecture position
- [cli](cli/arbiterstg.py): local report generator

## Quick CLI Use

```bash
python3 cli/arbiterstg.py examples/residue-input.example.json
```

The CLI reads structured residue input and prints a Trace Classification Report in Markdown.

## Core Warning

Do not treat trace absence as proof of non-execution.

Do not treat trace presence as proof of meaning.

Do not treat admission as validation.

Do not treat routing as truth.

Do not treat transfer as ownership.

Do not treat institutional assignment as origin.

Do not treat observer access as execution itself.

Do not treat proxy legibility as full residue recovery.

