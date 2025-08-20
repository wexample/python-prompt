from wexample_prompt.common.io_manager import IoManager

several_lines = "> And several short lines \n"
line_breaks_text = f'This is a {"long " * 30}text\n> With a {"long " * 30} line\n{several_lines * 30}'


def echo_long_multiline_text(io: IoManager) -> None:
    io.separator("Check lines break management")
    io.echo(line_breaks_text)


def task_long_multiline_text(io: IoManager) -> None:
    io.separator("Check lines break management in tasks")
    io.task(line_breaks_text)


if __name__ == "__main__":
    io = IoManager()
    echo_long_multiline_text(io)
    task_long_multiline_text(io)
