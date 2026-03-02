# Contributing to Local Passkeeper

Thank you for your interest in contributing to Local Passkeeper! We welcome contributions from the community and are grateful for your support.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Security](#security)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome people of all backgrounds and identities
- **Be collaborative**: Work together towards common goals
- **Be professional**: Maintain professional conduct in all interactions

## Getting Started

### Prerequisites

- Rust 1.75 or later
- Git
- A GitHub account

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/local-passkeeper.git
   cd local-passkeeper
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/LuisE503/local-passkeeper.git
   ```

4. **Install dependencies and build**:
   ```bash
   cargo build
   ```

5. **Run tests**:
   ```bash
   cargo test --all
   ```

## Development Process

### Branching Strategy

- `main` - Stable release branch
- `develop` - Development branch for next release
- `feature/xyz` - Feature branches
- `bugfix/xyz` - Bug fix branches
- `hotfix/xyz` - Critical hotfix branches

### Workflow

1. **Create a branch** from `develop`:
   ```bash
   git checkout develop
   git pull upstream develop
   git checkout -b feature/my-feature
   ```

2. **Make your changes** with clear, focused commits

3. **Keep your branch updated**:
   ```bash
   git fetch upstream
   git rebase upstream/develop
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/my-feature
   ```

5. **Open a Pull Request** against the `develop` branch

## Coding Standards

### Rust Style Guide

We follow the official [Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/):

- Use `rustfmt` for code formatting:
  ```bash
  cargo fmt
  ```

- Use `clippy` for linting:
  ```bash
  cargo clippy -- -D warnings
  ```

### Code Quality

- **Write clear, self-documenting code**: Use descriptive names for variables, functions, and types
- **Add comments for complex logic**: Explain *why*, not *what*
- **Keep functions small and focused**: Each function should do one thing well
- **Handle errors properly**: Use `Result` types and meaningful error messages
- **Avoid unsafe code**: Only use `unsafe` when absolutely necessary and document why

### Documentation

- Add doc comments to public APIs:
  ```rust
  /// Brief description of what the function does
  ///
  /// # Arguments
  ///
  /// * `param` - Description of the parameter
  ///
  /// # Returns
  ///
  /// Description of the return value
  ///
  /// # Examples
  ///
  /// ```
  /// use passkeeper_core::example_function;
  /// let result = example_function(42);
  /// ```
  pub fn example_function(param: i32) -> Result<String> {
      // implementation
  }
  ```

- Keep README files up to date
- Update CHANGELOG.md for notable changes

## Testing

### Running Tests

```bash
# Run all tests
cargo test --all

# Run tests for a specific package
cargo test --package passkeeper-core

# Run with output
cargo test -- --nocapture

# Run with coverage
cargo tarpaulin --out Html
```

### Writing Tests

- Write unit tests in the same file as the code:
  ```rust
  #[cfg(test)]
  mod tests {
      use super::*;

      #[test]
      fn test_example() {
          assert_eq!(2 + 2, 4);
      }
  }
  ```

- Write integration tests in the `tests/` directory
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use meaningful test names that describe what is being tested

## Submitting Changes

### Pull Request Guidelines

1. **Ensure all tests pass**:
   ```bash
   cargo test --all
   cargo clippy -- -D warnings
   cargo fmt -- --check
   ```

2. **Update documentation** if needed

3. **Write a clear PR description**:
   - What changes were made?
   - Why were these changes necessary?
   - Are there any breaking changes?
   - Related issues (use "Closes #123" to auto-close)

4. **Keep PRs focused**: One feature/fix per PR

5. **Be responsive**: Address review comments promptly

### Commit Message Format

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example**:
```
feat(cli): add password strength indicator

Add visual password strength indicator to the CLI
when generating new passwords.

Closes #123
```

## What to Contribute

### Good First Issues

Look for issues labeled `good first issue` - these are great for newcomers!

### Areas for Contribution

- **Features**: Implement new functionality from the roadmap
- **Bug fixes**: Fix reported bugs
- **Documentation**: Improve or translate documentation
- **Tests**: Add test coverage
- **Performance**: Optimize slow code
- **Security**: Find and fix security issues
- **UI/UX**: Improve user experience

### Feature Requests

Before implementing a new feature:

1. Open an issue to discuss the feature
2. Wait for maintainer feedback
3. Get agreement on the approach
4. Implement the feature

## Security

**Never commit**:
- Vault files (`.vault`)
- Real credentials
- API keys or secrets
- Private keys

If you discover a security vulnerability, please see [SECURITY.md](SECURITY.md) for reporting procedures.

## Questions?

- Open a [Discussion](https://github.com/LuisE503/local-passkeeper/discussions)
- Ask in an existing issue
- Contact the maintainers

## License

By contributing to Local Passkeeper, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
