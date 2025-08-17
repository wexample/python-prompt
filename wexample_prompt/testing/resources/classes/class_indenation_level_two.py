from wexample_prompt.mixins.with_io_manager import WithIoManager


class ClassIndentationLevelTwo(WithIoManager):
    def print_deep_log_two(self):
        from wexample_prompt.testing.resources.classes.class_indenation_level_three import ClassIndentationLevelThree
        level_two = ClassIndentationLevelThree(io=self.io)
        return level_two.print_deep_log_three()