# Wexample Prompt Package Development Notes

## Overview
The wexample-prompt package aims to be the centralized place for managing all terminal interactions in the Wexample ecosystem. This includes structured messages, data display, and user interactions.

## Core Features from Legacy IOManager

### 1. Log Frame Management
- [ ] Log frame functionality with message history
- [ ] Methods for showing/hiding log frames
- [ ] Log message length tracking
- [ ] Clear last N lines functionality
- [ ] Log frame cleanup and management

### 3. Message Types and Formatting
- [ ] Warning messages with parameters and fatal/trace options
- [ ] Error messages with logger integration
- [ ] Info messages with optional text
- [ ] Command suggestion messages
- [ ] Multiple command suggestions support

### 4. Color System
- [ ] Color theme customization
- [ ] TTY detection for color support

### 5. Verbosity and Logging
- [ ] Verbosity level support
- [ ] Integration with Python logging
- [ ] Command context in log messages
- [ ] Log message filtering by verbosity

### 6. Command Integration
- [ ] Command context support
- [ ] Command suggestion system
- [ ] Next command recommendations
- [ ] Multiple command suggestions

## Planned Improvements

### 1. Structured Data Display

#### Phase 1.1: Data Formatting
- [ ] Table formatting with headers and alignment
- [ ] List rendering with bullets and nesting
- [ ] Tree structure visualization
- [ ] JSON/YAML pretty printing
- [ ] Progress bars with percentage
- [ ] Spinners for async operations
- [ ] Box drawing for messages
- [ ] Section formatting with titles

### 2. User Input Handling

#### Phase 2.1: Input Features
- [ ] Basic input with validation
- [ ] Selection menus (single choice)
- [ ] Multi-select menus
- [ ] Confirmation dialogs
- [ ] Default value support
- [ ] Input history
- [ ] Tab completion

### 3. Enhanced Theme System

#### Phase 3.1: Theme Features
- [ ] Theme customization
- [ ] Style inheritance
- [ ] Complex formatting rules
- [ ] Color scheme management
- [ ] Style composition
- [ ] Theme switching
- [ ] Custom theme creation

### 4. Enhanced IOManager

#### Phase 4.1: Manager Features
- [ ] Automatic format detection
- [ ] Compound outputs
- [ ] Output redirection
- [ ] Terminal size handling
- [ ] Windows compatibility
- [ ] Unicode support
- [ ] Terminal capability detection

## Implementation Priority

1. **Phase 1: Core Features Migration**
   - [ ] Migrate log frame management
   - [ ] Migrate indentation system
   - [ ] Migrate message types
   - [ ] Migrate color system
   - [ ] Migrate verbosity support
   - [ ] Migrate command integration

2. **Phase 2: Enhanced Features**
   - [ ] Implement structured data display
   - [ ] Implement user input handling
   - [ ] Implement enhanced theme system
   - [ ] Implement enhanced IOManager

3. **Phase 3: Integration and Testing**
   - [ ] Set up comprehensive test suite
   - [ ] Add integration tests
   - [ ] Add visual tests for formatting
   - [ ] Add performance tests

## Testing Strategy

### 1. Unit Tests
- [ ] Test each component in isolation
- [ ] Mock terminal interactions
- [ ] Test color rendering
- [ ] Test unicode handling
- [ ] Test Windows compatibility

### 2. Integration Tests
- [ ] Test component interactions
- [ ] Test real terminal behavior
- [ ] Test color schemes
- [ ] Test user input scenarios

### 3. Performance Tests
- [ ] Test large output handling
- [ ] Test memory usage
- [ ] Test response times
- [ ] Test concurrent operations

## Dependencies
- [ ] Evaluate rich library features
- [ ] Consider click library integration
- [ ] Set up pytest environment
- [ ] Set up pytest-mock
- [ ] Consider prompt_toolkit integration

## Notes
- Ensure backward compatibility with legacy IOManager
- Focus on type safety and proper error handling
- Maintain clean separation of concerns
- Document all public APIs thoroughly
- Consider cross-platform compatibility
- Support both TTY and non-TTY environments