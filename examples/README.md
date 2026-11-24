# Forge examples

The `examples/` tree contains several deliberately different repository roles.

A model that participates in a public catalog owns canonical `model.yml`
metadata. Catalog membership is explicit in that file:

```yaml
purpose: example
purpose: verification
purpose: [example, verification]
```

The source directory does not define the public role. A current model may own:

```text
examples/<slug>/
  ci.yml
  model.yml
  README.md
  scpf/model.py
  verification/verify.py
  build123d/{ci.yml,model.py}      # optional independent evidence
  cadquery/{ci.yml,model.py}       # optional independent evidence
  pybosl2/{ci.yml,model.py}        # optional independent evidence
  pythonscad/{ci.yml,model.py}     # optional independent evidence
```

Examples and Verification are discovered independently from `model.yml.purpose`;
there is no central executable model-case registry and no separate
`catalog.yml`.

A top-level directory without canonical `model.yml` may still contain
`role.yml` as repository-maintenance metadata. That file records why the
fixture exists, who owns it and the current keep/promote/retire decision. It is
not the Example/Verification membership interface.

Supported exception roles are:

- `release-verification` — fixture owned by Forge package release verification;
- `regression-fixture` — focused source fixture whose behavior is owned by a
  current executing test outside the full model-verification catalog. This also
  covers deliberately non-native Q1/Q2 fixtures such as `model_authoring`.

Temporary migration candidates and unowned legacy samples are not permanent
roles. They must be promoted, explicitly superseded, or retired before the
reconciliation issue closes.

The historical lineage of the current 32-case catalog and every current
exception is recorded in `docs/background/example-history.md`.

Do not create a new public model without canonical `model.yml.purpose`.
Focused non-public fixtures may use an explicit local repository role.
