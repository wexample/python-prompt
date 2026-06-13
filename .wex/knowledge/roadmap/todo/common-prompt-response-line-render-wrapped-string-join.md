# _render_wrapped uses string += accumulation instead of list+join

**Source**: `packages/prompt/src/wexample_prompt/common/prompt_response_line.py:99`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: perf

## Symptom
`current_line += rendered` inside `_render_wrapped` performs quadratic string concatenation; `current_line` is reset multiple times across the loop body (lines 99, 105, 109–110, 115–116, 119–120), making a simple drop-in `join` impossible without touching ~9 lines.

## Suggested direction
Replace `current_line: str` with `current_line_parts: list[str]`, accumulate with `.append(rendered)`, and emit `''.join(current_line_parts)` at each flush point; reset with `current_line_parts = []`.
