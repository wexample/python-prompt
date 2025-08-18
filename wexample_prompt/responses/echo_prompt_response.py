from typing import TYPE_CHECKING, Type

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class EchoPromptResponse(AbstractPromptResponse):
    """A basic response with no style"""

    @classmethod
    def create_echo(
            cls: "EchoPromptResponse",
            message: str,
            context: "PromptContext" = None,
    ) -> "EchoPromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.common.prompt_response_line import PromptResponseLine

        return cls(
            lines=[
                PromptResponseLine.create_from_string(
                    text=message,
                    color=TerminalColor.WHITE
                )
            ],
            context=context
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.echo_example import EchoExample
        return EchoExample
