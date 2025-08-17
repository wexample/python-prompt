from typing import List, Type, TYPE_CHECKING, Optional

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.mixins.response.manager.messages.log_prompt_response_manager_mixin import \
    LogPromptResponseManagerMixin
from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class IoManager(
    ExtendedBaseModel,
    # Messages
    LogPromptResponseManagerMixin,
):
    output: Optional[AbstractOutputHandler] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_output()

    def _init_output(self):
        from wexample_prompt.output.strout_output_handler import StdoutOutputHandler
        self.output = self.output if (self.output is not None) else StdoutOutputHandler()

    @classmethod
    def get_response_types(cls) -> List[Type["AbstractPromptResponse"]]:
        from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse

        return [
            # Messages
            LogPromptResponse,
        ]

    def print_response(self, response: "AbstractPromptResponse") -> None:
        self.output.print(response)

