from wexample_prompt.common.io_manager import IoManager

if __name__ == "__main__":
    demo_io = IoManager()

    response = demo_io.choice(
        question="Which vegetable do you prefer?",
        choices=[
            "Onions",
            "Bananas",
        ]
    )

    choice = response.ask()

    if choice is None:
        demo_io.log("Aborted")
    else:
        demo_io.success(choice)
