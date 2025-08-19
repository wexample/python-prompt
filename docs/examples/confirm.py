from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse

if __name__ == "__main__":
    io = IoManager()

    # Simple yes/no box (using preset mapping constant)
    res = io.confirm(
        question="Do you want to continue?",
        choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
        default="yes",
        reset_on_finish=True,
    ).ask()
    print(f"Answer: {res}")

    # Yes / Yes for all / No (using class constant)
    res2 = io.confirm(
        question="Proceed with all operations?",
        choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
        default="ok",
        reset_on_finish=True,
    ).ask()
    print(f"Answer 2: {res2}")
