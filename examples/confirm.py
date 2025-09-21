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

    # Long paragraph example (should wrap across multiple lines in the terminal)
    long_paragraph = (
        "This is a long paragraph used to test how confirmation prompts behave when "
        "the question spans multiple lines. It contains enough words to exceed a "
        "typical terminal width, ensuring that auto-wrapping occurs and our erase/" 
        "render logic can be validated for multi-line content rendering."
    )
    response = io.confirm(
        question=long_paragraph,
        choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
        default="yes",
        reset_on_finish=True,
    )
    print(f"Long paragraph answer: {response.get_answer()}")

    # Long single-line example (URL / file path)
    long_url = (
        "https://example.com/some/really/long/path/that/keeps/going/and/going/"
        "and/contains/query?with=lots&of=parameters&and=maybe#fragments"
    )
    response = io.confirm(
        question=f"Open this URL? {long_url}",
        choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
        default="ok",
        reset_on_finish=True,
    )
    print(f"URL answer: {response.get_answer()}")

    long_path = (
        "/home/user/projects/some_project/build/output/deploy/"
        "very/very/very/long/subdirectory/structure/with/files/and/more/files/"
        "and/even/more/nested/paths/that/should/wrap/properly.txt"
    )
    response = io.confirm(
        question=f"Use this file path? {long_path}",
        choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
        default="ok",
        reset_on_finish=True,
    )
    print(f"Path answer: {response.get_answer()}")
