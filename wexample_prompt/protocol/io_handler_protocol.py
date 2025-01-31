from abc import abstractmethod
from typing import Protocol, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse
    from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse
    from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
    from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
    from wexample_prompt.responses.list_prompt_response import ListPromptResponse
    from wexample_prompt.responses.table_prompt_response import TablePromptResponse

T = TypeVar('T', bound='BasePromptResponse')


class IoHandlerProtocol(Protocol):
    @abstractmethod
    def title(self, message: str, **kwargs) -> "TitlePromptResponse":
        pass

    @abstractmethod
    def subtitle(self, message: str, **kwargs) -> "SubtitlePromptResponse":
        pass

    @abstractmethod
    def log(self, message: str, **kwargs) -> "LogPromptResponse":
        pass

    @abstractmethod
    def info(self, message: str, **kwargs) -> "InfoPromptResponse":
        pass

    @abstractmethod
    def list(self, items: list, **kwargs) -> "ListPromptResponse":
        pass

    @abstractmethod
    def table(self, data: list, **kwargs) -> "TablePromptResponse":
        pass
