# Documentation Guidelines
- Keep documentation concise and dense
- Avoid redundancy and unnecessary explanations
- Focus on technical accuracy and practical examples

This "prompt" package enables the use of an IoManager within application classes to centralize user interactions during terminal prints or logging.

## IoManager Usage
The IoManager enables user interactions during terminal prints or logging via `self.io`.
```python
self.io.info('Info message')
```

Ideally, it should be instantiated once at the application startup and then shared with the other application classes.

## Prompt Context
Classes extending PromptContext have access to IoManager methods with optional prefix and indentation.
```python
self.info('Info message')
```

Other application classes can extend the PromptContext class, which provides methods with the same signature as those in IoManager. The output of these methods may vary slightly depending on the implementing class. For instance, classes that implement PromptContext may add an extra indentation level and prefix messages to enhance clarity for the user.

## Prompt Response
Response types (info, log, success, title, etc.) are defined in:
- Manager: `wexample_prompt/mixins/response/manager/`
- Context: `wexample_prompt/mixins/response/context/`

The manager returns PromptResponse types such as info, log, success, title, table, choice, etc. Each PromptResponse corresponds to a method:
  - In the manager: `self.io.title('My title')`        # ❯ MY TITLE ⫻⫻⫻⫻⫻  
    - This method is defined in `wexample_prompt/mixins/response/manager/` and added to the IoManager class in `common/io_manager.py`
  - In the prompt context: `self.title('My title')`    # ❯ CLASS PREFIX: MY TITLE ⫻⫻⫻⫻⫻  
    - This method is defined in `wexample_prompt/mixins/response/context/` and added via the mixin `mixins/with_prompt_context.py`

## Testing
Each response requires test files in `/tests/`:
- Response class behavior
- IoManager method implementation
- PromptContext implementation

Each Prompt Response has associated test files located in the `/tests/` directory. These tests ensure the proper functioning of the response system at different levels:

- **Response Class Testing**: Tests the standalone response class (e.g., `TitlePromptResponse`)
- **IoManager Method Testing**: Tests the IoManager method implementation (e.g., `io_manager.title()`)
- **PromptContext Implementation Testing**: Tests classes implementing PromptContext with the response method (e.g., `self.title()`)

Example test file structure for the Title response:
```
/tests/responses/titles/test_title_response.py
```

Each test file should cover:
- Response class behavior and properties
- Correct output formatting
- Integration with IoManager
- Proper implementation in PromptContext classes

## Response Registration
Each new Prompt Response type must be registered in the IoManager's `get_response_types()` method to be available in the examples system.

## Example Classes
Each response needs an example class demonstrating:
- Direct response class usage
- IoManager usage
- PromptContext implementation

Each Prompt Response type also comes with an example class that demonstrates its usage in different contexts. These examples are crucial for understanding how the response behaves in various scenarios:

- **Example Class Implementation**: Shows how the response works in a class context
- **Example Manager Usage**: Demonstrates direct usage through the IoManager
- **Example Context Usage**: Shows usage within a PromptContext implementation

Example classes can be found in the response type's associated directory and are automatically executed through the `examples/all.py` script, which runs all available examples for each response type.

Run examples: `python3 examples/all.py`
