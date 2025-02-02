from typing import ClassVar, Type, TYPE_CHECKING, Optional

from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.enums.message_type import MessageType
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample
    from wexample_prompt.enums.terminal_color import TerminalColor


class SuccessPromptResponse(BaseMessageResponse):
    """Response for success messages."""
    
    SYMBOL: ClassVar[str] = "✅"
    
    @classmethod
    def create_success(
        cls: "SuccessPromptResponse",
        message: str,
        context: "PromptContext" = None,
        color: Optional["TerminalColor"] = None,
        **kwargs
    ) -> "AbstractPromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor

        return cls._create_symbol_message(
            text=message,
            context=context,
            color=color or TerminalColor.GREEN
        )

    @classmethod
    def get_message_type(cls) -> "MessageType":
        from wexample_prompt.enums.message_type import MessageType

        return MessageType.SUCCESS

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        """Get the example class for success messages."""
        from wexample_prompt.example.response.messages.success_example import SuccessExample
        return SuccessExample
