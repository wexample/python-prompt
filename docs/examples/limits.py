from wexample_prompt.common.io_manager import IoManager


def echo_long_multiline_text(io: IoManager) -> None:
    several_lines = "> And several short lines \n"

    io.separator("Check lines break managerment")
    io.echo(
        f'This is a {"long " * 30}text\n'
        f'> With a {"long " * 30} line\n'
        f'{several_lines * 30}'

    )


if __name__ == "__main__":
    io = IoManager()
    echo_long_multiline_text(io)
