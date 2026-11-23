# forge-release

Repository-level CAD-CI item that release-verifies the exact Forge package
built by `forge-package`.

## Purpose

This is package release verification, not package publication. It runs a fixed
representative Forge example set against the exact built wheel and records the
result as durable Forge release evidence.

## Contract

- **Item id:** `forge-release`
- **Kind:** `verification`
- **Dependency:** `forge-package`
- **Implementation:** [`scripts/tool_verify.py`](../../scripts/tool_verify.py)
  with shared mechanics from
  [`scripts/forge_example.py`](../../scripts/forge_example.py)
- **Output:** `tool_verify`
- **Watched identity inputs:** Forge source/package metadata, `CHANGELOG.md`
  and the representative example/test set listed in `ci.yml`

The authoritative publication contract is
[`docs/release.md`](../../docs/release.md). A green `forge-release` item does
not itself publish a package.

See the repository-level [CI map](../README.md).
