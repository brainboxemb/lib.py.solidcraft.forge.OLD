# Forge release

This document describes the repository's current package-release contract.

## Version sources

The SCPF package version is defined in `scpf/pyproject.toml`.

SolidCraft compatibility is defined separately in
`scpf/scpf/version.py::TESTED_SOLIDCRAFT_VERSION`.

A package-version change and a tested-SolidCraft-version change are different
decisions and must not be coupled accidentally.

## Current release state

The latest **actual** Forge GitHub Release is `v0.10.0`.

Current source preparation is ahead of that release:

- `scpf/pyproject.toml` currently carries package version `0.11.0`;
- post-0.10 user-visible work remains under `## [Unreleased]` in
  `CHANGELOG.md`;
- Forge is qualified against SolidCraft `0.45.0` / runtime `v0.3.4`.

A package version in source or a dated changelog heading is **not** proof that a
Forge release exists.

The active Forge workflow `.github/workflows/scpf.yml` delegates execution to
released `tool.cad.ci`. It verifies source/model/integration work and maintains
durable build/Page scopes. It does **not** create a Forge Git tag or GitHub
Release.

Issue #366 is complete. Generated Pages publication is already live and is not a
release blocker.

The next intended package release is tracked by #642: **Forge v0.11.0**.

## Release blockers

The active foundational blocker list is:

```text
docs/background/design/release-blockers.txt
```

Blank/comment-only content means there is no active foundational blocker.

The release candidate must also satisfy any explicit gate recorded in the
current repository plan and release issue. A release must not be published from
an arbitrary source revision merely because the blocker file is empty.

## Development changelog

User-visible changes remain under `## [Unreleased]` until an intentional
release candidate is chosen.

Do not create a dated release section early. Doing so previously made 0.11.0
look released when no tag or GitHub Release existed.

## Release-candidate verification

The exact intended release source must be a green `main` revision.

At minimum, verify:

1. the normal Forge/CAD-CI source and model checks;
2. durable `build/main` integration;
3. stable generated Pages publication;
4. `ci/forge-release/ci.yml` / `forge-release` representative package
   verification;
5. no active entry in
   `docs/background/design/release-blockers.txt`;
6. package metadata and tested SolidCraft version match the intended release
   contract.

Release verification proves that one source revision is eligible for
publication. It does not publish the release.

## Publishing a Forge release

Publication is an explicit repository-owner operation. It is not triggered by
a successful CAD-CI run.

The owner command is:

```text
/release vX.Y.Z <exact-40-character-main-sha>
```

The command is posted on the release tracking issue after the release-
preparation PR has merged and durable main integration is complete.

For an intentional release such as #642 / v0.11.0:

1. choose the exact green `main` SHA to release;
2. reconcile `CHANGELOG.md`:
   - move only actually shipped entries from `[Unreleased]` into
     `[0.11.0] - YYYY-MM-DD`;
   - leave deferred work under a fresh `[Unreleased]` section;
3. verify `scpf/pyproject.toml` contains exactly `0.11.0`;
4. require durable `build/main`, its `forge-release` evidence and stable
   Pages provenance to resolve to that exact SHA;
5. post `/release v0.11.0 <sha>` on #642;
6. the owner-only release workflow validates metadata/evidence, creates or
   verifies the annotated tag, and creates the GitHub Release from the dated
   changelog section;
7. verify both tag and GitHub Release resolve to the intended commit;
8. update `docs/plan.md` with the released baseline before starting another
   large development wave.

The workflow may repair the narrow case where the correct annotated tag already
exists at the validated SHA but the GitHub Release is missing. It never moves a
conflicting tag.

A release is complete only after tag and GitHub Release are proven. Source
metadata, a changelog heading, a commit named “release” or a green verification
run alone is release preparation.

## Related primary documents

- [API](api.md)
- [Design](design.md)
- [Development](development.md)
- [Plan](plan.md)
- [Requirements](requirements.md)
