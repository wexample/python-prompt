from typing import TYPE_CHECKING, Optional, List, Dict, Any

from InquirerPy.base.control import Choice
from InquirerPy.utils import InquirerPyDefault

if TYPE_CHECKING:
    from wexample_prompt.responses.interactive import ChoicePromptResponse


class ChoicePromptResponseManagerMixin:
    def choice(
        self,
        question: str,
        choices: List[Any],
        default: Optional[InquirerPyDefault] = None,
        abort: Optional[str] = "> Abort",
        **kwargs
    ) -> "ChoicePromptResponse":
        from wexample_prompt.responses.interactive import ChoicePromptResponse

        response = ChoicePromptResponse.create_choice(
            question=question,
            choices=choices,
            context=self.create_context(),
            default=default,
            abort=abort,
            **kwargs
        )

        self.print_response(response)
        return response

    def choice_dict(
        self,
        question: str,
        choices: Dict[str, str],
        default: Optional[str] = None,
        abort: Optional[str] = "> Abort",
        **kwargs
    ) -> str:
        from wexample_prompt.responses.interactive import ChoiceDictPromptResponse

        response = ChoiceDictPromptResponse.create_choice_dict(
            question=question,
            choices=choices,
            context=self.create_context(),
            default=default,
            abort=abort,
            **kwargs
        )

        self.print_response(response)
        return response.execute()
