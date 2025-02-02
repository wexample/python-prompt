"""Mixin for managing choice dict prompt responses."""
from typing import Any, Dict, Optional

from wexample_prompt.responses.interactive.choice_dict_prompt_response import ChoiceDictPromptResponse


class ChoiceDictPromptResponseManagerMixin:
    """Mixin class for managing choice dict prompt responses."""

    def choice_dict(
        self,
        question: str,
        choices: Dict[str, str],
        abort: Optional[str] = "> Abort",
        **kwargs: Any
    ) -> Optional[str]:
        """Create and execute a choice dict prompt.

        Args:
            question: The question to display
            choices: Dictionary of choices where keys are values and values are display labels
            abort: Optional abort choice text
            **kwargs: Additional arguments for inquirer.select

        Returns:
            str: Selected key from choices, or None if aborted
        """
        response = ChoiceDictPromptResponse.create_choice_dict(
            question=question,
            choices=choices,
            abort=abort,
            **kwargs
        )
        return response.execute()
