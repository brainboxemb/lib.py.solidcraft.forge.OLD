# reference-verification-batch

Repository-level producer for the active independent CAD reference models.

## Purpose

Forge compares model intent with independent PythonSCAD, pyBOSL2, CadQuery and
build123d implementations. This item runs the active reference set in one shared
reference-runtime batch and writes per-reference outputs plus verification
diagram output.

Individual reference child items below
`examples/<model>/<implementation>/ci.yml` remain the public reference items
and consume/copy their own result.

## Contract

- **Item id:** `reference-verification-batch`
- **Kind:** `verification`
- **Dependency:** `cad-verification-package`
- **Entry point:** [`scripts/reference_verification_batch.py`](../../scripts/reference_verification_batch.py)
- **Reference support:** `verification/reference_validation.py`,
  `verification/reference_preview.py` and
  `verification/build123d_export.py`
- **Diagram producer:** [`scripts/build_diagrams.py`](../../scripts/build_diagrams.py)
- **Outputs:** `items/` and `diagrams/`

The heavy reference runtime is selected by the root
[`cad-ci.yml`](../../cad-ci.yml); runtime packaging is not owned here.

See the repository-level [CI map](../README.md).
