# Duplicate parent.update call in RangeProgressHandle.update

**Source**: `packages/prompt/src/wexample_prompt/common/progress/range_progress_handle.py:67`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: style

## Symptom
`update()` has two separate `return self.parent.update(...)` branches (lines 67-69 and 72-74) that differ only in the `current` argument. The `else` branch repeats the full keyword-argument list, creating a maintenance hazard if new parameters are added.

## Suggested direction
Compute `mapped` (or `None`) before the `if`, then issue a single `self.parent.update(current=mapped, ...)` call; the lazy import can stay inside the `if` block unchanged.
