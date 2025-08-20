from typing import TYPE_CHECKING, Type, Optional, Union, List

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class EchoPromptResponse(AbstractPromptResponse):
    """A basic response with no style"""

    @classmethod
    def create_echo(
            cls: "EchoPromptResponse",
            message: Union[str, List[str]],
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "EchoPromptResponse":
        from wexample_prompt.common.prompt_response_line import PromptResponseLine

        return cls(
            lines=PromptResponseLine.create_from_string(
                text=message,
            ),
            verbosity=verbosity
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.echo_example import EchoExample
        return EchoExample

    def render(self, context: Optional["PromptContext"] = None) -> Optional[str]:
        # No style on echo.
        from wexample_prompt.common.prompt_context import PromptContext
        context = PromptContext.create_if_none(context=context)
        context.colorized = False

        return super().render(
            context=context,
        )
