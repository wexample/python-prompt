from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.messages import TaskPromptResponse


class TaskPromptResponseManagerMixin:
    def task(
            self,
            message: str,
            context: Optional["PromptContext"] = None,
            **kwargs:Kwargs
    ) -> "TaskPromptResponse":
        from wexample_prompt.responses.messages.task_prompt_response import TaskPromptResponse

        response = TaskPromptResponse.create_task(
            message=message,
        )

        self.print_response(
            response=response,
            context=TaskPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )

        return response
