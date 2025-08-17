from typing import List, Type, TYPE_CHECKING

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.mixins.response.manager.messages.log_prompt_response_manager_mixin import \
    LogPromptResponseManagerMixin

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class IoManager(
    ExtendedBaseModel,
    # Messages
    LogPromptResponseManagerMixin,
):

    @classmethod
    def get_response_types(cls) -> List[Type["AbstractPromptResponse"]]:
        from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse

        return [
            # Messages
            LogPromptResponse,
        ]

    def print_response(self, response: "AbstractPromptResponse") -> None:
        pass
