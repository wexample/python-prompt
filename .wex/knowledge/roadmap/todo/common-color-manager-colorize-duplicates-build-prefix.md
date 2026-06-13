# colorize duplicates build_prefix prefix-building logic

**Source**: `packages/prompt/src/wexample_prompt/common/color_manager.py:55`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: perf

## Symptom
`colorize` (lines 55–63) manually rebuilds the ANSI prefix with the same `if color / if bg / if styles` block that `build_prefix` already implements, meaning future changes to prefix logic must be mirrored in two places.

## Suggested direction
Have `colorize` delegate prefix construction to `build_prefix`, then append the legacy `style` argument separately, eliminating the duplication in one call.
