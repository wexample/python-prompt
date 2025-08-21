from typing import TYPE_CHECKING, Optional, Type

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.titles.abstract_title_response import (
    AbstractTitleResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor


class SubtitlePromptResponse(AbstractTitleResponse):
    DEFAULT_PREFIX = "  ❯"

    @classmethod
    def create_subtitle(
        cls: "SubtitlePromptResponse",
        text: str,
        color: Optional["TerminalColor"] = None,
        character: Optional[str] = None,
        width: Optional[int] = None,
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
    ) -> "SubtitlePromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor

        return super()._create_title(
            text=text,
            color=color or TerminalColor.BLUE,
            character=character,
            width=width,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.titles.subtitle_example import (
            SubtitleExample,
        )

        return SubtitleExample
