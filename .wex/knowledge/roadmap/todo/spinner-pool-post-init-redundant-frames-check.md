# Redundant `if not self.frames` guard after `list(... or DEFAULT_SPINNER_FRAMES)`

**Source**: `packages/prompt/src/wexample_prompt/common/spinner_pool.py:43`
**Agent**: agent:performance
**Bucket**: redundant-check
**Severity**: perf

## Symptom
In `Spinner.__attrs_post_init__`, line 42 sets `self.frames = list(self.frames or DEFAULT_SPINNER_FRAMES)`.
Lines 43-44 then check `if not self.frames:` and reassign — but this branch can only be reached if
`DEFAULT_SPINNER_FRAMES` itself is empty, which would be a bug elsewhere, not a valid runtime path.

## Suggested direction
Verify that `DEFAULT_SPINNER_FRAMES` is always non-empty (check `const/spinners.py`), then drop the
redundant guard so `__attrs_post_init__` makes only one assignment.
