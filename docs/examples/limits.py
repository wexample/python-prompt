from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse

several_lines = "> And several short lines \n"
line_breaks_text = f'This is a {"long " * 30}text\n> With a {"long " * 30} line\n{several_lines * 30}'


def echo_long_multiline_text(io: IoManager) -> None:
    io.separator("Check lines break management")
    io.echo(line_breaks_text)


def task_long_multiline_text(io: IoManager) -> None:
    io.separator("Check lines break management in tasks")
    io.task(line_breaks_text)


def confirm_long_multiline_text(io: IoManager) -> None:
    io.separator("Check lines break management in tasks")
    io.confirm(
        question=line_breaks_text,
        choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
        default="ok",
    )

def choice_long_multiline_text(io: IoManager) -> None:
    io.separator("Check lines break management in tasks")

    io.choice(
        question=line_breaks_text,
        choices=[
            "Onions",
            "Carrot",
        ]
    ).get_answer()

if __name__ == "__main__":
    io = IoManager()
    echo_long_multiline_text(io)
    task_long_multiline_text(io)
    choice_long_multiline_text(io)
    confirm_long_multiline_text(io)
