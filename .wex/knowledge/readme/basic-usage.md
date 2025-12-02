## Prompt IO Quickstart

### WithIoManager: owning or sharing the IoManager
- Any class that needs prompt output should inherit `WithIoManager`.
- Call `self.ensure_io_manager()` to lazily create or reuse an `IoManager`.
- To inherit a parent’s indentation/verbosity, call `self.set_parent_io_handler(parent)`; every context you create is automatically nested +1.
- If someone else instantiates the manager, call `self.use_io_manager(io)` to reuse it instead of creating a new instance.

### WithIoMethods: direct method proxies
- Mix in `WithIoMethods` when you want to call `self.log(...)`, `self.separator(...)`, etc., without reaching into `self.io`.
- The mixin delegates missing attribute lookups to the underlying `IoManager`, and it automatically injects `context=self.create_io_context()` so nested logging just works.

### Typical pattern
```python
from wexample_prompt.mixins.with_io_methods import WithIoMethods

class Worker(WithIoMethods):
    def __attrs_post_init__(self):
        self.ensure_io_manager()          # Owns an IoManager

    def run(self):
        self.log("top level message")     # via WithIoMethods

class Child(WithIoMethods):
    def __attrs_post_init__(self, parent):
        self.set_parent_io_handler(parent)  # reuse & indent

    def run(self):
        self.log("nested message")
```

The executor or parent decides whether to create a fresh manager or cascade an existing one; children only call `ensure_io_manager()` and never worry about the init order.
