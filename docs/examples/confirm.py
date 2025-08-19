from wexample_prompt.common.io_manager import IoManager

if __name__ == "__main__":
    io = IoManager()

    # Simple yes/no box
    res = io.confirm(
        question="Do you want to continue?",
        preset="yes_no",
        reset_on_finish=True,
    ).ask()
    print(f"Answer: {res}")

    # Yes / Yes for all / No
    res2 = io.confirm(
        question="Proceed with all operations?",
        preset="yes_no_all",
        reset_on_finish=True,
    ).ask()
    print(f"Answer 2: {res2}")