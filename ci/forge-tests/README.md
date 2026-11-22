# forge-tests

Repository-level CAD-CI item that runs the Forge Python test suite against the
exact wheel produced by `forge-package`.

## Purpose

Package construction and package testing are separate items. This item proves
the reusable Forge API/compiler package and repository policy helpers without
rebuilding the wheel.

## Contract

- **Item id:** `forge-tests`
- **Kind:** `tool`
- **Dependency:** `forge-package`
- **Implementation:** [`scripts/tool_ci.py`](../../scripts/tool_ci.py)
- **Shared package helper:** [`scripts/forge_example.py`](../../scripts/forge_example.py)
- **Additional repository policy coverage:** qualification-summary and
  merge-policy tests

Generic CAD-CI selection, scheduling and caching are not implemented here; they
come from the released CAD-CI stack.

See the repository-level [CI map](../README.md) and
[scripts inventory](../../scripts/README.md).
