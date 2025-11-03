from __future__ import annotations

from time import sleep

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class ScreenExample(AbstractResponseExample):
    def example_class(self):
        from wexample_prompt.responses.interactive.screen_prompt_response import (
            ScreenPromptResponse,
        )

        counter = {"n": 0}
        total = 10

        def _callback(response: ScreenPromptResponse):
            response.clear()
            response.print(f"Test screen iteration {counter['n']}/{total}")
            sleep(0.05)
            counter["n"] += 1
            if counter["n"] > total:
                response.close()
            else:
                response.reload()

        return ScreenPromptResponse.create_screen(
            callback=_callback,
            height=5,
        )

    def example_extended(self) -> None:
        counter = {"n": 0}
        total = 10

        def _callback(response):
            response.clear()
            response.print(f"Test screen (extended) {counter['n']}/{total}")
            sleep(0.05)
            counter["n"] += 1
            if counter["n"] > total:
                response.close()
            else:
                response.reload()

        self._class_with_methods.screen(callback=_callback, height=5)

    def example_manager(self) -> None:
        counter = {"n": 0}
        total = 10

        def _callback(response):
            response.clear()
            response.print(f"Test screen (manager) {counter['n']}/{total}")
            sleep(0.05)
            counter["n"] += 1
            if counter["n"] > total:
                response.close()
            else:
                response.reload()

        self.io.screen(callback=_callback, height=5)
