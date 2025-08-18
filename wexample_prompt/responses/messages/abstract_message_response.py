from typing import Optional, ClassVar, Tuple

from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class AbstractMessageResponse(AbstractPromptResponse):
    # Symbol to display before the message, override in subclasses
    SYMBOL: ClassVar[str] = ""

    @classmethod
    def _create_symbol_message(
            cls,
            text: str,
            color: TerminalColor,
            symbol: Optional[Tuple[str, False]] = None,
            bold_symbol: bool = True,
            context: Optional[PromptContext] = None,
            **kwargs
    ) -> 'AbstractMessageResponse':
        """Create a message with a symbol"""
        segments = []

        # Add symbol if present
        if symbol or (symbol is None and cls.SYMBOL):
            symbol_text = f"{symbol or cls.SYMBOL} "
            symbol_segment = PromptResponseSegment(
                text=ColorManager.colorize(
                    symbol_text,
                    color,
                    TerminalColor.BOLD if bold_symbol else None
                )
            )
            segments.append(symbol_segment)

        # Add message text
        message = PromptResponseSegment(
            text=ColorManager.colorize(text, color)
        )
        segments.append(message)

        # Create line with segments
        line = PromptResponseLine(
            segments=segments,
        )

        # Create response with context and additional kwargs
        create_args = {"lines": [line]}
        create_args.update(kwargs)

        return cls._create(**create_args)
