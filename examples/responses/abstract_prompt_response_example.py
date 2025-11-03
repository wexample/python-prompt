from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.example.interactive_example import InteractiveExample


@base_class
class AbstractPromptResponseExample(InteractiveExample):
    """
    Abstract base class for prompt response examples.
    Provides shared helper methods for generating edge case test content.
    """

    @staticmethod
    def generate_long_multiline_text() -> str:
        """
        Generate a long multiline text with line breaks for testing limits.
        Tests how prompts handle very long text with multiple lines.
        """
        several_lines = "> @color:cyan{And several short lines}\n"
        return (
                "@🔵+bold{This is a }" + ("@color:yellow{long} " * 15) + "text\n"
                                                                        "> With a " + (
                        "@color:magenta{long} " * 10) + "line\n"
                + several_lines * 10
        )

    @staticmethod
    def generate_long_single_line_text() -> str:
        """
        Generate a very long single line text for testing wrapping behavior.
        Tests how prompts handle text that exceeds terminal width.
        """
        return (
                "@🔵+bold{This is a }"
                + ("@color:yellow{long} " * 20)
                + "text with @🟣+underline{inline styling} sprinkled everywhere."
        )

    @staticmethod
    def generate_long_url() -> str:
        """Generate a long URL for testing path/URL display."""
        return (
            "https://example.com/some/really/long/path/that/keeps/going/and/going/"
            "and/contains/query?with=lots&of=parameters&and=maybe#fragments"
        )

    @staticmethod
    def generate_long_path() -> str:
        """Generate a long file path for testing path display."""
        return (
            "/home/user/projects/some_project/build/output/deploy/"
            "very/very/very/long/subdirectory/structure/with/files/and/more/files/"
            "and/even/more/nested/paths/that/should/wrap/properly.txt"
        )

    @staticmethod
    def generate_short_text() -> str:
        """Generate very short text for testing minimal content."""
        return "@🔵{OK}"

    @staticmethod
    def generate_empty_text() -> str:
        """Generate empty text for testing edge case."""
        return ""

    @staticmethod
    def generate_special_characters_text() -> str:
        """Generate text with special characters and unicode."""
        return "@🔵{Special: } émojis 🎉 symbols ±×÷ quotes \"'` brackets []{}() slashes /\\"

    def create_io_manager(self) -> IoManager:
        """Create and return a new IoManager instance."""
        return IoManager()
