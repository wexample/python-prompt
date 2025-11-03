import os

from ..abstract_prompt_response_example import AbstractPromptResponseExample
from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.enums.choice import FilePickerMode
from wexample_prompt.enums.terminal_color import TerminalColor


class ChoiceExample(AbstractPromptResponseExample):
    def execute(self) -> None:
        demo_io = IoManager()

        choice = demo_io.choice(
            question="Which @🟠+bold{vegetable} do you prefer?",
            choices=[
                "Onions",
                "Carrot",
            ],
            color=TerminalColor.CYAN,
        ).get_answer()

        if choice is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{choice}}}", color=TerminalColor.GREEN)

        choice = demo_io.choice(
            question="Which @🔶{fruit} do you prefer?",
            choices={
                "apples": "Apples",
                "bananas": "Bananas",
            },
            color=TerminalColor.MAGENTA,
        ).get_answer()

        if choice is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{choice}}}", color=TerminalColor.GREEN)

        choice = demo_io.choice(
            question="This question already has an @🔵+bold{answer}, so the choice is not interactive:",
            choices={
                "no": "No",
                "maybe": "Maybe",
                "yes": "Yes",
            },
            predefined_answer="Yes",
        ).get_answer()

        demo_io.separator("@🔶+bold{Files selection}")

        file = demo_io.file_picker(
            question="Select a @🔷{file}",
            mode=FilePickerMode.FILES,
        ).get_answer()

        if file is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{file}}}", color=TerminalColor.GREEN)

        file = demo_io.file_picker(
            question="Select a @🟤+bold{directory}",
            mode=FilePickerMode.DIRS,
        ).get_answer()

        if file is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{file}}}", color=TerminalColor.GREEN)

        file = None
        base_dir = os.getcwd()
        while file is None:
            file = demo_io.file_picker(
                base_dir=base_dir,
                question="Select a file somewhere",
                mode=FilePickerMode.BOTH,
                reset_on_finish=True,
                allow_parent_selection=True,
            ).get_answer()

            if file:
                absolute_path = os.path.join(base_dir, file)
                if os.path.isdir(absolute_path):
                    base_dir = absolute_path
                    file = None
            else:
                file = False

        if file is False:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{file}}}", color=TerminalColor.GREEN)

        # === EDGE CASES: LIMITS ===
        demo_io.separator("@🔶+bold{LIMITS: Long multiline text in choice}")

        choice = demo_io.choice(
            question=self.generate_long_multiline_text(),
            choices=[
                "Option A",
                "Option B",
            ],
        ).get_answer()

        if choice is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{choice}}}", color=TerminalColor.GREEN)

        demo_io.separator("@🔶+bold{LIMITS: Long single line text}")

        choice = demo_io.choice(
            question=self.generate_long_single_line_text(),
            choices=[
                "Yes",
                "No",
            ],
        ).get_answer()

        if choice is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{choice}}}", color=TerminalColor.GREEN)

        demo_io.separator("@🔶+bold{LIMITS: Very long choice labels}")

        choice = demo_io.choice(
            question="Select an option with @🔵+bold{very long labels}:",
            choices=[
                "This is a very long choice label that contains a lot of text and should test how the choice prompt handles wrapping",
                "Another extremely long option with lots of words to see how it displays in the terminal when it exceeds the width",
                "Short",
            ],
        ).get_answer()

        if choice is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{choice}}}", color=TerminalColor.GREEN)

        demo_io.separator("@🔶+bold{LIMITS: Many choices}")

        many_choices = {f"option_{i}": f"Option {i}" for i in range(1, 21)}
        choice = demo_io.choice(
            question="Select from @🔵+bold{many options}:",
            choices=many_choices,
        ).get_answer()

        if choice is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{choice}}}", color=TerminalColor.GREEN)

        # === EDGE CASES: INDENTATION ===
        demo_io.separator("@🔶+bold{INDENTATION: Choice with indentation}")

        choice = demo_io.choice(
            question="@🟢+bold{Does this indentation display well?}",
            choices=["Yes", "No"],
            indentation=5,
        ).get_answer()

        if choice is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{choice}}}", color=TerminalColor.GREEN)

        demo_io.separator("@🔶+bold{INDENTATION: Double indentation}")

        demo_io.indentation = 5
        choice = demo_io.choice(
            question="@🟢+bold{Does this double indentation display well?}",
            choices=["Yes", "No"],
            indentation=5,
        ).get_answer()

        if choice is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{choice}}}", color=TerminalColor.GREEN)

        demo_io.indentation = 0

        # === EDGE CASES: NESTING ===
        demo_io.separator("@🔶+bold{NESTING: Nested choices}")

        main_choice = demo_io.choice(
            question="@🔵+bold{Select main category}:",
            choices={
                "fruits": "Fruits",
                "vegetables": "Vegetables",
                "cancel": "Cancel",
            },
        ).get_answer()

        if main_choice and main_choice != "cancel":
            demo_io.indentation += 1

            if main_choice == "fruits":
                sub_choice = demo_io.choice(
                    question="@🟠+bold{Select a fruit}:",
                    choices=["Apple", "Banana", "Orange"],
                ).get_answer()

                if sub_choice:
                    demo_io.indentation += 1
                    demo_io.success(f"@🟢{{You selected: {sub_choice}}}")
                    demo_io.indentation -= 1

            elif main_choice == "vegetables":
                sub_choice = demo_io.choice(
                    question="@🟤+bold{Select a vegetable}:",
                    choices=["Carrot", "Broccoli", "Spinach"],
                ).get_answer()

                if sub_choice:
                    demo_io.indentation += 1
                    demo_io.success(f"@🟢{{You selected: {sub_choice}}}")
                    demo_io.indentation -= 1

            demo_io.indentation -= 1

        demo_io.separator("@🔶+bold{SPECIAL: Empty and special characters}")

        choice = demo_io.choice(
            question=self.generate_special_characters_text(),
            choices=[
                "Option with émojis 🎉",
                "Option with symbols ±×÷",
                "Normal option",
            ],
        ).get_answer()

        if choice is None:
            demo_io.log("@color:yellow{Aborted}")
        else:
            demo_io.success(f"@🟢{{{choice}}}", color=TerminalColor.GREEN)
