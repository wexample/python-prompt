#!/usr/bin/env python3
from typing import cast

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if __name__ == "__main__":
    all_response_types = IoManager.get_response_types()
    for all_response_type in all_response_types:
        all_response_types = cast(AbstractPromptResponse, all_response_types)

        example = (all_response_type.get_example_class())()
        example_response = example.example_class()
        example.io.print_response(example_response)

        example_response = example.example_class(indentation=1)
        example.io.print_response(example_response)

        example.example_manager()
        example.example_context()
