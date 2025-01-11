"""Response for displaying and handling choice prompts."""
from typing import Any, List, Optional, Dict

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import InquirerPyDefault
from pydantic import Field

from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle


class ChoicePromptResponse(BasePromptResponse):
    """Response for displaying a list of choices and getting user selection."""

    # Instance variables
    choices: List[Any] = Field(default_factory=list)
    default: Optional[InquirerPyDefault] = None
    inquirer_kwargs: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def create_choice(
        cls,
        question: str,
        choices: List[Any],
        context: Optional[PromptContext] = None,
        default: Optional[InquirerPyDefault] = None,
        abort: Optional[str] = "> Abort",
        **kwargs: Any
    ) -> 'ChoicePromptResponse':
        """Create a choice prompt response.
        
        Args:
            question: The question to display
            choices: List of choices (strings or Choice objects)
            context: Optional prompt context for formatting
            default: Default selection
            abort: Text for abort option, None to disable
            **kwargs: Additional arguments for inquirer.select
        """
        lines = []
        
        # Add the question line with blue color and bold style
        lines.append(
            PromptResponseLine(segments=[
                PromptResponseSegment(
                    text=ColorManager.colorize(question, TerminalColor.BLUE),
                    styles=[TextStyle.BOLD]
                )
            ])
        )
        
        # Add each choice with a modern arrow and styling
        choices_all = choices.copy()
        if abort:
            choices_all.append(Choice(value=None, name=abort))
            
        for i, choice in enumerate(choices_all):
            # Handle both simple values and Choice objects
            choice_text = choice.name if isinstance(choice, Choice) else str(choice)
            
            lines.append(
                PromptResponseLine(segments=[
                    # Arrow indicator with cyan color
                    PromptResponseSegment(
                        text=ColorManager.colorize(f"  {i + 1}. → ", TerminalColor.CYAN)
                    ),
                    # Choice text with gray color and dim style
                    PromptResponseSegment(
                        text=ColorManager.colorize(choice_text, TerminalColor.GRAY),
                        styles=[TextStyle.DIM]
                    )
                ])
            )
            
        return cls(
            lines=lines,
            context=context,
            choices=choices_all,
            default=default,
            inquirer_kwargs=kwargs
        )
        
    def execute(self) -> Any:
        """Execute the choice prompt and get user selection."""
        return inquirer.select(
            message=self.lines[0].render(),
            choices=self.choices,
            default=self.default,
            **self.inquirer_kwargs
        ).execute()
