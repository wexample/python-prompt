from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class CodeExample(AbstractResponseExample):
    """Example for the code response."""

    PY = 'def greet(name):\n    return f"hello, {name}!"\n\nprint(greet("world"))'
    JS = "function greet(name) {\n    return `hello, ${name}!`;\n}\n\nconsole.log(greet('world'));"
    PHP = "<?php\nfunction greet(string $name): string {\n    return \"hello, {$name}!\";\n}\necho greet('world');"

    def example_class(self):
        from wexample_prompt.responses.code_prompt_response import CodePromptResponse

        return CodePromptResponse.create_code(code=self.PY, language="python")

    def example_extended(self) -> None:
        self._class_with_methods.code(code=self.PY, language="python")

    def example_inside_frame(self) -> None:
        from wexample_prompt.responses.code_prompt_response import CodePromptResponse

        snippet = CodePromptResponse.create_code(
            code=self.PY, language="python", line_numbers=True
        )
        self.io.frame(responses=[snippet], title="greet.py")

    def example_javascript(self) -> None:
        self.io.code(code=self.JS, language="javascript")

    def example_line_numbers(self) -> None:
        self.io.code(code=self.PY, language="python", line_numbers=True)

    def example_manager(self) -> None:
        self.io.code(code=self.PY, language="python")

    def example_no_language(self) -> None:
        self.io.code(code="x = 42\nprint(x)")

    def example_php(self) -> None:
        self.io.code(code=self.PHP, language="php")

    def get_examples(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Python",
                "description": "Python snippet with language label",
                "callback": self.example_manager,
            },
            {
                "title": "JavaScript",
                "description": "JS snippet",
                "callback": self.example_javascript,
            },
            {
                "title": "PHP",
                "description": "PHP snippet",
                "callback": self.example_php,
            },
            {
                "title": "Line numbers",
                "description": "Code with line numbers",
                "callback": self.example_line_numbers,
            },
            {
                "title": "No language",
                "description": "Plain code, no header",
                "callback": self.example_no_language,
            },
            {
                "title": "Inside frame",
                "description": "Code wrapped in a frame with title",
                "callback": self.example_inside_frame,
            },
        ]
