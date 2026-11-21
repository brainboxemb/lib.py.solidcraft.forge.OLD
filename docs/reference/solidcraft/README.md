# SolidCraft version references

Forge keeps immutable reference directories for accepted SolidCraft targets.

The currently retained canonical snapshot is:

```text
docs/reference/solidcraft/
  0.42.0/
```

[0.42.0](0.42.0/SOURCE.md) remains the last retained canonical reference.

The former `0.43.0/` tree was removed by #617 because it was a hand-authored
focused migration subset rather than a complete version reference.

#619 owns creation of the next canonical 0.45 reference after the qualified
immutable runtime is released. #621 separately owns the reusable completeness
and capture-policy checks.

The repository-level development procedure is documented in
[../../development.md](../../development.md).
