# release-policy

Repository-level test item for Forge's explicit release-publication policy.

## Purpose

Release validation and publication rules are tested without starting any CAD
runtime. This keeps policy regressions separate from model verification.

## Contract

- **Item id:** `release-policy`
- **Kind:** `test`
- **Dependencies:** none
- **Validation implementation:**
  [`scripts/release/validate_release.py`](../../scripts/release/validate_release.py)
- **Publication implementation:**
  [`scripts/release/publish_release.py`](../../scripts/release/publish_release.py)
- **Tests:** `scripts/release/test_validate_release.py` and
  `scripts/release/test_publish_release.py`
- **Authoritative contract:** [`docs/release.md`](../../docs/release.md)

This item tests policy only. Actual publication remains an explicit
owner-controlled workflow operation.

See the repository-level [CI map](../README.md).
