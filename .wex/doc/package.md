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

## Prompt Response
Response types (info, log, success, title, etc.) are defined in:
- Manager: `wexample_prompt/mixins/response/manager/`

The manager returns PromptResponse types such as info, log, success, title, table, choice, etc. Each PromptResponse corresponds to a method:
  - In the manager: `self.io.title('My title')`        # ❯ MY TITLE ⫻⫻⫻⫻⫻  
    - This method is defined in `wexample_prompt/mixins/response/manager/` and added to the IoManager class in `common/io_manager.py`

## Testing
Each response requires test files in `/tests/`:
- Response class behavior
- IoManager method implementation

Each Prompt Response has associated test files located in the `/tests/` directory. These tests ensure the proper functioning of the response system at different levels:

- **Response Class Testing**: Tests the standalone response class (e.g., `TitlePromptResponse`)
- **IoManager Method Testing**: Tests the IoManager method implementation (e.g., `io_manager.title()`)

Example test file structure for the Title response:
```
/tests/responses/titles/test_title_response.py
```

Each test file should cover:
- Response class behavior and properties
- Correct output formatting
- Integration with IoManager

## Response Registration
Each new Prompt Response type must be registered in the IoManager's `get_response_types()` method to be available in the examples system.

## Example Classes
Each response needs an example class demonstrating:
- Direct response class usage
- IoManager usage

Each Prompt Response type also comes with an example class that demonstrates its usage in different contexts. These examples are crucial for understanding how the response behaves in various scenarios:

- **Example Class Implementation**: Shows how the response works in a class context
- **Example Manager Usage**: Demonstrates direct usage through the IoManager

Example classes can be found in the response type's associated directory and are automatically executed through the `examples/all.py` script, which runs all available examples for each response type.

Run examples: `python3 examples/all.py`
