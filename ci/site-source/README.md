# site-source

Repository-level test item for Forge's site source and presentation metadata.

## Purpose

The public site is derived from model-owned metadata, README content and durable
build evidence. These checks catch source/metadata regressions without starting
SolidCraft or an independent reference runtime.

## Contract

- **Item id:** `site-source`
- **Kind:** `test`
- **Dependencies:** none
- **Checks:**
  - `site/test_build_evidence.py`
  - `site/test_example_metadata.py`
  - `site/test_site.py`
- **Watched source:** site code, workflow integration, model metadata/README
  files, role declarations and model verification/source files used by the site

Model presentation metadata remains model-owned. This item validates it; it
does not maintain a second central model catalog.

See the repository-level [CI map](../README.md) and
[`examples/README.md`](../../examples/README.md).
