from wexample_prompt.common.io_manager import IoManager

line_breaks_text = f'This is a {"long " * 80}text'

if __name__ == "__main__":
    io = IoManager()

    # Simple yes/no box (using preset mapping constant)
    response = io.log(
        message=line_breaks_text,
    )
