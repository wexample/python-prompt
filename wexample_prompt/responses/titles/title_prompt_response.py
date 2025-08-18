from typing import Type, Optional, TYPE_CHECKING

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.titles.abstract_title_response import AbstractTitleResponse

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor


class TitlePromptResponse(AbstractTitleResponse):
    """Main title: "❯ <text> -----"""

    @classmethod
    def create_title(
            cls: "TitlePromptResponse",
            text: str,
            color: Optional["TerminalColor"] = None,
            character: Optional[str] = None,
            width: Optional[int] = None,
    ) -> "TitlePromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor

        return super()._create_title(
            text=text,
            color=color or TerminalColor.BLUE,
            character=character,
            width=width,
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.titles.title_example import TitleExample
        return TitleExample
