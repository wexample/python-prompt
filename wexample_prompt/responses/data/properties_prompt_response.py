from typing import Dict, Any, Optional, List, Type

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class PropertiesPromptResponse(AbstractPromptResponse):
    """Render a dictionary of properties as a formatted block, with optional title.

    The visual width adapts to the provided render context. Lines are generated during
    render, so the response remains context-agnostic until displayed.
    """

    @classmethod
    def get_example_class(cls) -> Type:
        from wexample_prompt.example.response.data.properties_example import PropertiesExample
        return PropertiesExample

    @classmethod
    def create_properties(
            cls,
            properties: Dict[str, Any],
            title: Optional[str] = None,
            nested_indent: int = 2,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
            **kwargs,
    ) -> "PropertiesPromptResponse":
        # Use a fixed default content width. Context-based sizing will be handled at render stage later.
        total_width = 80
        content_width = 78  # total minus padding

        # Compute max key width by scanning nested dicts
        max_key_width = 0

        def scan_keys(obj: Dict[str, Any]):
            nonlocal max_key_width
            for k, v in obj.items():
                max_key_width = max(max_key_width, len(str(k)))
                if isinstance(v, dict):
                    scan_keys(v)

        scan_keys(properties)

        content_lines = cls._format_properties(properties, max_key_width, nested_indent)

        lines: List[PromptResponseLine] = []
        # Empty top spacer
        lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="")]))

        if title:
            title_len = len(title)
            left_pad = max(0, (content_width - title_len) // 2)
            right_pad = max(0, content_width - title_len - left_pad)
            lines.append(
                PromptResponseLine(
                    segments=[
                        PromptResponseSegment(text="-" * left_pad),
                        PromptResponseSegment(text=f" {title} "),
                        PromptResponseSegment(text="-" * max(0, right_pad - 2)),
                    ]
                )
            )
        else:
            lines.append(cls._create_border_line(content_width))

        for content in content_lines:
            lines.append(
                PromptResponseLine(
                    segments=[
                        PromptResponseSegment(text=" "),
                        PromptResponseSegment(text=content),
                    ]
                )
            )

        lines.append(cls._create_border_line(content_width))

        return cls(
            lines=lines,
            properties=properties,
            title=title,
            nested_indent=nested_indent,
            verbosity=verbosity,
            **kwargs,
        )

    @staticmethod
    def _format_properties(
            properties: Dict[str, Any],
            key_width: int,
            indent: int,
            current_indent: int = 0,
    ) -> List[str]:
        lines: List[str] = []
        indent_str = " " * current_indent
        for key, value in properties.items():
            if isinstance(value, dict):
                lines.append(f"{indent_str}{str(key)}:")
                lines.extend(
                    PropertiesPromptResponse._format_properties(
                        value, key_width, indent, current_indent + indent
                    )
                )
            else:
                key_str = str(key).ljust(key_width)
                lines.append(f"{indent_str}{key_str} : {str(value)}")
        return lines

    @staticmethod
    def _create_border_line(width: int) -> PromptResponseLine:
        return PromptResponseLine(segments=[PromptResponseSegment(text=f"{'-' * width}")])
