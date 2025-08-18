from typing import List, Type, TYPE_CHECKING, Optional

from pydantic import Field, PrivateAttr

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.mixins.response.echo_prompt_response_manager_mixin import \
    EchoPromptResponseManagerMixin

from wexample_prompt.mixins.response.messages.info_prompt_response_manager_mixin import \
    InfoPromptResponseManagerMixin
from wexample_prompt.mixins.response.messages.debug_prompt_response_manager_mixin import \
    DebugPromptResponseManagerMixin
from wexample_prompt.mixins.response.messages.warning_prompt_response_manager_mixin import \
    WarningPromptResponseManagerMixin
from wexample_prompt.mixins.response.messages.error_prompt_response_manager_mixin import \
    ErrorPromptResponseManagerMixin
from wexample_prompt.mixins.response.log_prompt_response_manager_mixin import \
    LogPromptResponseManagerMixin
from wexample_prompt.mixins.response.messages.success_prompt_response_manager_mixin import \
    SuccessPromptResponseManagerMixin
from wexample_prompt.mixins.response.messages.task_prompt_response_manager_mixin import \
    TaskPromptResponseManagerMixin
from wexample_prompt.mixins.response.titles.separator_prompt_response_manager_mixin import \
    SeparatorPromptResponseManagerMixin
from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
    from wexample_prompt.common.prompt_context import PromptContext


class IoManager(
    ExtendedBaseModel,
    # Basics
    EchoPromptResponseManagerMixin,
    LogPromptResponseManagerMixin,
    # Messages
    InfoPromptResponseManagerMixin,
    DebugPromptResponseManagerMixin,
    WarningPromptResponseManagerMixin,
    ErrorPromptResponseManagerMixin,
    SuccessPromptResponseManagerMixin,
    TaskPromptResponseManagerMixin,
    # Titles
    SeparatorPromptResponseManagerMixin,
):
    output: Optional[AbstractOutputHandler] = Field(
        default=None,
        description="Manages what to do with the generated output (print, or store), "
                    "by default print to stdout"
    )

    _terminal_width: int = PrivateAttr(
        default=None
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_output()

    @property
    def terminal_width(self, reload: bool = False) -> int:
        if reload or self._terminal_width is None:
            import shutil
            self._terminal_width = shutil.get_terminal_size().columns

        return self._terminal_width

    def _init_output(self):
        from wexample_prompt.output.stdout_output_handler import StdoutOutputHandler
        self.output = self.output if (self.output is not None) else StdoutOutputHandler()

    @classmethod
    def get_response_types(cls) -> List[Type["AbstractPromptResponse"]]:
        from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse
        from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
        from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse
        from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
        from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
        from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
        from wexample_prompt.responses.messages.task_prompt_response import TaskPromptResponse
        from wexample_prompt.responses.titles.separator_prompt_response import SeparatorPromptResponse

        return [
            # Basics
            EchoPromptResponse,
            LogPromptResponse,
            InfoPromptResponse,
            # Messages
            DebugPromptResponse,
            WarningPromptResponse,
            ErrorPromptResponse,
            SuccessPromptResponse,
            TaskPromptResponse,
            # Titles
            SeparatorPromptResponse,
        ]

    def print_response(self, response: "AbstractPromptResponse", context: Optional["PromptContext"] = None) -> None:
        self.output.print(response=response, context=context)
