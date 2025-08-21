from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.common.prompt_context import PromptContext

line_breaks_text = f'This is a {"long " * 80}text'

if __name__ == "__main__":
    io = IoManager()

    # Simple yes/no box (using preset mapping constant)
    io.log(
        message=line_breaks_text,
    )

    io.log(
        message=line_breaks_text,
        context=PromptContext(
            formatting=True,
            indentation=1,
        )
    )
