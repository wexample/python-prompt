# create_context masks explicit indentation_length=0 via `or` fallback

**Source**: `packages/prompt/src/wexample_prompt/common/io_manager.py:323`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: bug

## Symptom
`base_indentation_length = context_kwargs.get("indentation_length") or self.indentation_length`
silently discards an explicitly-passed `indentation_length=0` because `0` is falsy, falling back to `self.indentation_length` instead.

## Suggested direction
Replace with `context_kwargs.get("indentation_length") if context_kwargs.get("indentation_length") is not None else self.indentation_length`, or use a sentinel-based lookup, to preserve an intentional zero value.
