"""Response for displaying and handling choice prompts."""
from typing import Any, List, Optional

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import InquirerPyDefault

from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle


class ChoicePromptResponse(BasePromptResponse):
    """Response for displaying a list of choices and getting user selection."""

    @classmethod
    def create(
        cls,
        question: str,
        choices: List[Any],
        default: Optional[InquirerPyDefault] = None,
        abort: Optional[str] = "> Abort",
        **kwargs: Any
    ) -> 'ChoicePromptResponse':
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
            
        response = cls(lines=lines)
        response._choices = choices_all
        response._default = default
        response._kwargs = kwargs
        return response
        
    def execute(self) -> Any:
        """Execute the choice prompt and get user selection.
        
        Returns:
            Any: The selected choice value
        """
        return inquirer.select(
            message=self.lines[0].render(),  # Use the question as message
            choices=self._choices,
            default=self._default,
            **self._kwargs
        ).execute()
