---
title: "Code Contribution Guide"
linkTitle: "Code Contribution Guide"
weight: 2
description: >
cascade:
  - type: "docs"
---

## Contributing to **UWA-Channels** (MATLAB & Python)

First off — thank you for considering a contribution! Bug reports, feature requests, documentation improvements, and code changes are all welcome.

This guide explains how to contribute effectively to the two companion repositories hosted at [https://github.com/uwa-channels](https://github.com/uwa-channels):

| Repository                                                        | Language         | Main Branch | Folder Layout                      |
| ----------------------------------------------------------------- | ---------------- | ----------- | ---------------------------------- |
| [**uwa-channels/matlab**](https://github.com/uwa-channels/matlab) | MATLAB (R2021a+) | `main`      | `src/`, `tests/`, `examples/`      |
| [**uwa-channels/python**](https://github.com/uwa-channels/python) | Python (≥ 3.10)  | `main`      | `uwa_channels/`, `tests/`, `docs/` |

## Getting Started

### Prerequisites

- Familiarity with **Git**, **GitHub**, Markdown, and either MATLAB or Python.\
  Helpful references: [GitHub Quickstart](https://docs.github.com/en/get-started/quickstart), [Markdown Guide](https://www.markdownguide.org/).

- Development environment:

  **MATLAB repository**

  ```bash
  git clone https://github.com/uwa-channels/matlab.git
  ```

  To run example scripts:

  ```matlab
  cd examples
  example_replay
  ```

  To run tests:

  ```matlab
  cd tests
  addpath('../src')
  runtests('testReplay')
  ```


  **Python repository** — create a virtual environment and install dependencies:

  ```bash
  git clone https://github.com/uwa-channels/python.git
  cd python
  pip install numpy scipy matplotlib h5py pytest pytest-benchmark pre-commit
  ```

  To run example scripts:

  ```bash
  PYTHONPATH=src python examples/example_replay.py
  ```

  To run tests:

  ```bash
  PYTHONPATH=src pytest
  ```

  To initialize `pre-commit`:

  ```bash
  pre-commit install
  pre-commit run --all-files
  ```

  
### Code of Conduct

We expect all contributors to be **professional, respectful, and constructive**. By participating, you agree to uphold these standards.

## Bug Reports, Feature Requests, & Discussions

### Bug Reports

- Search existing issues and pull requests—your bug may already be reported or fixed.
- Provide a *minimal, reproducible example* (MATLAB `.m` file or live script, or a Python snippet), along with:
  - Package versions (`uwa_channels.__version__` or MATLAB `ver`)
  - OS and MATLAB/Python version, if relevant

### Feature Requests

Describe both the *motivation* and the *proposed change*. Sketch a possible API or workflow if applicable.

### Discussions

General Q&A, design ideas, and roadmap conversations belong in [**GitHub Discussions**](https://github.com/orgs/uwa-channels/discussions), not in Issues.

### Issue Labels

| Label                            | Meaning                |
| -------------------------------- | ---------------------- |
| `high-priority` / `low-priority` | Relative urgency       |
| `good first issue`               | Suitable for newcomers |
| `breaking-change`                | API/behavior change    |
| Milestone assigned               | Planned for release    |

## Workflow for Code & Documentation Changes

1. **Fork** the repository and clone your fork.
2. **Create a branch** from `main`, named like `topic-short-description` (lowercase, hyphen-separated).
3. **Develop locally**:
   - **MATLAB** — run `runtests('tests')` and address Code Analyzer (MLint) warnings.
   - **Python** — run `PYTHONPATH=src pytest` frequently.
4. **Write tests** for new features or bug fixes.
5. **Document** your changes:
   - Use NumPy-style docstrings in Python functions and classes.
   - Use MATLAB help text headers; add usage examples for public APIs.
6. **Commit** with clear messages, then push to your fork.
7. **Open a pull request (PR)** against `main`. Mark it as "Draft" if it's not yet ready for review. Reference any related issues.
8. Address reviewer feedback. Once all checks pass and approvals are received, a maintainer will merge.

## Commit Message Style

We follow a simplified version of [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <summary>

<body>
```

- **type** ∈ {`feat`, `fix`, `docs`, `test`, `perf`, `refactor`, `style`, `chore`, `revert`}
- **scope** identifies the module or subsystem (e.g., `io`, `replay`, `noisegen`)
- Use imperative mood for the summary (e.g., “add support…” not “added”)
- Limit the summary to ≤ 50 characters; wrap the body at 72 characters
- If the change is breaking, begin the body with `BREAKING CHANGE:`

**Examples:**

```text
feat(replay): add resampling support for replay channels
fix(io): handle empty .mat files (issue #42)
```

## Coding Standards

### MATLAB, follow the [MATLAB Style Guide](https://github.com/eeberhard/matlab_style_guide):

- 4-space indentation; `camelCase` for functions, `PascalCase` for classes
- Each function/class in its own `.m` file
- Use `arguments` blocks for input validation where possible
- Add unit tests under `tests/testPkgName/` using MATLAB Unit Test
- Vectorize where possible; comment non-obvious logic

### Python

- Formatting is enforced via **Black** and **isort**
- Static analysis via **Flake8** and **Ruff**
- Use NumPy-style doc strings with LaTeX equations where helpful
- Keep functions short, prefer clarity to cleverness, and avoid premature optimization


## Testing & Continuous Integration

| Repository | Local Test Command      | CI Matrix                |
| ---------- | ----------------------- | ------------------------ |
| Python     | `PYTHONPATH=src pytest` | Python 3.10 – 3.12       |
| MATLAB     | `runtests('tests')`     | MATLAB R2021a and latest |

**All CI checks must pass before a pull request is merged.**

## Release Process (Python only)

Maintainers tag releases using `git tag -s vX.Y.Z` following [Semantic Versioning (SemVer)](https://semver.org/).

Merged PRs are reflected in `CHANGELOG.md`, with entries auto-generated from commit messages.

## Acknowledgments

This guide was inspired by the excellent [`UnderwaterAcoustics.jl` contributing guide](https://github.com/org-arl/UnderwaterAcoustics.jl/blob/master/CONTRIBUTING.md), as well as the contribution guidelines from `NumPy`, `SciPy`, and `MATLAB Style Guide`.

*Happy hacking -- may your channels be peaceful and your SNR high!*
