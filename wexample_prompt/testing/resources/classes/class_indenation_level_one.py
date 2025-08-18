from wexample_prompt.mixins.with_io_manager import WithIoManager


class ClassIndentationLevelOne(WithIoManager):
    def print_deep_log_one(self):
        from wexample_prompt.testing.resources.classes.class_indenation_level_two import ClassIndentationLevelTwo

        self.io.log('test deep log one', context=self.io_context)

        level_two = ClassIndentationLevelTwo(
            parent_io_handler=self
        )

        level_two.print_deep_log_two()
