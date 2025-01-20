# Development Style Guide

## How to modify this file

- Respect existing content - correct typos but don't extensively rewrite content
- Add only essential missing information - request further specifics if needed - add only the content we have been requested to do
- Don't add extra section titles or subtitles
- Be as concise as possible - avoid listing every file or type
- Check for instruction redundancy
- Write in English
- Keep instructions project-specific - avoid general development practices

## Code Organization

### File Structure
- Each class in a separate file using snake_case naming
- File name must match class name in snake_case
- Group related files in appropriate subdirectories

### Class Structure
- Use Pydantic models for data validation
- Define class-level type hints using ClassVar
- Order methods: class methods first, then instance methods
- Implement create() classmethod for instantiation
- Keep rendering logic in render() method

## Code Style

### Type Hints
- Use type hints for all function parameters and return values
- Use Optional[] for nullable value, use Union[] for multiple types

### Pydantic Usage
- Use Pydantic models for data validation following best practices
- Define Config class for model customization
- Use validator decorators for complex validations
- Use `pydantic.ConfigDict` instead of class-based Config (required for Pydantic v2+)

### Error Handling
- Use ErrorContext for error management
- Never expose raw tracebacks to end users

## Testing

### Structure
- Tests directory mirrors package structure
- Test class names must match source class with "test_" prefix
- Test all response rendering scenarios

## Demo
- Like test, every feature should have an implementation in the examples/demo.py file