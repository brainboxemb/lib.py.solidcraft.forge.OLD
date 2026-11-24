# Forge Verification

Forge Verification is independent from the small public teaching Examples
catalog.

Repository roles:

```text
verification/cases/<slug>/
    public capability Verification cases

verification/regressions/<slug>/
    non-public regression/release fixtures

verification/diagrams/
verification/tests/
    shared Forge-owned verification presentation/tests
```

A public case owns its model-specific source, contract tests and verification
expectations in one case root. Its slug is public identity; its repository path
is source location. Site/evidence code must therefore use the discovered source
path rather than assuming `examples/<slug>`.

The Verification overview groups public cases by the `section` declared in
their local `model.yml`. Sheet-metal capabilities use the first-class
`sheet-metal` section.

Teaching examples may also participate in Verification, but only when their
local `examples/<slug>/catalog.yml` explicitly sets
`public_verification: true`.

Adding a Verification case must not change the public Example count.
Adding a teaching Example must not silently create a Verification case.
