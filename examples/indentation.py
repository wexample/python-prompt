from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.classes.example.example import Example
from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.terminal_bg_color import TerminalBgColor
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.mixins.with_io_methods import WithIoMethods

line_breaks_text = (
    "@🔵+bold{This is a }"
    + ("@color:yellow{long} " * 20)
    + "text with @🟣+underline{inline styling} sprinkled everywhere."
)


@base_class
class TestClassA(WithIoMethods):
    def __attrs_post_init__(self, **kwargs):
        self._init_io_manager()
        self.info("@🟢+bold{Test class A created}")

    def create_b(self) -> TestClassB:
        test_class_b = TestClassB(io=self.io)
        return test_class_b


@base_class
class TestClassB(WithIoMethods):
    def __attrs_post_init__(self, **kwargs):
        self._init_io_manager()
        self.info("@🟢+bold{Test class B created}")
        progress = self.progress(
            label="@color:magenta+bold{Some progress bar...}"
        ).get_handle()
        progress.finish(label="@🟢+bold{Progress complete}")

    def get_io_context_indentation_color(self) -> TerminalColor | None:
        return TerminalColor.WHITE

    def get_io_context_indentation_background_color(self) -> TerminalBgColor | None:
        return TerminalBgColor.LIGHT_BLACK

    def get_io_context_indentation_character(self) -> str | None:
        return "|"


class Indentation(Example):
    def execute(self) -> None:
        io = IoManager()

        io.log(
            message=line_breaks_text,
        )

        io.log(
            message=line_breaks_text,
            context=PromptContext(
                formatting=True,
                indentation=1,
            ),
        )

        test_class_a = TestClassA()
        test_class_a.create_b()
