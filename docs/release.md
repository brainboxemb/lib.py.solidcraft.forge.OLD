# Forge release

This document describes Forge-specific release rules and how Forge consumes the
shared CAD release flow.

## Ownership

Forge is a release-flow consumer.

Released `tool.cad.ci v0.36.1` owns:

- parsing/checking the stable main `ci-build-record`;
- proving the requested release commit is the exact stable build source;
- keeping Pages out of release qualification.

Released `tool.py.lib.ci v0.2.1` owns:

- strict `/release vX.Y.Z <40-character-sha>` parsing;
- repository-owner enforcement;
- requiring the requested SHA to remain the stable branch head;
- annotated tag creation/verification;
- GitHub Release creation/verification;
- idempotent repeated publication;
- publication reporting on the triggering issue.

Forge owns only repository-specific validation:

- `scpf/pyproject.toml` package version matches the requested version;
- `CHANGELOG.md` contains a dated release section with release content;
- `docs/background/design/release-blockers.txt` has no active blocker;
- `scpf/scpf/version.py::TESTED_SOLIDCRAFT_VERSION` is readable;
- the Forge validator writes the release notes used by the shared publisher.

`gh-pages` is web output and is not release evidence.

## Current release state

Latest actual Forge release: **v0.13.2**.

- annotated tag: `v0.13.2`;
- exact source:
  `ea5710a5d2d33b0633b93c5da95dd5b74f126aa4`;
- published GitHub Release: `v0.13.2`;
- qualified SolidCraft: `0.45.0`;
- exact main branch build: `45269510406`;
- central release run: `45269991837`.

The annotated tag resolves exactly to the release source above.

v0.13.2 is the consumer hotfix for #796. It preserves symbolic placed-primitive
dimensions through Box/Cylinder/Cone anchor arithmetic and fixes the
v0.13.1-adoption failure exposed by the existing `hub75-panel` model.

v0.13.2 adds no new public modelling API beyond v0.13.1. It is the recommended
v0.13.x consumer baseline.

The v0.12.0, v0.13.0 and v0.13.1 tags remain valid and immutable.

### Unreleased baseline

Current unreleased Forge development is qualified against **SolidCraft 0.48.1**
through immutable `docker.cad.solidcraft v0.3.5`. The canonical command
reference is `docs/reference/solidcraft/0.48.1/`.

This does not rewrite the v0.13.2 release record above: v0.13.2 remains
qualified against SolidCraft 0.45.0. A later Forge release must explicitly carry
the 0.48.1 baseline and retained #753 component-Cylinder regression evidence.

## Consumer workflow

Forge keeps a copy-ready thin wrapper in:

```text
.github/workflows/release.yml
```

It pins:

```text
brainboxemb/tool.cad.ci/.github/workflows/reusable-release.yml@v0.36.1
```

with:

```text
stable_ref: main
build_branch: build
validator_path: scripts/release/validate_release.py
```

Do not add local command parsing, build-record parsing, tag creation, GitHub
Release calls or Pages checks to this wrapper.

## Forge validator

The shared workflow checks out the exact requested source commit and calls:

```text
python scripts/release/validate_release.py \
  --version X.Y.Z \
  --target-sha <exact-sha> \
  --notes-out <path>
```

The validator reads only files from that exact checkout. It does not fetch or
parse generated branches.

The `target-sha` argument is part of the shared validator interface; exact
source selection and stable-main verification are owned by the shared release
flow.

## Publishing

Publication remains an explicit repository-owner action. A normal CAD-CI build
never creates a release automatically.

After the intended release commit is stable on `main` and its main build is
green, comment on the release tracking issue:

```text
/release vX.Y.Z <exact-40-character-main-sha>
```

The central flow then:

1. checks the stable main `ci-build-record`;
2. runs the Forge-specific validator;
3. creates or verifies the annotated tag and GitHub Release;
4. reports the release on the tracking issue.

A repeated command for the exact same version/SHA is idempotent. A stale source,
conflicting tag or mismatched release is rejected by the shared flow.

## Next checkpoint

No Forge release is currently active.

Resume the post-v0.13.2 CAD/API/documentation work. Product-CAD PR #406 should
consume the exact released v0.13.2 source before any later Forge release is
considered.
