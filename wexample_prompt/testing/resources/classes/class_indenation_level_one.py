from wexample_prompt.mixins.with_io_manager import WithIoManager


class ClassIndentationLevelOne(WithIoManager):
    def print_deep_log_one(self):
        from wexample_prompt.testing.resources.classes.class_indenation_level_two import ClassIndentationLevelTwo
        level_two = ClassIndentationLevelTwo(io=self.io)

        self.io.log('test deep log one')

        return level_two.print_deep_log_two()
