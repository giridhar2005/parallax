# Contributing to Parallax

Thank you for your interest in improving Parallax.

## Development Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:giridhar2005/parallax.git
   cd parallax
   ```
2. Set up local virtual environment and dependencies:
   ```bash
   make setup
   ```
3. Seed the forensic case fixture data:
   ```bash
   make fixture
   ```
4. Run the test suite:
   ```bash
   make test
   ```
5. Check code formatting and linting:
   ```bash
   make lint
   ```

## Pull Request Guidelines

- All backend changes must maintain 100% passing tests in `tests/`.
- Frontend code must build cleanly without TypeScript errors (`npm run build`).
- Keep code clean, typed, and well-documented.
