# Contributing to Azure Function Chat API

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Use the issue template if available
- Include detailed information about the problem
- Provide steps to reproduce
- Include relevant logs or screenshots

### Suggesting Enhancements

- Open an issue with your suggestion
- Explain the use case and benefits
- Be open to discussion and feedback

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation as needed

4. **Run tests**
   ```bash
   pytest tests/ -v
   ```

5. **Run linting**
   ```bash
   flake8 function_app.py
   mypy function_app.py --ignore-missing-imports
   ```

6. **Format code**
   ```bash
   black .
   ```

7. **Commit your changes**
   ```bash
   git commit -m "feat: add new feature"
   ```

8. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **Open a Pull Request**

## 📝 Coding Standards

### Python Style Guide

- Follow PEP 8 style guide
- Use Black for code formatting (88 character line length)
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Use type hints where appropriate

### Example:

```python
def process_chat_message(message: str, user_id: str = "anonymous") -> dict:
    """
    Process a chat message and return a response.
    
    Args:
        message: The chat message to process
        user_id: Optional user identifier
        
    Returns:
        Dictionary containing the response data
    """
    # Implementation
    pass
```

### Git Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example:
```
feat: add authentication to chat endpoint

- Implement JWT token validation
- Add user authentication middleware
- Update tests for authenticated endpoints
```

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

### Example:

```python
def test_chat_api_with_valid_message():
    """Test chat API with a valid message"""
    # Arrange
    req = func.HttpRequest(
        method='POST',
        url='/api/chat',
        body=json.dumps({'message': 'Hello'}).encode('utf-8')
    )
    
    # Act
    response = chat_api(req)
    
    # Assert
    assert response.status_code == 200
    assert 'success' in response.get_body().decode('utf-8')
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=function_app --cov-report=html

# Run specific test
pytest tests/test_chat_api.py::TestChatAPI::test_chat_api_success -v
```

## 📚 Documentation

- Update README.md for user-facing changes
- Add code comments for complex logic
- Update API documentation
- Include examples where helpful

## 🔍 Code Review Process

1. All submissions require review
2. Address reviewer comments
3. Keep PRs focused and small
4. Be responsive to feedback
5. Be respectful and constructive

## 🚀 Release Process

1. Version bumps follow Semantic Versioning (SemVer)
2. Update CHANGELOG.md
3. Tag releases in git
4. Deploy to staging first
5. Verify in staging
6. Deploy to production

## 📋 Checklist for Pull Requests

- [ ] Code follows project style guidelines
- [ ] Tests added for new functionality
- [ ] All tests pass locally
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts
- [ ] Branch is up to date with main

## 🏷️ Labels

- `bug` - Bug fixes
- `enhancement` - New features or improvements
- `documentation` - Documentation changes
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Questions or discussions

## 💬 Communication

- Be respectful and inclusive
- Ask questions if unclear
- Provide constructive feedback
- Help others learn

## 📞 Getting Help

- Open an issue for questions
- Tag maintainers with @username
- Join discussions in pull requests

## 📜 License

By contributing, you agree that your contributions will be licensed under the project's license.

---

Thank you for contributing! 🎉
