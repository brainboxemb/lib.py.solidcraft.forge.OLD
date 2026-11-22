# cad-verification-package

Repository-level CAD-CI item that prepares the exact released
`lib.py.cad.verification` package consumed by Forge verification.

## Purpose

Forge verification must use a released verification-library revision without
embedding that library in the SolidCraft runtime image. This item builds that
exact dependency once and exposes it to downstream verification items.

## Contract

- **Item id:** `cad-verification-package`
- **Kind:** `tool`
- **Implementation:** [`scripts/verification_package.py`](../../scripts/verification_package.py)
- **Configuration:** [`package.json`](package.json)
- **Outputs:** `dist/` and `provenance.json`
- **Consumers:** `model-verification-batch` and `reference-verification-batch`

The package pin and transport are Forge-owned integration concerns. Generic
verification behavior remains owned by `lib.py.cad.verification`.

See the repository-level [CI map](../README.md) and
[scripts inventory](../../scripts/README.md).
