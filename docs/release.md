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

Latest actual Forge release: **v0.11.0**.

- tag: `v0.11.0`;
- exact source:
  `9258d54079981604b6dd777a4c4face897c190fe`;
- qualified SolidCraft: `0.45.0`.

The v0.12.0 source preparation is already present in the current integration
history. Publication waits for #739 to reach stable `main` and for the exact
resulting main build to be green.

The earlier failed v0.12.0 release attempt created no v0.12.0 tag or GitHub
Release.

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

The next planned release is **v0.12.0** under #714, after #739 reaches
`main` and the exact main build is green.
