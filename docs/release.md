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

Latest actual Forge release: **v0.14.0**.

- annotated tag: `v0.14.0`;
- annotated tag object:
  `71464de5f5290a29b2b235ecf065b8bab35ad2c0`;
- exact source:
  `cd46d6797df319b9d13605c11568990113772700`;
- published GitHub Release: `v0.14.0`;
- qualified runtime: `docker.cad.solidcraft v0.3.5`;
- qualified SolidCraft: `0.48.1`;
- canonical SolidCraft registry: 866 commands under
  `docs/reference/solidcraft/0.48.1/`;
- exact main branch build: `45381336046`;
- central release run: `45381885774`.

The annotated tag resolves exactly to the release source above.

v0.14.0 is the first Forge release carrying:

- canonical `model.yml.purpose` classification for curated Examples and the
  broader Verification catalog (#785);
- immutable runtime v0.3.5 / SolidCraft 0.48.1 adoption with the retained
  component-local joined-Cylinder occurrence regression (#753/#823);
- first-class Sheet metal API Guide/Reference/Cheatsheet documentation (#786).

v0.14.0 remains a valid immutable runtime/catalog baseline, but later product
qualification in CAD #388 proved that it did **not** fix the real HUB75
five-panel save/reopen replay-context defect. Do not cite v0.14.0 as the #753
product fix; that Forge replay fix first ships in the v0.15.0 candidate below.

### Previous v0.13.2 baseline

v0.13.2 remains valid and immutable at exact source
`ea5710a5d2d33b0633b93c5da95dd5b74f126aa4`, qualified against SolidCraft
0.45.0. Its exact main build was `45269510406` and its central release run was
`45269991837`.

v0.13.2 was the consumer hotfix for #796 and remains part of the historical
release chain; the v0.14.0 record above does not rewrite it.

## Next release candidate

Candidate: **v0.15.0**.

The accepted post-v0.14 batch contains:

- generalized native feature-pattern sources, including applied Hole/native
  primitive seeds (#347);
- native exploded Assembly presentation without mutating assembled placements
  (#751);
- native whole-sheet `Shape.perforate(...)` manufacturing fields (#779);
- active-component restoration across headless save/reopen replay phases
  (#753).

The stable pre-release integration point is main
`b20e68b20ef5bec9c717f1e477eae064eec35a23`. Exact main durable run
`45398101329` succeeded and `build/main` source-matches that commit.

For #753, the retained Forge owner preview is visually clean on the accepted
fix, and temporary CAD #388 qualification run `45396787004` rebuilt the full
16-root consumer graph successfully on the same Forge fix without product
geometry changes. Final product-render visual acceptance remains intentionally
post-release on the normal durable CAD adoption path.

Publication must not occur until the exact v0.15.0 release-preparation commit is
stable on `main`, its durable main build is green/source-matched, and the
shared release flow accepts that exact SHA.

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

Forge v0.15.0 release preparation is active under #836. Validate and merge the
release-metadata PR to `main`, require exact durable main provenance, then
publish only through the shared `/release v0.15.0 <exact-sha>` flow. After
publication, downstream CAD adopts the immutable release and performs the final
durable five-panel render acceptance for #753/#388.
