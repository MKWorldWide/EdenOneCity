# Contributing to Eden One City

Thank you for your interest in contributing to Eden One City! This document outlines the process for contributing to our project.

## 🚀 Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
   ```bash
   git clone https://github.com/your-username/EdenOneCity.git
   cd EdenOneCity
   ```
3. **Set up** the development environment
   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate

   # Install development dependencies
   pip install -e ".[dev]"
   ```

## 🔧 Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style guidelines (see below)
   - Write tests for new features
   - Update documentation as needed

3. **Run tests and linters**
   ```bash
   # Run tests
   pytest

   # Format code
   black .

   # Check for linting errors
   ruff check .
   ```

4. **Commit your changes**
   - Write clear, concise commit messages
   - Reference any related issues
   ```bash
   git commit -m "feat: add new feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Target the `main` branch
   - Fill out the PR template
   - Request reviews from maintainers

## 📜 Code Style

- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/)
- **Docstrings**: Use Google style docstrings
- **Type Hints**: Use type hints for all function signatures
- **Imports**: Group imports in the following order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports

## 🧪 Testing

- Write tests for all new features and bug fixes
- Use descriptive test names
- Keep tests focused and independent
- Aim for good test coverage (90%+)

## 📚 Documentation

- Update documentation when adding new features
- Keep docstrings up to date
- Add examples for public APIs

## 🐛 Reporting Issues

When reporting issues, please include:
- A clear title and description
- Steps to reproduce the issue
- Expected vs. actual behavior
- Environment details (OS, Python version, etc.)
- Any relevant logs or error messages

## 🤝 Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## 🙏 Thank You!

Your contributions help make Eden One City better for everyone. Thank you for your time and effort!
