# _render_wrapped uses list.pop(0) (O(n)) instead of deque.popleft() (O(1))

**Source**: `packages/prompt/src/wexample_prompt/common/prompt_response_line.py:102`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: perf

## Symptom
`queue.pop(0)` on a plain list shifts all remaining elements left on every iteration; for lines with many segments this degrades to O(n²).

## Suggested direction
Replace `queue = list(self.segments)` with `queue = collections.deque(self.segments)` and `queue.pop(0)` with `queue.popleft()` — profile on a representative large-segment line to confirm the win justifies the import addition.
