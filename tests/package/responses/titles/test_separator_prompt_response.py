from __future__ import annotations

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.responses.titles.separator_prompt_response import (
    SeparatorPromptResponse,
)


def test_separator_label_markup_is_rendered() -> None:
    response = SeparatorPromptResponse.create_separator(
        label="@color:magenta+bold{Section}",
        width=40,
    )

    rendered = response.render(context=PromptContext())
    assert rendered is not None
    assert "@color" not in rendered
    assert "Section" in rendered
