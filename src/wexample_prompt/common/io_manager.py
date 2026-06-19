from __future__ import annotations

import time
from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.mixin.response.code_prompt_response_manager_mixin import (
    CodePromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.command_prompt_response_manager_mixin import (
    CommandPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.data.list_prompt_response_manager_mixin import (
    ListPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.data.multiple_prompt_response_manager_mixin import (
    MultiplePromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.data.properties_prompt_response_manager_mixin import (
    PropertiesPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.data.suggestions_prompt_response_manager_mixin import (
    SuggestionsPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.data.table_prompt_response_manager_mixin import (
    TablePromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.data.tree_prompt_response_manager_mixin import (
    TreePromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.echo_prompt_response_manager_mixin import (
    EchoPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.frame_prompt_response_manager_mixin import (
    FramePromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.interactive.choice_prompt_response_manager_mixin import (
    ChoicePromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.interactive.confirm_prompt_response_manager_mixin import (
    ConfirmPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.interactive.file_picker_prompt_response_manager_mixin import (
    FilePickerPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.interactive.input_prompt_response_manager_mixin import (
    InputPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.interactive.leader_line_prompt_response_manager_mixin import (
    LeaderLinePromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.interactive.multiline_input_prompt_response_manager_mixin import (
    MultilineInputPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.interactive.pending_prompt_response_manager_mixin import (
    PendingPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.interactive.progress_prompt_response_manager_mixin import (
    ProgressPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.interactive.screen_prompt_response_manager_mixin import (
    ScreenPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.interactive.spinner_prompt_response_manager_mixin import (
    SpinnerPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.log_prompt_response_manager_mixin import (
    LogPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.messages.debug_prompt_response_manager_mixin import (
    DebugPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.messages.error_prompt_response_manager_mixin import (
    ErrorPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.messages.failure_prompt_response_manager_mixin import (
    FailurePromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.messages.info_prompt_response_manager_mixin import (
    InfoPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.messages.success_prompt_response_manager_mixin import (
    SuccessPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.messages.task_prompt_response_manager_mixin import (
    TaskPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.messages.warning_prompt_response_manager_mixin import (
    WarningPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.titles.separator_prompt_response_manager_mixin import (
    SeparatorPromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.titles.subtitle_prompt_response_manager_mixin import (
    SubtitlePromptResponseManagerMixin,
)
from wexample_prompt.mixin.response.titles.title_prompt_response_manager_mixin import (
    TitlePromptResponseManagerMixin,
)
from wexample_prompt.mixin.with_indentation import WithIndentation

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.output.abstract_prompt_output_handler import (
        AbstractPromptOutputHandler,
    )
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


@base_class
class IoManager(
    # Basics
    EchoPromptResponseManagerMixin,
    LogPromptResponseManagerMixin,
    # Messages
    InfoPromptResponseManagerMixin,
    DebugPromptResponseManagerMixin,
    WarningPromptResponseManagerMixin,
    ErrorPromptResponseManagerMixin,
    FailurePromptResponseManagerMixin,
    SuccessPromptResponseManagerMixin,
    TaskPromptResponseManagerMixin,
    # Titles
    SeparatorPromptResponseManagerMixin,
    TitlePromptResponseManagerMixin,
    SubtitlePromptResponseManagerMixin,
    # Data
    ListPromptResponseManagerMixin,
    MultiplePromptResponseManagerMixin,
    PropertiesPromptResponseManagerMixin,
    SuggestionsPromptResponseManagerMixin,
    TablePromptResponseManagerMixin,
    TreePromptResponseManagerMixin,
    FramePromptResponseManagerMixin,
    CommandPromptResponseManagerMixin,
    CodePromptResponseManagerMixin,
    # Interactive
    ChoicePromptResponseManagerMixin,
    FilePickerPromptResponseManagerMixin,
    PendingPromptResponseManagerMixin,
    LeaderLinePromptResponseManagerMixin,
    ProgressPromptResponseManagerMixin,
    ScreenPromptResponseManagerMixin,
    SpinnerPromptResponseManagerMixin,
    ConfirmPromptResponseManagerMixin,
    InputPromptResponseManagerMixin,
    MultilineInputPromptResponseManagerMixin,
    # Parent classes
    WithIndentation,
    BaseClass,
):
    default_context_verbosity: VerbosityLevel = public_field(
        default=VerbosityLevel.DEFAULT,
        description="The overall verbosity level used in contexts.",
    )
    default_response_verbosity: VerbosityLevel = public_field(
        default=VerbosityLevel.DEFAULT,
        description="The default verbosity for every generated message.",
    )
    output: AbstractPromptOutputHandler = public_field(
        default=None,
        description="Manages what to do with the generated output (print, or store), "
        "by default print to stdout",
    )
    _recorder_stack: list[list[AbstractPromptResponse]] = private_field(
        factory=list,
        description="LIFO stack of capture buffers for prompt_trace. Each "
        "execute_kernel_command (and each QueuedCollectionResponse step) pushes a "
        "fresh buffer here; every print_response appends to the top buffer (so "
        "nested sub-commands capture only their own emissions, not the parent's). "
        "Empty when no command is executing — capture is then a no-op.",
    )
    _resize_callbacks: list = private_field(
        factory=list,
        description="Subscribers notified after a SIGWINCH refreshes the terminal "
        "width cache. Single source of truth for terminal resize — interactive "
        "widgets register here instead of installing their own SIGWINCH handlers.",
    )
    _terminal_width: int = private_field(
        default=None, description="The terminal with cached value."
    )
    _winch_installed: bool = private_field(
        default=False,
        description="Whether SIGWINCH is wired to our handler. Set on first install; "
        "stays True for the lifetime of the IoManager (we never uninstall, since "
        "another IoManager could exist and we want to keep notifying subscribers).",
    )

    def __attrs_post_init__(self) -> None:
        self._init_output()
        # Note: SIGWINCH listening is OPT-IN — call `enable_resize_listening()`
        # explicitly from the owner (typically the kernel) so only the
        # "primary" IoManager wires the signal. Auto-installing here would
        # have any later-created IoManager silently steal SIGWINCH from the
        # one before it (signal.signal replaces, doesn't chain).

    @classmethod
    def get_response_types(cls) -> list[type[AbstractPromptResponse]]:
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )
        from wexample_prompt.responses.data.multiple_prompt_response import (
            MultiplePromptResponse,
        )
        from wexample_prompt.responses.data.properties_prompt_response import (
            PropertiesPromptResponse,
        )
        from wexample_prompt.responses.data.suggestions_prompt_response import (
            SuggestionsPromptResponse,
        )
        from wexample_prompt.responses.data.table_prompt_response import (
            TablePromptResponse,
        )
        from wexample_prompt.responses.data.tree_prompt_response import (
            TreePromptResponse,
        )
        from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse
        from wexample_prompt.responses.interactive.choice_prompt_response import (
            ChoicePromptResponse,
        )
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )
        from wexample_prompt.responses.interactive.file_picker_prompt_response import (
            FilePickerPromptResponse,
        )
        from wexample_prompt.responses.interactive.input_prompt_response import (
            InputPromptResponse,
        )
        from wexample_prompt.responses.interactive.pending_prompt_response import (
            PendingPromptResponse,
        )
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )
        from wexample_prompt.responses.interactive.screen_prompt_response import (
            ScreenPromptResponse,
        )
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse
        from wexample_prompt.responses.messages.debug_prompt_response import (
            DebugPromptResponse,
        )
        from wexample_prompt.responses.messages.error_prompt_response import (
            ErrorPromptResponse,
        )
        from wexample_prompt.responses.messages.failure_prompt_response import (
            FailurePromptResponse,
        )
        from wexample_prompt.responses.messages.info_prompt_response import (
            InfoPromptResponse,
        )
        from wexample_prompt.responses.messages.success_prompt_response import (
            SuccessPromptResponse,
        )
        from wexample_prompt.responses.messages.task_prompt_response import (
            TaskPromptResponse,
        )
        from wexample_prompt.responses.messages.warning_prompt_response import (
            WarningPromptResponse,
        )
        from wexample_prompt.responses.titles.separator_prompt_response import (
            SeparatorPromptResponse,
        )
        from wexample_prompt.responses.titles.subtitle_prompt_response import (
            SubtitlePromptResponse,
        )
        from wexample_prompt.responses.titles.title_prompt_response import (
            TitlePromptResponse,
        )

        return [
            # Basics
            EchoPromptResponse,
            LogPromptResponse,
            InfoPromptResponse,
            # Messages
            DebugPromptResponse,
            WarningPromptResponse,
            ErrorPromptResponse,
            FailurePromptResponse,
            SuccessPromptResponse,
            TaskPromptResponse,
            # Titles
            SeparatorPromptResponse,
            TitlePromptResponse,
            SubtitlePromptResponse,
            # Data
            ListPromptResponse,
            MultiplePromptResponse,
            PropertiesPromptResponse,
            SuggestionsPromptResponse,
            TablePromptResponse,
            TreePromptResponse,
            # Interactive
            ChoicePromptResponse,
            FilePickerPromptResponse,
            PendingPromptResponse,
            ProgressPromptResponse,
            ScreenPromptResponse,
            ConfirmPromptResponse,
            InputPromptResponse,
        ]

    @property
    def terminal_width(self) -> int:
        if self._terminal_width is None:
            self.reload_terminal_width()
        return self._terminal_width

    def create_context(self, context: PromptContext | None = None) -> PromptContext:
        from wexample_prompt.common.prompt_context import PromptContext

        base_context = PromptContext.create_if_none(context=context)
        context_kwargs = PromptContext.create_kwargs_from_context(context=base_context)

        base_indentation_length = (
            context_kwargs.get("indentation_length") or self.indentation_length
        )
        base_indentation = context_kwargs.get("indentation", 0)
        total_indentation = base_indentation + self.indentation

        context_kwargs["colorized"] = base_context.colorized
        context_kwargs["formatting"] = base_context.formatting
        context_kwargs["indentation"] = total_indentation
        context_kwargs["indentation_length"] = base_indentation_length
        verbosity = context_kwargs.get("verbosity")
        context_kwargs["verbosity"] = (
            verbosity if verbosity is not None else self.default_context_verbosity
        )

        width = context_kwargs.get("width")
        if width is None:
            context_kwargs["width"] = self.terminal_width - (
                total_indentation * base_indentation_length
            )

        return PromptContext.create_from_parent_context_and_kwargs(
            parent_context=base_context.parent_context,
            kwargs=context_kwargs,
        )

    def enable_resize_listening(self) -> bool:
        """Wire SIGWINCH so this IoManager refreshes the width cache and
        notifies its subscribers on every terminal resize.

        Opt-in by design: call this from the owner of the *primary*
        IoManager (typically the kernel) once during setup. Subsequent
        IoManager instances must NOT call it, otherwise they'd silently
        steal SIGWINCH from the primary (signal.signal replaces, doesn't
        chain).

        Safe to call from any environment: Windows has no SIGWINCH, and
        non-main threads raise on `signal.signal` — both cases are
        swallowed and we fall back to lazy refresh on demand.

        Returns True if the handler was installed (or already was);
        False if the environment doesn't support it.
        """
        if self._winch_installed:
            return True
        try:
            import signal

            signal.signal(signal.SIGWINCH, self._on_sigwinch)
            self._winch_installed = True
            return True
        except (AttributeError, ValueError, OSError):
            return False

    def erase_response(
        self,
        response: AbstractPromptResponse,
    ) -> None:
        self.output.erase(response=response)

    def pop_recorder(self) -> list[AbstractPromptResponse]:
        """Close the top capture buffer and return its contents."""
        return self._recorder_stack.pop()

    def print_response(
        self,
        response: AbstractPromptResponse,
        context: PromptContext | None = None,
        frame: str | bool | None = None,
    ) -> AbstractPromptResponse:
        # `frame=` shortcut: wrap any response in a FramePromptResponse before
        # printing. `True` → untitled cartouche, str → titled cartouche. Saves
        # callers from building Frame(responses=[...]) by hand for the common
        # "this block deserves its own box" case (agent /info blocks, etc.).
        if frame:
            from wexample_prompt.responses.frame_prompt_response import (
                FramePromptResponse,
            )

            wrapped = FramePromptResponse.create_frame(
                title=frame if isinstance(frame, str) else None,
                responses=[response],
                verbosity=response.verbosity,
            )
            # Print the wrapped version (recurses once, frame=None this time)
            # so the recorder + verbosity + output handlers stay aligned.
            self.print_response(response=wrapped, context=context)
            # Caller still gets the inner response back — preserves the typed
            # return contract (`io.code()` returns CodePromptResponse, etc.).
            return response

        # Stamp emission time once, regardless of verbosity — the recorder
        # captures even QUIET responses so consumers (agent IA, MCP) see the
        # full chronology, not just what the CLI happened to render.
        if response.created_at is None:
            response.created_at = time.time()

        if self._recorder_stack:
            self._recorder_stack[-1].append(response)

        # Quiet mode: capture above, but skip the CLI render.
        if response.verbosity == VerbosityLevel.QUIET:
            return response

        self.output.print(
            response=response, context=self.create_context(context=context)
        )

        return response

    def push_recorder(self) -> list[AbstractPromptResponse]:
        """Open a fresh capture buffer at the top of the stack and return it."""
        buf: list[AbstractPromptResponse] = []
        self._recorder_stack.append(buf)
        return buf

    def reload_terminal_width(self) -> int:
        import shutil

        self._terminal_width = shutil.get_terminal_size().columns
        return self._terminal_width

    def subscribe_resize(self, callback) -> callable:
        """Register `callback` to be invoked after each terminal resize.

        The callback receives no arguments. The cache has already been
        refreshed (`self._terminal_width`) by the time it fires, so the
        callback can read `self.terminal_width` synchronously.

        Returns an `unsubscribe()` function — call it to detach the
        callback (e.g. in a widget's `finally`).
        """
        self._resize_callbacks.append(callback)

        def unsubscribe() -> None:
            try:
                self._resize_callbacks.remove(callback)
            except ValueError:
                pass

        return unsubscribe

    def _init_output(self) -> None:
        from wexample_prompt.output.prompt_stdout_output_handler import (
            PromptStdoutOutputHandler,
        )

        self.output = (
            self.output if (self.output is not None) else PromptStdoutOutputHandler()
        )

    def _on_sigwinch(self, signum, frame) -> None:  # noqa: ARG002
        self.reload_terminal_width()
        # Iterate over a copy: callbacks may unsubscribe themselves and
        # mutate the list mid-iteration.
        for cb in list(self._resize_callbacks):
            try:
                cb()
            except Exception:  # noqa: BLE001
                # A misbehaving subscriber must not break SIGWINCH for
                # the others.
                pass
