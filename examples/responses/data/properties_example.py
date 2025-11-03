"""Interactive example for properties - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class PropertiesExample(AbstractPromptResponseExample):
    """Interactive example for properties."""

    def execute(self) -> None:
        """Execute properties examples."""
        from wexample_prompt.example.response.data.properties_example import (
            PropertiesExample as SrcPropertiesExample,
        )

        self.execute_delegated(SrcPropertiesExample)
