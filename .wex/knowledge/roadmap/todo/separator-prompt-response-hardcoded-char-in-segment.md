# SeparatorPromptResponse.create_separator hardcodes "-" in segment instead of using character param

**Source**: `packages/prompt/src/wexample_prompt/responses/titles/separator_prompt_response.py:84`
**Agent**: agent:performance
**Bucket**: inconsistency
**Severity**: inconsistency

## Symptom
`create_separator` always constructs the `PromptResponseSegment` with `text="-"` regardless of
the `character` argument (line 84). The correct character only reaches the segment at render time
(line 140: `separator_segment.text = length * character`), so the segment carries a stale
placeholder until `render` is called.

## Suggested direction
Pass `character or cls.DEFAULT_CHARACTER` as the `text` argument when constructing
`separator_response_segment` in `create_separator`, making the segment's initial state consistent
with the caller's intent.
