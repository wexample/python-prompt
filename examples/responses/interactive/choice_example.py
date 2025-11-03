import os

from wexample_helpers.classes.example.example import Example
from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.enums.choice import FilePickerMode
from wexample_prompt.enums.terminal_color import TerminalColor


class ChoiceExample(Example):
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
