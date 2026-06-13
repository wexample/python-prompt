# _get_response_class_for_method: linear scan over response types on every call

**Source**: `packages/prompt/src/wexample_prompt/mixins/with_io_methods.py:70`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: perf

## Symptom
Every call to `_get_response_class_for_method` iterates the full `IoManager.get_response_types()` list, invoking `get_snake_short_class_name()` on each entry until a match is found. If the list grows or the method is called on every `__getattr__` lookup, this becomes an O(n) scan per attribute access.

## Suggested direction
Build a `{short_name: response_class}` dict cached at `IoManager` class level (e.g. via `functools.lru_cache` on `get_response_types` or a lazily-built class-level dict) so lookups become O(1); profile first to confirm this path is actually hot before adding complexity.
