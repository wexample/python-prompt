#!/usr/bin/env python3
from typing import cast

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if __name__ == "__main__":
    all_response_types = IoManager.get_response_types()
    demo_io = IoManager()

    for response_type in all_response_types:
        all_response_types = cast(AbstractPromptResponse, all_response_types)

        example = (response_type.get_example_class())()
        example_response = example.example_class()

        demo_io.separator(
            label=response_type.get_snake_short_class_name(),
            character=">"
        )

        # Print from manager
        example.example_manager()

        # Print from response
        example.io.print_response(example_response, context=PromptContext())

        # Print white
        example.io.print_response(example_response, context=PromptContext(colorized=False))

        # Print indented
        example.io.print_response(example_response, context=PromptContext(indentation=1))
