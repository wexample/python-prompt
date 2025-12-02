#!/usr/bin/env python
"""Test script to verify prefix and symbol order."""

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.example.helpers.nesting_demo_classes import ChildTask

# Create IO manager
io = IoManager()

# Create child task with prefix
child = ChildTask(io=io)

# Test with warning (has symbol ⚠)
print("Testing warning with prefix=True:")
child.warning(message="Child task started", prefix=True)

print("\nExpected: [child] ⚠ Child task started")
print("If it shows: ⚠ [child] Child task started - WRONG ORDER")

# Also test using _output_message
print("\n\nTesting _output_message with prefix=True:")
child._output_message("warning", "Test message", prefix=True)
