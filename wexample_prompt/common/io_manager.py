from wexample_helpers.classes.extended_base_model import ExtendedBaseModel

from wexample_prompt.mixins.response.manager.messages.log_prompt_response_manager_mixin import \
    LogPromptResponseManagerMixin

class IoManager(
    ExtendedBaseModel,
    # Messages
    LogPromptResponseManagerMixin,
):
    pass
