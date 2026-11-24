# Native exploded assembly views

> Documentation provenance: Forge #751 publishes native SolidCraft exploded assembly presentation as public Verification. Machine verification lives in [`verification/verify.py`](verification/verify.py).

## Goal

Qualify SolidCraft exploded views as persistent presentation state on a real
Forge component/occurrence assembly.

## Forge API

```python
assembly = first + second + third
assembly = assembly.with_exploded_view("Automatic", scale=1.25)
assembly = assembly.with_exploded_view(
    "Instructions",
    moves=[
        (second, (0, 25, 0)),
        (third, (0, 50, 10)),
    ],
)
assembly = assembly.show_assembled()
```

## Native lowering

Forge establishes normal component occurrences and placements first. It then
emits two native `explode.create` commands. Explicit moves reference the
actual occurrence ids bound by `component.create` / `occurrence.copy`.
Finally `explode.show(view=None)` selects assembled presentation.

No exploded translation is lowered as `occurrence.move`.

## Saved-design proof

The saved design is reopened and asked to show each stored exploded view. The
commands must succeed without rerunning Python. A second command returns the
explicit view to assembled presentation. Model verification continues to see
the original occurrence placements because exploded state is presentation only.
