# _strip_ansi: hoist compiled regex to class constant

**Source**: `packages/prompt/src/wexample_prompt/responses/data/table_prompt_response.py:152`
**Agent**: agent:performance
**Bucket**: hoist
**Severity**: perf

## Symptom
`re.compile(r"...")` is called inside `_strip_ansi` on every invocation. Python's internal re cache avoids recompilation but still pays a dict-lookup on each call; `_strip_ansi` sits in a tight double-loop (one call per segment per cell per row).

## Suggested direction
Hoist the compiled pattern to a class-level constant (e.g. `_ANSI_RE`); requires moving `import re` to module scope, which is outside this agent's import-freeze rule and must be done in a dedicated pass.
