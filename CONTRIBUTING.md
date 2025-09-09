# Contributing to LogSentinel

Thank you for your interest in contributing to LogSentinel! This document provides guidelines and information for contributors.

## 🎯 Development Philosophy

LogSentinel is built using **Test-Driven Development (TDD)** principles and follows **SOLID** design principles. Every contribution should maintain these standards.

### Core Principles
- **Test-First Development** - Write tests before implementing features
- **100% Test Coverage** - All code must be tested
- **SOLID Design** - Follow Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles
- **Clean Code** - Write readable, maintainable, and well-documented code

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Git
- Basic understanding of TDD and SOLID principles

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/logsentinel.git
   cd logsentinel
   ```

2. **Build Development Environment**
   ```bash
   docker compose build dev
   ```

3. **Run Tests**
   ```bash
   docker compose run test
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## 🧪 Development Workflow

### TDD Process
1. **Red** - Write a failing test
2. **Green** - Write minimal code to pass the test
3. **Refactor** - Improve code while keeping tests green
4. **Repeat** - Continue for each feature

### Code Quality Standards
- **Type Hints** - All functions and methods must have type hints
- **Documentation** - All public APIs must be documented
- **Linting** - Code must pass all linting checks
- **Formatting** - Code must be formatted with Black and isort

### Testing Requirements
- **Unit Tests** - Test individual components in isolation
- **Integration Tests** - Test component interactions
- **Coverage** - Maintain 100% test coverage
- **Performance Tests** - Include performance benchmarks where applicable

## 📁 Project Structure

```
logsentinel/
├── src/logsentinel/          # Main application code
│   ├── parsers/              # Log parsing modules
│   ├── rules/                # Rules engine
│   ├── alerts/               # Alert system
│   ├── config/               # Configuration management
│   └── main.py               # Main application
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── fixtures/             # Test data
├── rules/                    # Security rules
├── config/                   # Configuration files
└── docs/                     # Documentation
```

## 🔧 Making Changes

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Follow TDD Process
- Write failing tests first
- Implement minimal code to pass tests
- Refactor and improve
- Ensure 100% coverage

### 3. Run Quality Checks
```bash
# Run all tests
docker compose run test

# Run linting
docker compose run dev flake8 src/

# Run type checking
docker compose run dev mypy src/

# Run formatting
docker compose run dev black src/ tests/
docker compose run dev isort src/ tests/
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add new feature description"
```

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

## 📝 Commit Message Format

We follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Maintenance tasks

### Examples
```
feat(parsers): add JSON log parser support
fix(rules): resolve regex pattern validation issue
test(alerts): add unit tests for webhook handler
docs(readme): update installation instructions
```

## 🧪 Testing Guidelines

### Test Structure
```python
def test_feature_should_behavior_when_condition():
    """Test description explaining what is being tested."""
    # Arrange
    setup_test_data()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
```

### Test Categories
- **Unit Tests** - Test individual functions/classes
- **Integration Tests** - Test component interactions
- **End-to-End Tests** - Test complete workflows

### Test Naming
- Use descriptive names that explain the test scenario
- Follow the pattern: `test_[method]_should_[expected_behavior]_when_[condition]`
- Group related tests in classes

## 📚 Documentation

### Code Documentation
- **Docstrings** - All public functions and classes must have docstrings
- **Type Hints** - Use type hints for all function parameters and return values
- **Comments** - Add comments for complex logic

### API Documentation
- Document all public APIs
- Include usage examples
- Specify parameter types and return values

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description** - Clear description of the issue
2. **Steps to Reproduce** - Detailed steps to reproduce the bug
3. **Expected Behavior** - What should happen
4. **Actual Behavior** - What actually happens
5. **Environment** - OS, Python version, Docker version
6. **Logs** - Relevant error logs or stack traces

## 💡 Feature Requests

When requesting features, please include:

1. **Use Case** - Why is this feature needed?
2. **Proposed Solution** - How should it work?
3. **Alternatives** - Other solutions considered
4. **Implementation Ideas** - Technical approach suggestions

## 🔍 Code Review Process

### Review Checklist
- [ ] Tests are comprehensive and pass
- [ ] Code follows SOLID principles
- [ ] Type hints are present and correct
- [ ] Documentation is complete
- [ ] Code is properly formatted
- [ ] No linting errors
- [ ] Performance considerations addressed

### Review Guidelines
- Be constructive and respectful
- Focus on code quality and maintainability
- Suggest improvements rather than just pointing out issues
- Approve when all requirements are met

## 📋 Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass
- [ ] 100% test coverage maintained

## Checklist
- [ ] Code follows SOLID principles
- [ ] Type hints added
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Code formatted with Black/isort
```

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the golden rule

### Getting Help
- Check existing issues and discussions
- Ask questions in GitHub discussions
- Join our community chat (if available)

## 📄 License

By contributing to LogSentinel, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to LogSentinel! 🎉
