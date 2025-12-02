#!/usr/bin/env python
"""Test with prefix explicitly enabled to verify order."""

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.example.helpers.nesting_demo_classes import ChildTask, GrandchildTask

# Create IO manager
io = IoManager()

# Create child task with prefix
child = ChildTask(io=io)
grandchild = GrandchildTask(parent_io_handler=child)

print("=== Child with warning (prefix enabled) ===")
child._output_message("warning", "Child task started", prefix=True)

print("\n=== Grandchild with warning (prefix enabled) ===")
grandchild._output_message("warning", "Grandchild task started", prefix=True)

print("\n=== Child with subtitle (prefix enabled) ===")
child._output_message("subtitle", "Child task started", prefix=True)

print("\n=== Grandchild with subtitle (prefix enabled) ===")
grandchild._output_message("subtitle", "Grandchild task started", prefix=True)

print("\n\nExpected orders:")
print("[child] ⚠ Child task started")
print("(grandchild) ⚠ Grandchild task started")
print("[child] ❯ Child task started")
print("(grandchild) ❯ Grandchild task started")
