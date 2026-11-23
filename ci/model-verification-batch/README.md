# model-verification-batch

Repository-level producer for native SolidCraft verification of the active
Forge model catalog.

## Purpose

Starting a SolidCraft runtime separately for every model is unnecessarily
expensive. This item runs the active declarative Forge model verification set
in one shared immutable SolidCraft runtime and writes per-model results below
its `items/` output.

Individual `examples/<model>/ci.yml` items remain the public model items and
copy only their own result from this producer.

## Contract

- **Item id:** `model-verification-batch`
- **Kind:** `verification`
- **Dependencies:** `forge-package`, `cad-verification-package`
- **Entry point:** [`scripts/model_verification_batch.py`](../../scripts/model_verification_batch.py)
- **Per-model launcher:** [`scripts/model_verify_declarative.py`](../../scripts/model_verify_declarative.py)
- **Visual adapter:** [`scripts/model_visual.py`](../../scripts/model_visual.py)
- **Output:** `items/`

Forge owns model definitions and model-specific expectations. Generic
verification mechanics stay in the released `lib.py.cad.verification`
dependency. Generic selection/scheduling stays in CAD-CI.

See the repository-level [CI map](../README.md).

## Selection context

The `verify_models` command opts into released CAD-CI
`selection_context: direct_dependents`.

CAD-CI derives the already-active direct model consumers from the SCons graph
and supplies their item ids through `CAD_CI_ACTIVE_DEPENDENTS_JSON`. The
Forge batch validates those ids against its existing processed declarative
models and puts only that ordered subset into the SolidCraft runtime manifest.

Forge does **not** run its own Git/path selector. A full CAD-CI run naturally
supplies the complete processed model set; an empty direct-dependent set starts
no SolidCraft container.

The exact list is part of the generic CAD-CI target signature/cache identity
and public step evidence. That behavior is owned by released
`lib.py.cad.ci 0.11.0` / `tool.cad.ci 0.18.1`.
