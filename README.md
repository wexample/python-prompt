# prompt

Version: 13.1.1

Helper for your tty interactions

## Table of Contents

- [Tests](#tests)
- [Suite Integration](#suite-integration)
- [Dependencies](#dependencies)
- [Versioning](#versioning)
- [License](#license)
- [Suite Integration](#suite-integration)
- [Suite Signature](#suite-signature)
- [Basic Usage](#basic-usage)
- [Introduction](#introduction)
- [Roadmap](#roadmap)
- [Status Compatibility](#status-compatibility)
- [Useful Links](#useful-links)
- [Migration Notes](#migration-notes)

## Tests

Run the test suite:

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=prompt tests/
```

## Integration in the Suite

This package is part of the Wexample Suite — a collection of high-quality, modular tools designed to work seamlessly together across multiple languages and environments.

### Related Packages

The suite includes packages for configuration management, file handling, prompts, and more. Each package can be used independently or as part of the integrated suite.

Visit the [Wexample Suite documentation](https://docs.wexample.com) for the complete package ecosystem.

## Dependencies

- attrs: >=23.1.0
- cattrs: >=23.1.0
- colorama: 
- readchar: 
- wcwidth: 
- wexample-helpers: >=16.0.0

## Versioning & Compatibility Policy

Wexample packages follow **Semantic Versioning** (SemVer):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

We maintain backward compatibility within major versions and provide clear migration guides for breaking changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Free to use in both personal and commercial projects.

## Integration in the Suite

This package is part of the Wexample Suite — a collection of high-quality, modular tools designed to work seamlessly together across multiple languages and environments.

### Related Packages

The suite includes packages for configuration management, file handling, prompts, and more. Each package can be used independently or as part of the integrated suite.

Visit the [Wexample Suite documentation](https://docs.wexample.com) for the complete package ecosystem.

# About us

[Wexample](https://wexample.com) stands as a cornerstone of the digital ecosystem — a collective of seasoned engineers, researchers, and creators driven by a relentless pursuit of technological excellence. More than a media platform, it has grown into a vibrant community where innovation meets craftsmanship, and where every line of code reflects a commitment to clarity, durability, and shared intelligence.

This packages suite embodies this spirit. Trusted by professionals and enthusiasts alike, it delivers a consistent, high-quality foundation for modern development — open, elegant, and battle-tested. Its reputation is built on years of collaboration, refinement, and rigorous attention to detail, making it a natural choice for those who demand both robustness and beauty in their tools.

Wexample cultivates a culture of mastery. Each package, each contribution carries the mark of a community that values precision, ethics, and innovation — a community proud to shape the future of digital craftsmanship.

## Prompt IO Quickstart

### WithIoManager: owning or sharing the IoManager
- Any class that needs prompt output should inherit `WithIoManager`.
- Call `self.ensure_io_manager()` to lazily create or reuse an `IoManager`.
- To inherit a parent’s indentation/verbosity, call `self.set_parent_io_handler(parent)`; every context you create is automatically nested +1.
- If someone else instantiates the manager, call `self.use_io_manager(io)` to reuse it instead of creating a new instance.

### WithIoMethods: direct method proxies
- Mix in `WithIoMethods` when you want to call `self.log(...)`, `self.separator(...)`, etc., without reaching into `self.io`.
- The mixin delegates missing attribute lookups to the underlying `IoManager`, and it automatically injects `context=self.create_io_context()` so nested logging just works.

### Typical pattern
```python
from wexample_prompt.mixins.with_io_methods import WithIoMethods

class Worker(WithIoMethods):
    def __attrs_post_init__(self):
        self.ensure_io_manager()          # Owns an IoManager

    def run(self):
        self.log("top level message")     # via WithIoMethods

class Child(WithIoMethods):
    def __attrs_post_init__(self, parent):
        self.set_parent_io_handler(parent)  # reuse & indent

    def run(self):
        self.log("nested message")
```

The executor or parent decides whether to create a fresh manager or cascade an existing one; children only call `ensure_io_manager()` and never worry about the init order.

# prompt

Version: 6.1.2

Helper for your tty interactions

## Table of Contents

- [Tests](#tests)
- [Suite Integration](#suite-integration)
- [Dependencies](#dependencies)
- [Versioning](#versioning)
- [License](#license)
- [Suite Integration](#suite-integration)
- [Suite Signature](#suite-signature)
- [Basic Usage](#basic-usage)
- [Introduction](#introduction)
- [Roadmap](#roadmap)
- [Status Compatibility](#status-compatibility)
- [Useful Links](#useful-links)
- [Migration Notes](#migration-notes)

## Tests

Run the test suite:

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=prompt tests/
```

## Integration in the Suite

This package is part of the Wexample Suite — a collection of high-quality, modular tools designed to work seamlessly together across multiple languages and environments.

### Related Packages

The suite includes packages for configuration management, file handling, prompts, and more. Each package can be used independently or as part of the integrated suite.

Visit the [Wexample Suite documentation](https://docs.wexample.com) for the complete package ecosystem.

## Dependencies

- attrs: >=23.1.0
- cattrs: >=23.1.0
- colorama: 
- inquirerpy: 
- readchar: 
- wcwidth: 
- wexample-helpers: >=8.0.0

## Versioning & Compatibility Policy

Wexample packages follow **Semantic Versioning** (SemVer):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

We maintain backward compatibility within major versions and provide clear migration guides for breaking changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Free to use in both personal and commercial projects.

## Integration in the Suite

This package is part of the Wexample Suite — a collection of high-quality, modular tools designed to work seamlessly together across multiple languages and environments.

### Related Packages

The suite includes packages for configuration management, file handling, prompts, and more. Each package can be used independently or as part of the integrated suite.

Visit the [Wexample Suite documentation](https://docs.wexample.com) for the complete package ecosystem.

# About us

[Wexample](https://wexample.com) stands as a cornerstone of the digital ecosystem — a collective of seasoned engineers, researchers, and creators driven by a relentless pursuit of technological excellence. More than a media platform, it has grown into a vibrant community where innovation meets craftsmanship, and where every line of code reflects a commitment to clarity, durability, and shared intelligence.

This packages suite embodies this spirit. Trusted by professionals and enthusiasts alike, it delivers a consistent, high-quality foundation for modern development — open, elegant, and battle-tested. Its reputation is built on years of collaboration, refinement, and rigorous attention to detail, making it a natural choice for those who demand both robustness and beauty in their tools.

Wexample cultivates a culture of mastery. Each package, each contribution carries the mark of a community that values precision, ethics, and innovation — a community proud to shape the future of digital craftsmanship.

## Prompt IO Quickstart

### WithIoManager: owning or sharing the IoManager
- Any class that needs prompt output should inherit `WithIoManager`.
- Call `self.ensure_io_manager()` to lazily create or reuse an `IoManager`.
- To inherit a parent’s indentation/verbosity, call `self.set_parent_io_handler(parent)`; every context you create is automatically nested +1.
- If someone else instantiates the manager, call `self.use_io_manager(io)` to reuse it instead of creating a new instance.

### WithIoMethods: direct method proxies
- Mix in `WithIoMethods` when you want to call `self.log(...)`, `self.separator(...)`, etc., without reaching into `self.io`.
- The mixin delegates missing attribute lookups to the underlying `IoManager`, and it automatically injects `context=self.create_io_context()` so nested logging just works.

### Typical pattern
```python
from wexample_prompt.mixins.with_io_methods import WithIoMethods

class Worker(WithIoMethods):
    def __attrs_post_init__(self):
        self.ensure_io_manager()          # Owns an IoManager

    def run(self):
        self.log("top level message")     # via WithIoMethods

class Child(WithIoMethods):
    def __attrs_post_init__(self, parent):
        self.set_parent_io_handler(parent)  # reuse & indent

    def run(self):
        self.log("nested message")
```

The executor or parent decides whether to create a fresh manager or cascade an existing one; children only call `ensure_io_manager()` and never worry about the init order.

# prompt

Version: 2.0.0

Helper for your tty interactions

## Table of Contents

- [Tests](#tests)
- [Suite Integration](#suite-integration)
- [Dependencies](#dependencies)
- [Versioning](#versioning)
- [License](#license)
- [Suite Integration](#suite-integration)
- [Suite Signature](#suite-signature)
- [Basic Usage](#basic-usage)
- [Roadmap](#roadmap)
- [Status Compatibility](#status-compatibility)
- [Useful Links](#useful-links)
- [Migration Notes](#migration-notes)

## Tests

Run the test suite:

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=prompt tests/
```

## Integration in the Suite

This package is part of the Wexample Suite — a collection of high-quality, modular tools designed to work seamlessly together across multiple languages and environments.

### Related Packages

The suite includes packages for configuration management, file handling, prompts, and more. Each package can be used independently or as part of the integrated suite.

Visit the [Wexample Suite documentation](https://docs.wexample.com) for the complete package ecosystem.

## Dependencies

- attrs: >=23.1.0
- cattrs: >=23.1.0
- colorama: 
- inquirerpy: 
- readchar: 
- wcwidth: 
- wexample-helpers: >=1.1.0

## Versioning & Compatibility Policy

Wexample packages follow **Semantic Versioning** (SemVer):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

We maintain backward compatibility within major versions and provide clear migration guides for breaking changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Free to use in both personal and commercial projects.

## Integration in the Suite

This package is part of the Wexample Suite — a collection of high-quality, modular tools designed to work seamlessly together across multiple languages and environments.

### Related Packages

The suite includes packages for configuration management, file handling, prompts, and more. Each package can be used independently or as part of the integrated suite.

Visit the [Wexample Suite documentation](https://docs.wexample.com) for the complete package ecosystem.

# About us

[Wexample](https://wexample.com) stands as a cornerstone of the digital ecosystem — a collective of seasoned engineers, researchers, and creators driven by a relentless pursuit of technological excellence. More than a media platform, it has grown into a vibrant community where innovation meets craftsmanship, and where every line of code reflects a commitment to clarity, durability, and shared intelligence.

This packages suite embodies this spirit. Trusted by professionals and enthusiasts alike, it delivers a consistent, high-quality foundation for modern development — open, elegant, and battle-tested. Its reputation is built on years of collaboration, refinement, and rigorous attention to detail, making it a natural choice for those who demand both robustness and beauty in their tools.

Wexample cultivates a culture of mastery. Each package, each contribution carries the mark of a community that values precision, ethics, and innovation — a community proud to shape the future of digital craftsmanship.

## Prompt IO Quickstart

### WithIoManager: owning or sharing the IoManager
- Any class that needs prompt output should inherit `WithIoManager`.
- Call `self.ensure_io_manager()` to lazily create or reuse an `IoManager`.
- To inherit a parent’s indentation/verbosity, call `self.set_parent_io_handler(parent)`; every context you create is automatically nested +1.
- If someone else instantiates the manager, call `self.use_io_manager(io)` to reuse it instead of creating a new instance.

### WithIoMethods: direct method proxies
- Mix in `WithIoMethods` when you want to call `self.log(...)`, `self.separator(...)`, etc., without reaching into `self.io`.
- The mixin delegates missing attribute lookups to the underlying `IoManager`, and it automatically injects `context=self.create_io_context()` so nested logging just works.

### Typical pattern
```python
from wexample_prompt.mixins.with_io_methods import WithIoMethods

class Worker(WithIoMethods):
    def __attrs_post_init__(self):
        self.ensure_io_manager()          # Owns an IoManager

    def run(self):
        self.log("top level message")     # via WithIoMethods

class Child(WithIoMethods):
    def __attrs_post_init__(self, parent):
        self.set_parent_io_handler(parent)  # reuse & indent

    def run(self):
        self.log("nested message")
```

The executor or parent decides whether to create a fresh manager or cascade an existing one; children only call `ensure_io_manager()` and never worry about the init order.

## Known Limitations & Roadmap

Current limitations and planned features are tracked in the GitHub issues.

See the [project roadmap](https://github.com/wexample/python-prompt/issues) for upcoming features and improvements.

## Status & Compatibility

**Maturity**: Production-ready

**Python Support**: >=3.10

**OS Support**: Linux, macOS, Windows

**Status**: Actively maintained

## Useful Links

- **Homepage**: https://github.com/wexample/python-prompt
- **Documentation**: [docs.wexample.com](https://docs.wexample.com)
- **Issue Tracker**: https://github.com/wexample/python-prompt/issues
- **Discussions**: https://github.com/wexample/python-prompt/discussions
- **PyPI**: [pypi.org/project/prompt](https://pypi.org/project/prompt/)

## Migration Notes

When upgrading between major versions, refer to the migration guides in the documentation.

Breaking changes are clearly documented with upgrade paths and examples.

## Known Limitations & Roadmap

Current limitations and planned features are tracked in the GitHub issues.

See the [project roadmap](https://github.com/wexample/python-prompt/issues) for upcoming features and improvements.

## Status & Compatibility

**Maturity**: Production-ready

**Python Support**: >=3.10

**OS Support**: Linux, macOS, Windows

**Status**: Actively maintained

## Useful Links

- **Homepage**: https://github.com/wexample/python-prompt
- **Documentation**: [docs.wexample.com](https://docs.wexample.com)
- **Issue Tracker**: https://github.com/wexample/python-prompt/issues
- **Discussions**: https://github.com/wexample/python-prompt/discussions
- **PyPI**: [pypi.org/project/prompt](https://pypi.org/project/prompt/)

## Migration Notes

When upgrading between major versions, refer to the migration guides in the documentation.

Breaking changes are clearly documented with upgrade paths and examples.

## Known Limitations & Roadmap

Current limitations and planned features are tracked in the GitHub issues.

See the [project roadmap](https://github.com/wexample/python-prompt/issues) for upcoming features and improvements.

## Status & Compatibility

**Maturity**: Production-ready

**Python Support**: >=3.10

**OS Support**: Linux, macOS, Windows

**Status**: Actively maintained

## Useful Links

- **Homepage**: https://github.com/wexample/python-prompt
- **Documentation**: [docs.wexample.com](https://docs.wexample.com)
- **Issue Tracker**: https://github.com/wexample/python-prompt/issues
- **Discussions**: https://github.com/wexample/python-prompt/discussions
- **PyPI**: [pypi.org/project/prompt](https://pypi.org/project/prompt/)

## Migration Notes

When upgrading between major versions, refer to the migration guides in the documentation.

Breaking changes are clearly documented with upgrade paths and examples.
