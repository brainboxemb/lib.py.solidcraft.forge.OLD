# Forge release

This document describes the repository's current package-release contract.

## Version sources

The SCPF package version is defined in `scpf/pyproject.toml`.

SolidCraft compatibility is defined separately in
`scpf/scpf/version.py::TESTED_SOLIDCRAFT_VERSION`.

A package-version change and a tested-SolidCraft-version change are different
decisions and must not be coupled accidentally.

## Current release state

The latest **actual** Forge GitHub Release is **`v0.11.0`**.

Released baseline:

- package version: `0.11.0`;
- annotated tag: `v0.11.0`;
- exact tagged source commit:
  `9258d54079981604b6dd777a4c4face897c190fe`;
- GitHub Release:
  `https://github.com/brainboxemb/lib.py.solidcraft.forge/releases/tag/v0.11.0`;
- qualified SolidCraft: `0.45.0`;
- immutable runtime: `docker.cad.solidcraft v0.3.4`.

Before publication, durable `build/main`, `ci/forge-release`,
`ci/release-policy` and stable Pages all resolved to the exact tagged source
commit.

Issue #642 is complete. The historical source-only commit that previously used
the words “Release SCPF 0.11.0” was not itself release evidence; the real
release is the immutable tag + GitHub Release above.

The current `CHANGELOG.md` keeps a fresh `## [Unreleased]` section for work
after v0.11.0.

## What counts as a release

A package version, dated changelog heading, commit message or green CI run is
not sufficient release evidence.

A Forge release is complete only when:

1. one exact green `main` SHA has matching durable build/Page evidence;
2. `forge-release` verification was produced from that exact SHA;
3. an annotated `vX.Y.Z` Git tag resolves to that SHA;
4. a GitHub Release exists for that tag.

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

Do not create a dated release section early. The v0.11.0 history demonstrated
why source preparation and actual immutable publication must remain distinct.

## Release-candidate verification

The exact intended release source must be a green `main` revision.

At minimum, verify:

1. normal Forge/CAD-CI source and model checks;
2. durable `build/main` integration;
3. stable generated Pages publication;
4. `ci/forge-release/ci.yml` / `forge-release` representative package
   verification from the exact candidate SHA;
5. `ci/release-policy` from the exact candidate SHA;
6. no active entry in
   `docs/background/design/release-blockers.txt`;
7. package metadata, dated changelog section and tested SolidCraft version
   match the intended release contract.

Release-candidate metadata such as `CHANGELOG.md` is an explicit input of
`forge-release`, so a release-preparation change cannot silently reuse
package-release evidence from an older source commit.

## Publishing a Forge release

Publication is an explicit repository-owner operation. A successful CAD-CI run
never publishes a release automatically.

The owner command is:

```text
/release vX.Y.Z <exact-40-character-main-sha>
```

Post it on the dedicated release tracking issue only after the release-
preparation PR has merged and durable main integration is complete.

The owner-only workflow is intentionally thin. It delegates validation, tag
policy and GitHub Release publication to repository code under
`scripts/release/`.

For each release:

1. choose the exact green `main` SHA;
2. reconcile `CHANGELOG.md`, moving only shipped changes into the dated
   release section and leaving a fresh `[Unreleased]`;
3. verify package metadata contains the intended version;
4. require `build/main`, `forge-release`, `release-policy` and stable
   Pages provenance to resolve to the same exact SHA;
5. post `/release vX.Y.Z <sha>` on that release issue;
6. let `scripts/release/validate_release.py` reject stale/mismatched evidence;
7. let `scripts/release/publish_release.py` create or verify the annotated
   tag and GitHub Release;
8. independently verify that tag and Release resolve to the intended commit;
9. reconcile `docs/plan.md` after publication.

The publisher may repair the narrow case where the correct annotated tag
already exists at the validated SHA but the GitHub Release is absent. It never
moves a conflicting tag.

## Next release checkpoint

The plan currently targets **v0.12.0** as the next release checkpoint after the
first coherent post-v0.11 CAD/CI batch reaches `main`.

That is a planning checkpoint only. Do not bump source metadata or create a
dated v0.12.0 changelog section until a dedicated release issue explicitly
starts that release.

## Related primary documents

- [API](api.md)
- [Design](design.md)
- [Development](development.md)
- [Plan](plan.md)
- [Requirements](requirements.md)
