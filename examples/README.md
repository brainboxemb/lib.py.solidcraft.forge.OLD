# Forge examples

The `examples/` tree is the deliberately small public teaching catalog.

It is **not** the complete Forge Verification catalog.

The current public examples are:

- `simple-box`;
- `anchored-holes`;
- `components`;
- `corner-anchor`.

Each teaching root owns its normal model files plus a local `catalog.yml`:

```text
examples/<slug>/
  catalog.yml
  ci.yml
  model.yml
  README.md
  scpf/model.py
  verification/verify.py
  ...
```

`catalog.yml` explicitly declares whether that teaching item is public as an
Example and whether it also participates in public Verification. A new
Verification case must not become an Example merely because it has a
`model.yml`.

Public capability verification lives under:

```text
verification/cases/<slug>/
```

Non-public regression/release fixtures live under:

```text
verification/regressions/<slug>/
```

Those roots are independently discovered by CAD-CI and the Pages site.

Do not put a new public modelling capability under `examples/` unless it is
intentionally one of the small teaching examples. Normal new capabilities belong
under `verification/cases/`.

Historical catalog lineage is recorded in
`docs/background/example-history.md`.
