"""Response for displaying and handling dictionary-based choice prompts."""
from typing import Any, Dict, Optional

from wexample_prompt.responses.choice_prompt_response import ChoicePromptResponse


class ChoiceDictPromptResponse(ChoicePromptResponse):
    """Response for displaying choices from a dictionary and returning the selected key."""

    @classmethod
    def create(
        cls,
        question: str,
        choices: Dict[str, str],
        default: Optional[str] = None,
        abort: Optional[str] = "> Abort",
        **kwargs: Any
    ) -> 'ChoiceDictPromptResponse':
        """Create a dictionary-based choice prompt response.
        
        Args:
            question: The question to display
            choices: Dictionary of choices (key: internal value, value: display text)
            default: Optional default key
            abort: Optional abort choice text (None to disable)
            **kwargs: Additional arguments for inquirer.select
            
        Returns:
            ChoiceDictPromptResponse: A new dictionary choice prompt response
        """
        # Store original choices for key lookup
        response = super().create(
            question=question,
            choices=list(choices.values()),
            default=choices.get(default) if default else None,
            abort=abort,
            **kwargs
        )
        response._original_choices = choices
        return response
        
    def execute(self) -> Optional[str]:
        """Execute the choice prompt and get selected key.
        
        Returns:
            str: The key of the selected choice, or None if aborted
        """
        selected_value = super().execute()
        if selected_value is None:
            return None
            
        # Find the key corresponding to the selected value
        return next(
            (key for key, value in self._original_choices.items() 
             if value == selected_value),
            None
        )
