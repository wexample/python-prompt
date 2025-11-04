#!/usr/bin/env python
"""Test script to verify prefix and symbol order in full nesting scenario."""

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

# Create IO manager
io = IoManager()

# Create parent task
parent = ParentTask(io=io)

# Execute with warning (has symbol ⚠)
print("=== Testing with warning (symbol: ⚠) ===\n")
parent.execute(method_name="warning")

print("\n\n=== Testing with subtitle (symbol: ❯) ===\n")
parent2 = ParentTask(io=io)
parent2.execute(method_name="subtitle")
