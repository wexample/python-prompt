import os

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.enums.choice import FilePickerMode

if __name__ == "__main__":
    demo_io = IoManager()

    choice = demo_io.choice(
        question="Which vegetable do you prefer?",
        choices=[
            "Onions",
            "Carrot",
        ]
    ).get_answer()

    if choice is None:
        demo_io.log("Aborted")
    else:
        demo_io.success(choice)

    choice = demo_io.choice(
        question="Which fruit do you prefer?",
        choices={
            "apples": "Apples",
            "bananas": "Bananas",
        }
    ).get_answer()

    if choice is None:
        demo_io.log("Aborted")
    else:
        demo_io.success(choice)

    choice = demo_io.choice(
        question="This question already have an answer, so the choice is not interactive:",
        choices={
            "no": "No",
            "maybe": "Maybe",
            "yes": "Yes",
        },
        answer="Yes"
    ).get_answer()

    demo_io.separator("Files selection")

    file = demo_io.file_picker(
        question="Select a file",
        mode=FilePickerMode.FILES
    ).get_answer()

    if file is None:
        demo_io.log("Aborted")
    else:
        demo_io.success(file)

    file = demo_io.file_picker(
        question="Select a directory",
        mode=FilePickerMode.DIRS
    ).get_answer()

    if file is None:
        demo_io.log("Aborted")
    else:
        demo_io.success(file)

    file = None
    base_dir = os.getcwd()
    while file is None:
        file = demo_io.file_picker(
            base_dir=base_dir,
            question="Select a file somewhere",
            mode=FilePickerMode.BOTH,
            reset_on_finish=True,
            allow_parent_selection=True
        ).get_answer()

        if file:
            absolute_path = os.path.join(base_dir, file)
            if os.path.isdir(absolute_path):
                base_dir = absolute_path
                file = None
        else:
            file = False

    if file is False:
        demo_io.log("Aborted")
    else:
        demo_io.success(file)
