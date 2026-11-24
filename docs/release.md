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

Latest actual Forge release: **v0.15.0**.

- annotated tag: `v0.15.0`;
- annotated tag object:
  `1aa6304b412269163cffe19045cdd4b13b1f7e74`;
- exact source:
  `efc88bfcaf452051d721347f2e5ca561decad654`;
- published GitHub Release: `v0.15.0`;
- qualified runtime: `docker.cad.solidcraft v0.3.5`;
- qualified SolidCraft: `0.48.1`;
- canonical SolidCraft registry: 866 commands under
  `docs/reference/solidcraft/0.48.1/`;
- exact main branch build: `45399136016`;
- central release run: `45399592693`.

The annotated tag resolves exactly to the release source above.

v0.15.0 ships the accepted post-v0.14 CAD/API batch:

- generalized native feature-pattern sources, including applied Hole/native
  primitive seeds (#347);
- native exploded Assembly presentation without mutating assembled placements
  (#751);
- native whole-sheet `Shape.perforate(...)` manufacturing fields (#779);
- active-component restoration across headless save/reopen replay phases
  (#753).

The #753 fix has also passed final released-source product acceptance. CAD #388
adopted exact v0.15.0 without geometry/runtime changes as
`0d3081a1b76148854d82e2bf0e1593571fb7fb60`; durable run
`45400699265` succeeded. The exact durable `hub75-screen` render blob
`ae6ce9178ba354ac67899044814bfb1ff91661b2` was visually inspected and
contains the five intended panel occurrences with no detached component-local
Cylinder/tool geometry.

### Previous v0.14.0 baseline

v0.14.0 remains valid and immutable at exact source
`cd46d6797df319b9d13605c11568990113772700`, qualified against immutable
runtime v0.3.5 / SolidCraft 0.48.1. Its exact main build was
`45381336046` and central release run was `45381885774`.

v0.14.0 established the 0.48.1 runtime/catalog baseline, but later CAD #388
proved it did not fix the real save/reopen replay-context presentation defect.
That Forge fix first ships in v0.15.0.

### Previous v0.13.2 baseline

v0.13.2 remains valid and immutable at exact source
`ea5710a5d2d33b0633b93c5da95dd5b74f126aa4`, qualified against SolidCraft
0.45.0. Its exact main build was `45269510406` and its central release run was
`45269991837`.

v0.13.2 was the consumer hotfix for #796 and remains part of the historical
release chain.

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

v0.15.0 is the recommended released Forge baseline for current CAD consumers
that need #347 pattern sources, #751 exploded views, #779 sheet perforation or
the #753 replay-context fix. Resume normal Forge backlog work; release mechanics
remain unchanged.
