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

Latest actual Forge release: **v0.13.1**.

- annotated tag: `v0.13.1`;
- exact source:
  `17a4e1d0e2edf0124d40daf5425891fdf65c24be`;
- published GitHub Release: `v0.13.1`;
- qualified SolidCraft: `0.45.0`;
- exact main branch build: `45262080873`;
- central release run: `45262594629`.

v0.13.1 is a release/documentation patch on the v0.13.0 modelling baseline.
Its notes explicitly explain that v0.12.0 was published before
#746/#747/#749/#750 reached stable main. Models depending on those fixes require
v0.13.0 or newer; v0.13.1 is the recommended patch level.

The v0.12.0 and v0.13.0 tags remain valid and immutable.

## Active release checkpoint

Forge **v0.13.2** is the active hotfix release under #800.

The #796 implementation is already qualified on both permanent lanes:

- `dev-cad` source: `926feda24ee61c01ab5bfe00521b6aae0c4ede2a`;
- exact dev-cad branch build: `45267112890`;
- stable `main` hotfix source before release metadata:
  `9df3a2fa5634ea1d44046959a54b4a8f060ab603`;
- exact main branch build: `45268325135`.

The v0.13.2 preparation changes only package/release metadata on top of that
qualified hotfix baseline. After this preparation reaches `main`, require the
exact resulting main branch build green before publishing.

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

Finish #800 as Forge v0.13.2.

After the release-preparation PR reaches `main`, require the exact resulting
main branch build green and publish only with:

```text
/release v0.13.2 <exact-40-character-main-sha>
```

Then verify that the annotated tag and GitHub Release resolve to that exact SHA
before asking product-CAD PR #406 to adopt the hotfix.
