from ..abstract_prompt_response_example import AbstractPromptResponseExample
from wexample_prompt.common.io_manager import IoManager

class ErrorExample(AbstractPromptResponseExample):
    def execute(self) -> None:
        def make_boom():
            def inner():
                raise ValueError("boom from example")

            def middle():
                inner()

            middle()

        demo_io = IoManager()
        demo_io.error(message="@🔴+bold{Simple error message}")

        try:
            make_boom()
        except Exception as e:
            demo_io.error(
                message="@color:magenta+bold{Error message with exception}",
                exception=e,
            )

        # === EDGE CASES: LIMITS ===
        demo_io.separator("@🔶+bold{LIMITS: Long error messages}")

        demo_io.error(message=self.generate_long_single_line_text())

        demo_io.error(message=self.generate_long_multiline_text())

        long_error_msg = (
            "@🔴+bold{Critical Error:} "
            + ("This is a very long error message that contains detailed information about what went wrong. " * 5)
        )
        demo_io.error(message=long_error_msg)

        # === EDGE CASES: INDENTATION ===
        demo_io.separator("@🔶+bold{INDENTATION: Errors with indentation}")

        demo_io.error(
            message="@🔴+bold{Error at level 0}",
            indentation=0
        )

        demo_io.indentation = 3
        demo_io.error(
            message="@🔴+bold{Error at indentation level 3}"
        )

        demo_io.error(
            message="@🔴+bold{Error at indentation level 3 + 5}",
            indentation=5
        )
        demo_io.indentation = 0

        # === EDGE CASES: NESTING ===
        demo_io.separator("@🔶+bold{NESTING: Nested error contexts}")

        def outer_function():
            demo_io.log("@color:cyan{Starting outer function}")
            demo_io.indentation += 1
            
            try:
                middle_function()
            except Exception as e:
                demo_io.error(
                    message="@🔴+bold{Error caught in outer function}",
                    exception=e
                )
            finally:
                demo_io.indentation -= 1

        def middle_function():
            demo_io.log("@color:yellow{Starting middle function}")
            demo_io.indentation += 1
            
            try:
                inner_function()
            except Exception as e:
                demo_io.error(
                    message="@🟠+bold{Error caught in middle function}",
                    exception=e
                )
                raise  # Re-raise for outer to catch
            finally:
                demo_io.indentation -= 1

        def inner_function():
            demo_io.log("@color:magenta{Starting inner function}")
            demo_io.indentation += 1
            demo_io.error("@🔴+bold{Error in deepest level}")
            demo_io.indentation -= 1
            raise RuntimeError("Nested error example")

        outer_function()

        # === EDGE CASES: SPECIAL CHARACTERS ===
        demo_io.separator("@🔶+bold{SPECIAL: Special characters in errors}")

        demo_io.error(message=self.generate_special_characters_text())

        demo_io.error(
            message="@🔴+bold{Path error:} " + self.generate_long_path()
        )

        demo_io.error(
            message="@🔴+bold{URL error:} " + self.generate_long_url()
        )

        # === EDGE CASES: MULTIPLE EXCEPTIONS ===
        demo_io.separator("@🔶+bold{MULTIPLE: Different exception types}")

        exceptions = [
            (ValueError("Invalid value provided"), "ValueError"),
            (KeyError("missing_key"), "KeyError"),
            (TypeError("Wrong type"), "TypeError"),
            (RuntimeError("Runtime issue"), "RuntimeError"),
        ]

        for exc, exc_type in exceptions:
            demo_io.error(
                message=f"@🔴+bold{{Handling {exc_type}}}",
                exception=exc
            )
