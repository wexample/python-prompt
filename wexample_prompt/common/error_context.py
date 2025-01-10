from wexample_prompt.common.prompt_context import PromptContext
import traceback


class ErrorContext(PromptContext):
    trace: bool = True

    def format_message(self, message: str) -> str:
        message = super().format_message(message)

        if self.trace:
            trace = traceback.format_exc()
            if trace and trace != 'NoneType: None\n':
                message = f"{message}\n{trace}"

        return message
