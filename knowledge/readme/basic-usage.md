## Basic Usage

### Writing Styled Messages

The prompt system now understands an inline markup that lets you tweak colors and styles without touching the underlying response classes. Use the `@color:...{...}` directive inside any message string:

```
Hello @color:red{World}
```

You can combine multiple modifiers by separating them with `+`. The markup accepts any `TerminalColor` member (case-insensitive, `-` and `_` are interchangeable) and any `TextStyle` value:

```
@color:blue+bold{Primary}
@color:yellow+underline{Highlight}
@color:light_green+bold+underline{Important}
```

Nested directives inherit the currently active styles, making it easy to accent parts of a sentence:

```
@color:cyan+bold{Outer @color:yellow{Inner} and back}
```

Break lines as usual—each newline delimits a new `PromptResponseLine` while keeping the active styles:

```
@color:magenta+bold{Title line}
Second line keeps magenta bold unless overridden
```

If the markup is malformed (missing closing brace, unknown modifier), the raw text is preserved so you can fix it without breaking rendering.

You can also use emoji shorthand instead of the explicit `color:` prefix for the base colors:

```
@🔵+bold{Blue headline}
@🟢{Success}
@🔴{Failure}
```

Both syntaxes can be mixed freely inside the same string.

### Manager Helpers

All `IoManager` helpers mirror their response factory signatures, so you can pass new styling arguments directly. For example, every message-level helper accepts an optional `color=...` argument:

```python
io.success("Done!", color=TerminalColor.GREEN)
io.error("Oops", exception=err, color=TerminalColor.RED)
io.choice("Pick one:", choices=["a", "b"], color=TerminalColor.CYAN)
```

Optional parameters stay explicit on the helper signature—no need to rely on `**kwargs`, and missing arguments surface immediately in tests.
