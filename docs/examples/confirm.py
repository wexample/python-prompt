from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse

if __name__ == "__main__":
    io = IoManager()

    # Simple yes/no box (using preset mapping constant)
    response = io.confirm(
        question="Do you want to continue?",
        choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
        default="yes",
        reset_on_finish=True,
    )
    print(f"Answer: {response.get_answer()}")

    # Yes / Yes for all / No (using class constant)
    response = io.confirm(
        question="Proceed with all operations?",
        choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
        default="ok",
        reset_on_finish=True,
    )
    print(f"Answer 2: {response.get_answer()}")

    # Yes / Yes for all / No (using class constant)
    response = io.confirm(
        question="Do you prefer not to be asked?",
        choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
        default="yes",
        reset_on_finish=True,
        predefined_answer="no"
    )
    print(f"Answer 3: {response.get_answer()}")
