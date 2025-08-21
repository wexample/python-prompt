from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.const.types import LineMessage
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.messages.task_prompt_response import (
        TaskPromptResponse,
    )


class TaskPromptResponseManagerMixin:
    def task(
        self: "IoManager",
        message: LineMessage,
        verbosity: VerbosityLevel | None = VerbosityLevel.DEFAULT,
        context: Optional["PromptContext"] = None,
        **kwargs: Kwargs
    ) -> "TaskPromptResponse":
        from wexample_prompt.responses.messages.task_prompt_response import (
            TaskPromptResponse,
        )

        response = TaskPromptResponse.create_task(
            message=message,
            verbosity=verbosity,
        )

        return self.print_response(
            response=response,
            context=TaskPromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )
