from typing import Optional, ClassVar

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
            symbol: Optional[str] = None,
            **kwargs
    ) -> 'AbstractMessageResponse':
        """Create a message with a symbol"""
        # Determine effective symbol (explicit > class default)
        effective_symbol = symbol if symbol is not None else cls.SYMBOL

        segments: list[PromptResponseSegment] = []

        # Add symbol if non-empty
        if effective_symbol:
            symbol_text = f"{effective_symbol} "
            segments.append(
                PromptResponseSegment(
                    text=symbol_text,
                    color=color
                )
            )

        # Add message text
        segments.append(
            PromptResponseSegment(
                text=text,
                color=color
            )
        )

        # Create response with context and additional kwargs
        return cls._create(lines=[
            PromptResponseLine(segments=segments)
        ], **kwargs)
