from wexample_helpers.classes.example.example import Example
from wexample_prompt.common.io_manager import IoManager

class ExceptionExample(Example):
    def execute(self) -> None:
        def make_boom():
            def inner():
                raise ValueError("boom from example")

            def middle():
                inner()

            middle()

        demo_io = IoManager()
        demo_io.error(message="Simple error message")

        try:
            make_boom()
        except Exception as e:
            demo_io.error(message="Error message with exception", exception=e)
