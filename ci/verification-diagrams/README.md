# verification-diagrams

Repository-level CI item exposing the verification diagrams produced by the
shared independent-reference batch.

## Purpose

Diagram rendering already happens in `reference-verification-batch`. This item
does not start another renderer/runtime; it copies the produced `diagrams/`
output into its own durable item result.

## Contract

- **Item id:** `verification-diagrams`
- **Kind:** `verification`
- **Dependency:** `reference-verification-batch`
- **Action:** CAD-CI dependency-output `copy:`
- **Output:** `diagrams/`
- **Sources:** `verification/diagrams/sources/`
- **Producer implementation:** [`scripts/build_diagrams.py`](../../scripts/build_diagrams.py)

The generic dependency-copy behavior belongs to released CAD-CI. Forge owns
only the diagram sources and Forge-specific rendering inputs.

See the repository-level [CI map](../README.md).
