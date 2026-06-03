"""Tests for the IoManager recorder stack — feeds AbstractResponse.prompt_trace."""

from __future__ import annotations


def _make_io():
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.output.prompt_buffer_output_handler import (
        PromptBufferOutputHandler,
    )

    return IoManager(output=PromptBufferOutputHandler())


def test_print_response_stamps_created_at_once() -> None:
    """created_at is set on first print_response and preserved on re-print."""
    from wexample_prompt.responses.log_prompt_response import LogPromptResponse

    io = _make_io()
    response = LogPromptResponse.create_log(message="hello")

    assert response.created_at is None
    io.print_response(response=response)
    first = response.created_at
    assert first is not None

    io.print_response(response=response)
    assert response.created_at == first


def test_recorder_captures_only_within_push_pop() -> None:
    from wexample_prompt.responses.log_prompt_response import LogPromptResponse

    io = _make_io()

    io.print_response(response=LogPromptResponse.create_log(message="outside-before"))

    buf = io.push_recorder()
    io.print_response(response=LogPromptResponse.create_log(message="captured-1"))
    io.print_response(response=LogPromptResponse.create_log(message="captured-2"))
    captured = io.pop_recorder()

    io.print_response(response=LogPromptResponse.create_log(message="outside-after"))

    assert captured is buf
    assert len(captured) == 2
    assert "captured-1" in captured[0].render()
    assert "captured-2" in captured[1].render()


def test_recorder_stack_isolates_nested_buffers() -> None:
    """Nested push: inner captures only its own emissions, outer captures only its own."""
    from wexample_prompt.responses.log_prompt_response import LogPromptResponse

    io = _make_io()

    outer = io.push_recorder()
    io.print_response(response=LogPromptResponse.create_log(message="outer-1"))

    inner = io.push_recorder()
    io.print_response(response=LogPromptResponse.create_log(message="inner-1"))
    io.print_response(response=LogPromptResponse.create_log(message="inner-2"))
    io.pop_recorder()

    io.print_response(response=LogPromptResponse.create_log(message="outer-2"))
    io.pop_recorder()

    inner_texts = [r.render() for r in inner]
    outer_texts = [r.render() for r in outer]

    assert len(inner) == 2
    assert "inner-1" in inner_texts[0]
    assert "inner-2" in inner_texts[1]

    assert len(outer) == 2
    assert "outer-1" in outer_texts[0]
    assert "outer-2" in outer_texts[1]

    # Critical: outer must NOT have absorbed inner's emissions.
    assert all("inner" not in t for t in outer_texts)


def test_recorder_captures_quiet_responses() -> None:
    """QUIET silences the CLI render but the trace still records — decision: agent IA sees everything."""
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.log_prompt_response import LogPromptResponse

    io = _make_io()

    buf = io.push_recorder()
    quiet = LogPromptResponse.create_log(message="quiet-one")
    quiet.verbosity = VerbosityLevel.QUIET
    io.print_response(response=quiet)
    io.pop_recorder()

    assert len(buf) == 1
    assert buf[0] is quiet
    assert buf[0].created_at is not None
