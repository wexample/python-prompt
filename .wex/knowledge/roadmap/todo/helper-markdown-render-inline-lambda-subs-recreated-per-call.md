# _render_inline lambda sub callables recreated on every call

**Source**: `packages/prompt/src/wexample_prompt/helper/markdown.py:146`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: perf

## Symptom
`_render_inline` defines five inline lambdas (`_BOLD`, `_ITALIC`, `_BOLD_UNDERSCORE`, `_ITALIC_UNDERSCORE`, `_STRIKE` subs) as anonymous functions on every invocation. The same two lambdas (bold, italic) are duplicated a second time in `_link_sub`, so each hyperlink call creates two more short-lived closures.

## Suggested direction
Hoist the five sub callables to module-level named functions (like the existing `_code_sub`, `_image_sub`, `_link_sub`); reference them directly in `_render_inline` and `_link_sub` to eliminate per-call object creation and remove the duplication.
