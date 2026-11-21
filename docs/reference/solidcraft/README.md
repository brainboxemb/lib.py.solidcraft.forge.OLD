# SolidCraft version references

Forge keeps canonical, immutable engineering references only for SolidCraft
versions whose runtime and reference capture were actually qualified.

Current retained canonical snapshot:

```text
docs/reference/solidcraft/
  0.42.0/
```

[0.42.0](0.42.0/SOURCE.md) is currently the last retained canonical snapshot.

The previously checked-in `0.43.0/` tree was removed by #617 because it was a
small hand-authored Forge migration slice presented under a path that implied a
complete version snapshot. It must not be used as reference evidence.

Issue #619 owns the next canonical snapshot for the selected current runtime.
It must not be created until the runtime owner publishes the qualified immutable
release.

## What counts as a canonical version reference

A directory named `docs/reference/solidcraft/<version>/` is an engineering
source of truth, not a notes folder.

It must be derived from the exact qualified immutable runtime and include:

1. `SOURCE.md` with:
   - exact upstream release tag;
   - exact upstream commit;
   - exact immutable owner-runtime release used for capture;
2. the **complete** command registry from the actual
   `solidcraft-cli commands` of that runtime;
3. a reproducible human-readable command catalog generated from that complete
   registry or the exact upstream generation path;
4. machine-readable command/contract evidence where the runtime exposes it;
5. version-to-version comparisons derived from those canonical inputs.

Forge-specific notes may be selective, but they must be clearly derived notes.
They never replace the complete canonical command snapshot.

A small manually selected command subset is not a valid
`docs/reference/solidcraft/<version>/` snapshot.

## Adding a new SolidCraft version

When Forge intentionally moves to a new SolidCraft release:

1. the runtime owner first selects, tests and publishes an immutable runtime;
2. run the actual released runtime and verify its exact SolidCraft version;
3. create a new sibling version directory; never modify an already accepted
   canonical directory in place;
4. record exact upstream and runtime provenance in `SOURCE.md`;
5. capture the complete runtime command registry;
6. generate the canonical human command catalog from that complete registry;
7. capture any available machine contracts and compare them with the previous
   canonical snapshot;
8. only after that evidence exists, derive Forge compatibility changes and
   update Forge's tested target.

Do not create a version directory as a placeholder or migration notebook.

The repository-level development procedure is documented in
[../../development.md](../../development.md).
