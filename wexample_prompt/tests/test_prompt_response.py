"""Tests for prompt responses."""
import pytest
from pydantic import ValidationError

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.responses.progress_prompt_response import ProgressPromptResponse
from wexample_prompt.responses.list_prompt_response import ListPromptResponse
from wexample_prompt.responses.tree_prompt_response import TreePromptResponse
from wexample_prompt.responses.table_prompt_response import TablePromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestPromptResponse:
    def test_create_basic_response(self):
        """Test creating a basic text response."""
        line = PromptResponseLine(segments=[
            PromptResponseSegment(text="Hello World")
        ])
        response = BasePromptResponse(
            lines=[line],
            response_type=ResponseType.PLAIN
        )
        assert len(response.lines) == 1
        assert response.response_type == ResponseType.PLAIN

    def test_create_table_response(self):
        """Test creating a table response."""
        data = [["Name", "Age"], ["John", "30"], ["Jane", "25"]]
        response = TablePromptResponse.create(data)
        assert response.response_type == ResponseType.TABLE
        assert len(response.lines) == 3
        assert "Name" in str(response.lines[0])

    def test_create_list_response(self):
        """Test creating a list response."""
        items = ["First", "Second", "Third"]
        response = ListPromptResponse.create(items)
        assert response.response_type == ResponseType.LIST
        assert len(response.lines) == 3
        assert "•" in str(response.lines[0])  # Default bullet point

    def test_response_with_context(self):
        """Test response rendering with context."""
        line = PromptResponseLine(segments=[
            PromptResponseSegment(text="Wide Text")
        ])
        response = BasePromptResponse(
            lines=[line],
            response_type=ResponseType.PLAIN
        )
        context = PromptContext(
            terminal_width=40,
            is_tty=True
        )
        rendered = response.render(context)
        assert len(rendered) <= 40

    def test_response_combination(self):
        """Test combining two responses."""
        resp1 = BasePromptResponse(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="First")
            ])],
            response_type=ResponseType.PLAIN
        )
        resp2 = BasePromptResponse(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="Second")
            ])],
            response_type=ResponseType.PLAIN
        )
        combined = resp1.append(resp2)
        assert len(combined.lines) == 2

    def test_styled_response(self):
        """Test applying style to entire response."""
        response = BasePromptResponse(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="Text")
            ])],
            response_type=ResponseType.PLAIN
        )
        styled = response.wrap([TextStyle.BOLD])
        assert TextStyle.BOLD in styled.lines[0].segments[0].styles

    def test_tree_response(self):
        """Test creating a tree response."""
        tree_data = {
            "root": {
                "child1": "value1",
                "child2": {
                    "grandchild": "value2"
                }
            }
        }
        response = TreePromptResponse.create(tree_data)
        assert response.response_type == ResponseType.TREE
        assert len(response.lines) > 1
        # Check for tree characters
        assert "└" in str(response.lines[-1]) or "├" in str(response.lines[-1])

    def test_progress_response(self):
        """Test creating a progress response."""
        response = ProgressPromptResponse.create(total=100, current=50)
        assert response.response_type == ResponseType.PROGRESS
        rendered = str(response.lines[0])
        assert "[" in rendered and "]" in rendered  # Progress bar brackets
        assert "50%" in rendered
