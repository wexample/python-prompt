from wexample_prompt.common.io_manager import IoManager

if __name__ == "__main__":
    demo_io = IoManager()

    choice = demo_io.choice(
        question="Which vegetable do you prefer?",
        choices=[
            "Onions",
            "Carrot",
        ]
    ).ask()

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
    ).ask()

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
        }
    ).ask(answer="Yes")
