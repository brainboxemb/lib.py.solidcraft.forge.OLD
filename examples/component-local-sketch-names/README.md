# Component-local Sketch-name regression fixture

This non-public regression fixture qualifies Forge issue #679 against the pinned
SolidCraft 0.45 runtime.

## Purpose

Independent reusable component definitions may both author the same local Sketch
name:

```python
with Sketch(name="Profile", plane="XY") as sketch:
    ...
```

That local name is part of the component implementation. It must not become a
cross-component naming convention that every CAD consumer has to coordinate.

Forge assembly lowering therefore assigns deterministic document-global native
Sketch identities per component definition while preserving the authored local
name in Python.

## Model

The fixture contains two independent plate component definitions:

- `LeftPlate` with local Sketch `Profile`;
- `RightPlate` with local Sketch `Profile`.

They are placed apart in one assembly and saved in one SolidCraft design.

The native command contract must contain:

- `d1_LeftPlate__Profile`;
- `d2_RightPlate__Profile`.

No caller-authored prefix or raw SolidCraft command is used.

## Additional contract coverage

Unit/command-contract tests also exercise multiple independent definition
variants of one component class and semantic Sketch-reference rewriting. Plain
text, font, body, material and generic feature-name strings remain opaque.

## Native qualification

SolidCraft must replay and save the complete assembly without the historical
`another feature is called 'Profile'` failure and retain two separate solid
bodies at the expected placements.
