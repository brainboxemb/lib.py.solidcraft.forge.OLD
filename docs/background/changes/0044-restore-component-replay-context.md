# 0044 — restore component context across replay checkpoints

Status: **implemented**
Issue: **#753**
SolidCraft target: **0.48.1**

## Problem

Forge headless replay splits a command document whenever a later command needs a
newly bound SolidCraft result. Each phase runs in a fresh `solidcraft-cli`
process and reopens the previous `.sc` checkpoint.

The transport already restores an unfinished Sketch because the saved design
does not preserve the CLI session's active-Sketch flag. It did not restore the
active reusable component.

That gap is observable with the minimal timing reproducer:

1. create one component and one Box;
2. save/reopen;
3. add one joined Cylinder to the component body;
4. copy/move five component occurrences.

The boolean body result is correct, but the Cylinder feature/tool is rendered in
root/world context for every occurrence. The same commands are clean when the
Cylinder is authored before the first save.

## Fix

Headless replay now tracks active component state alongside active Sketch state.

At every new replay phase Forge restores transport context in this order:

1. `component.activate` for a non-root active component;
2. `sketch.edit` when an unfinished Sketch is also active;
3. the authored replay commands.

These restore commands are transport-only. They are excluded from authored
result alignment and replay logs exactly like the existing Sketch restore.

`component.create`, `component.activate` and `file.new` update the tracked
component context. Activating `root` clears the component restore requirement.

## Verification

Unit tests cover:

- restoring a component before a new phase;
- component restore before Sketch restore;
- component create/activate state transitions;
- invalid component identities.

The retained #753 HUB75-history fixture remains the model-level regression:
five copied/rotated occurrences with component-local joined Cylinders must
render without detached world-space feature/tool islands on the qualified
SolidCraft runtime.
