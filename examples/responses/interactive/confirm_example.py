from ..abstract_prompt_response_example import AbstractPromptResponseExample
from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse


class ConfirmExample(AbstractPromptResponseExample):
    def execute(self) -> None:
        io = IoManager()

        # Simple yes/no box (using preset mapping constant)
        response = io.confirm(
            question="@🔵+bold{Do you want to continue?}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="yes",
            reset_on_finish=True,
        )
        print(f"Answer: {response.get_answer()}")

        # Yes / Yes for all / No (using class constant)
        response = io.confirm(
            question="@color:magenta+bold{Proceed with all operations?}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
            default="ok",
            reset_on_finish=True,
        )
        print(f"Answer 2: {response.get_answer()}")

        # Yes / Yes for all / No (using class constant)
        response = io.confirm(
            question="@🟣+bold{Do you prefer not to be asked?}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
            default="yes",
            reset_on_finish=True,
            predefined_answer="no",
        )
        print(f"Answer 3: {response.get_answer()}")

        # Long paragraph example (should wrap across multiple lines in the terminal)
        long_paragraph = (
            "@color:cyan+bold{This is a long paragraph} used to test how confirmation prompts behave when "
            "the question spans multiple lines. It contains enough words to exceed a "
            "@🔶{typical terminal width}, ensuring that auto-wrapping occurs and our erase/"
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
            question=f"Open this @🔷+bold{{URL}}? {long_url}",
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
            question=f"Use this @color:yellow+bold{{file path}}? {long_path}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
            default="ok",
            reset_on_finish=True,
        )
        print(f"Path answer: {response.get_answer()}")

        response = io.confirm(
            question="@🟢+bold{Does this indentation display well?}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="yes",
            reset_on_finish=True,
            indentation=5,
        )
        print(f"Answer: {response.get_answer()}")

        io.indentation = 5
        response = io.confirm(
            question="@🟢+bold{Does this double indentation display well?}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="yes",
            reset_on_finish=True,
            indentation=5,
        )
        print(f"Answer: {response.get_answer()}")

        # === EDGE CASES: NESTING ===
        io.separator("@🔶+bold{NESTING: Nested confirmations}")

        response = io.confirm(
            question="@🔵+bold{Do you want to proceed with nested operations?}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="yes",
            reset_on_finish=True,
        )

        if response.get_answer() == "yes":
            io.indentation += 1

            response = io.confirm(
                question="@🟠+bold{Are you sure? This will trigger sub-operations.}",
                choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
                default="no",
                reset_on_finish=True,
            )

            if response.get_answer() == "yes":
                io.indentation += 1

                response = io.confirm(
                    question="@🔴+bold{Final confirmation: This cannot be undone!}",
                    choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
                    default="cancel",
                    reset_on_finish=True,
                )

                if response.get_answer() == "ok":
                    io.success("@🟢+bold{All confirmations accepted!}")
                else:
                    io.log("@color:yellow{Cancelled at final step}")

                io.indentation -= 1
            else:
                io.log("@color:yellow{Cancelled at second step}")

            io.indentation -= 1
        else:
            io.log("@color:yellow{Cancelled at first step}")

        io.indentation = 0

        # === EDGE CASES: SPECIAL CHARACTERS ===
        io.separator("@🔶+bold{SPECIAL: Special characters and unicode}")

        response = io.confirm(
            question=self.generate_special_characters_text(),
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="yes",
            reset_on_finish=True,
        )
        print(f"Special chars answer: {response.get_answer()}")

        # === EDGE CASES: VERY SHORT TEXT ===
        io.separator("@🔶+bold{LIMITS: Very short text}")

        response = io.confirm(
            question=self.generate_short_text(),
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="yes",
            reset_on_finish=True,
        )
        print(f"Short text answer: {response.get_answer()}")

        io.success("@🟢+bold{Confirm demo complete!}")
