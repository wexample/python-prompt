from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.terminal_bg_color import TerminalBgColor
from wexample_prompt.enums.terminal_color import TerminalColor

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_bg_color import TerminalBgColor
    from wexample_prompt.enums.terminal_color import TerminalColor


@base_class
class WithIoManager(BaseClass):
    io: IoManager | None = public_field(
        default=None,
        description="The optional IO manager that could be shared with a parent.",
    )
    parent_io_handler: WithIoManager | None = public_field(
        default=None,
        description="A parent class that may share its IO and context (ex shared verbosity or indentation level).",
    )

    def __attrs_post_init__(self) -> None:
        self._execute_super_attrs_post_init_if_exists()

        if self.parent_io_handler and self.parent_io_handler.io:
            self.io = self.parent_io_handler.io

    @property
    def io_context(self) -> PromptContext:
        # Compute context on-demand to avoid stale state and to honor
        # any dynamic overrides provided by subclass getters.
        return self._create_io_context()

    def get_io_context_colorized(self) -> bool | None:
        return None

    def get_io_context_indentation(self) -> int:
        if self.parent_io_handler is not None:
            return self.parent_io_handler.io_context.indentation + 1
        return 0

    def get_io_context_indentation_background_color(self) -> TerminalBgColor | None:
        return None

    def get_io_context_indentation_character(self) -> str | None:
        return None

    def get_io_context_indentation_color(self) -> TerminalColor | None:
        return None

    def get_io_context_indentation_width(self) -> int | None:
        return None

    def _create_io_context(self, **kwargs) -> PromptContext:
        from wexample_prompt.common.prompt_context import PromptContext

        parent_context = (
            self.parent_io_handler.io_context if self.parent_io_handler else None
        )

        defaults = {
            "parent_context": parent_context,
            "indentation": self.get_io_context_indentation(),
            "indentation_character": self.get_io_context_indentation_character(),
            "indentation_color": self.get_io_context_indentation_color(),
            "indentation_background_color": self.get_io_context_indentation_background_color(),
            "colorized": self.get_io_context_colorized()
            or (
                parent_context.colorized
                if parent_context is not None
                else PromptContext.DEFAULT_COLORIZED
            ),
            "verbosity": (
                parent_context.verbosity
                if parent_context is not None
                else PromptContext.DEFAULT_VERBOSITY
            ),
            "width": self.get_io_context_indentation_width()
            or (parent_context.width if parent_context is not None else None)
            or (self.io.terminal_width if self.io else None),
        }

        defaults.update(kwargs)

        return PromptContext.create_from_kwargs(kwargs=defaults)

    def _init_io_manager(self) -> IoManager:
        from wexample_prompt.common.io_manager import IoManager

        self.io = IoManager()
        return self.io