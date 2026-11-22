# Change 0043 — standalone Sketch extrusion Boolean operands

## Problem

A standalone `Sketch(...).extrude(...)` already compiled correctly when it was
the root body, but the ordered feature-tree Boolean dispatcher rejected the same
shape when used as the right-hand operand of `+`, `-` or `&`.

The workaround was to attach the Sketch to the target body even when the design
intent was an independent world-plane cutting/joining solid.

## Native contract

The immutable SolidCraft 0.45 command reference records
`solid.extrude.operation` as:

```text
new | join | cut | intersect | auto
```

and supports explicit `targets=[body]` for Boolean application.

## Decision

Reuse the standalone Sketch creation path and make only the extrusion
application operation-sensitive:

- root standalone extrusion -> `body_name=<name>`;
- `+` operand -> `operation=join, targets=[<name>]`;
- `-` operand -> `operation=cut, targets=[<name>]`;
- `&` operand -> `operation=intersect, targets=[<name>]`.

Do not create a temporary second body or add a combine feature.

## Compatibility

Attached Sketch extrusion remains on its existing face-attached path. Pure
primitive CSG remains on the CSG compiler. This change only closes the
standalone-Sketch composability gap.

## Evidence

Q1 compiler tests cover join, cut and intersect command lowering, including a
symmetric YZ-plane RoundedRectangle2D case matching the HUB75 rear-recess use
case from issue #354.
