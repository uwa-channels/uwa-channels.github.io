---
title: "Code Contribution Guide"
linkTitle: "Code Contribution Guide"
weight: 2
description: >
  A guide for contributing to the MATLAB and Python implementations of the channel replay library, covering setup, coding standards, and pull requests.
cascade:
  - type: "docs"
---

You can contribute by reporting a bug, suggesting a feature, improving the documentation, or changing the code.

This guide covers the MATLAB and Python repositories in the [uwa-channels organization](https://github.com/uwa-channels):

| Repository                                                        | Language         | Main Branch | Folder Layout                      |
| ----------------------------------------------------------------- | ---------------- | ----------- | ---------------------------------- |
| [**uwa-channels/matlab**](https://github.com/uwa-channels/matlab) | MATLAB (R2021a+) | `main`      | `src/`, `tests/`, `examples/`, `packaging/` |
| [**uwa-channels/python**](https://github.com/uwa-channels/python) | Python (≥ 3.10)  | `main`      | `src/uwa_channels/`, `tests/`, `examples/` |

The library's Julia support is hosted separately, in the [`UnderwaterAcoustics.jl`](https://github.com/org-arl/UnderwaterAcoustics.jl) package maintained by the Acoustic Research Laboratory. Please refer to that repository's own contribution guidelines for Julia-specific bug reports and pull requests.

The MATLAB and Python implementations must produce consistent results. The [calibration suite](https://github.com/uwa-channels/calibrations) checks this weekly by running both implementations on the released Zenodo files.

If you change a function's behavior, make the corresponding change in both repositories. Keep argument order, output length, and indexing conventions consistent with each API. In particular, `array_index` starts at 1 in MATLAB and at 0 in Python; preserve the existing convention for `start` as well. The released `.mat` files are fixed, so changes must remain compatible with them.

## Getting started

### Prerequisites

- Familiarity with **Git**, **GitHub**, Markdown, and either MATLAB or Python.\
  Helpful references: [GitHub Quickstart](https://docs.github.com/en/get-started/quickstart), [Markdown Guide](https://www.markdownguide.org/).

- Development environment:

  **MATLAB repository**

  ```bash
  git clone https://github.com/uwa-channels/matlab.git
  ```

  To run example scripts, first download `blue_1.mat` and `blue_noise.mat` from [Zenodo](https://doi.org/10.5281/zenodo.21287414) into `examples/`, then:

  ```matlab
  addpath('src')
  cd examples
  example_replay
  ```

  To run all tests from the repository root (they use `matlab.unittest`, so they need MATLAB with the Signal Processing Toolbox):

  ```bash
  matlab -batch "addpath('src'); assertSuccess(runtests('tests'))"
  ```


  **Python repository**: create a virtual environment and install dependencies:

  ```bash
  git clone https://github.com/uwa-channels/python.git
  cd python
  pip install -r requirements.txt pytest pre-commit
  ```

  To run example scripts, with `blue_1.mat` and `blue_noise.mat` from Zenodo in the working folder:

  ```bash
  PYTHONPATH=src python examples/example_replay.py
  ```

  To run tests:

  ```bash
  PYTHONPATH=src pytest
  ```

  The tests in `tests/test_zenodo.py` replay the released Zenodo files and are skipped by default. Run them with the command below; they download the files to `$UWA_CHANNELS_CACHE`, or to `~/.cache/uwa-channels`:

  ```bash
  PYTHONPATH=src pytest tests/test_zenodo.py --zenodo
  ```

  To initialize `pre-commit`:

  ```bash
  pre-commit install
  pre-commit run --all-files
  ```


### Code of conduct

Treat other contributors respectfully and keep feedback constructive.

## Bug reports, feature requests, and discussions

### Bug reports

- Search existing issues and pull requests; your bug may already be reported or fixed.
- Provide a *minimal, reproducible example* (MATLAB `.m` file or live script, or a Python snippet), along with:
  - Package version: `pip show uwa-channels` in Python; in MATLAB, the `Underwater Acoustic Channel Toolbox` row of `matlab.addons.installedAddons`, or the `VERSION` file in a clone
  - OS and MATLAB/Python version, if relevant

### Feature requests

Explain what you want to do, why it matters, and how the proposed change would help. Include an example API or workflow if useful.

### Discussions

Use [GitHub Discussions](https://github.com/orgs/uwa-channels/discussions) for questions, design ideas, and future plans.

### Issue labels

| Label                            | Meaning                |
| -------------------------------- | ---------------------- |
| `high-priority` / `low-priority` | Relative urgency       |
| `good first issue`               | Suitable for newcomers |
| `breaking-change`                | API/behavior change    |

Issues planned for release are tracked with a GitHub milestone rather than a label.

## Workflow for code and documentation changes

1. **Fork** the repository and clone your fork.
2. **Create a branch** from `main`, named like `topic-short-description` (lowercase, hyphen-separated).
3. **Develop locally**:
   - **MATLAB**: run `addpath('src'); runtests('tests')` from the repository root and address Code Analyzer warnings.
   - **Python**: run `PYTHONPATH=src pytest` frequently.
4. **Write tests** for new features or bug fixes.
5. **Document** your changes:
   - Use NumPy-style docstrings in Python functions and classes.
   - Start each MATLAB function with a help block (H1 line, call forms, inputs, outputs, an example, and a dated revision history), and add a line to the revision history when you change its behavior.
6. **Commit** with clear messages, then push to your fork.
7. **Open a pull request (PR)** against `main`. Mark it as "Draft" if it's not yet ready for review. Reference any related issues.
8. Address reviewer feedback. Once all checks pass and approvals are received, a maintainer will merge.

## Commit message style

Start each commit message with a verb and describe the change. For example:

```text
Start the f_resamp phase ramp at zero, and test that it does
Read MAT v5 files, and fix the beta axis order from h5py
```

## Coding standards

### MATLAB

Follow the [MATLAB Style Guide](https://github.com/eeberhard/matlab_style_guide):

- Four-space indentation, as MATLAB's Smart Indent applies it; `snake_case` for functions, `PascalCase` for classes
- Each function/class in its own `.m` file
- Keep `src/` working on MATLAB R2021a: validate inputs with `assert` in a `validate_inputs` subfunction rather than with `arguments` blocks
- Add unit tests as flat files directly under `tests/` using MATLAB Unit Test
- Vectorize where possible; comment non-obvious logic

### Python

- Formatting is enforced via **Black** and **Ruff** at 88 columns (Ruff handles import sorting, so a separate isort pass is unnecessary)
- Static analysis via **Flake8**, **Ruff**, **mypy**, and **Bandit**
- Use NumPy-style docstrings with LaTeX equations where helpful
- Validate public function inputs with `validate_inputs` before processing. Match the checks in the MATLAB implementation and raise `ValueError` for invalid inputs. Do not use `assert` for validation; Python removes it when run with `-O`.
- Keep functions short, prefer clarity to cleverness, and avoid premature optimization


### Equations in documentation

The same formula needs different delimiters on GitHub and on this site.

- In Markdown that GitHub renders, such as `CONTRIBUTING.md` in the MATLAB and Python repositories, write inline math as ``$`\hat\varphi(nT_s)`$`` and display math in a fenced ` ```math ` block. A bare `$...$` lets GitHub's Markdown run first, which turns `_` into emphasis and `\,` into a comma, and `<` inside math should be written `\lt`.
- On this site, write `$...$` and `$$...$$`. Hugo renders them with its bundled KaTeX when it builds the site, and `params.katex.version` in `config.toml` must name that same KaTeX version, or rules such as the underline in $\hat{\underline{h}}$ are not drawn. The build checks this with `tools/check_katex_css.py`.

## Testing and continuous integration

| Repository | Local Test Command | CI Matrix |
| ---------- | ------------------ | --------- |
| MATLAB     | `matlab -batch "addpath('src'); assertSuccess(runtests('tests'))"` | MATLAB R2021a and latest |
| Python     | `PYTHONPATH=src pytest` | Python 3.10–3.13; Zenodo tests on 3.13 |

**All CI checks must pass before a pull request is merged.**

## Release process

Both repositories follow [Semantic Versioning](https://semver.org/). Do not change the version in a pull request unless a maintainer asks for a release.

- **MATLAB**: bump `VERSION` and the `version` in `CITATION.cff` together, then push a tag `vX.Y.Z` that matches `VERSION`. The release workflow builds `uwa-channels.mltbx` on the latest MATLAB, checks that it installs there and on R2021a, attaches it to a GitHub release, and checks that the one-line install works against it.
- **Python**: bump `version` in `pyproject.toml` and in `CITATION.cff` together on `main`. CI then creates the tag `vX.Y.Z`, publishes a GitHub release with signed distributions, and uploads the package to TestPyPI and PyPI.

## Acknowledgements

This guide draws on the [`UnderwaterAcoustics.jl` contributing guide](https://github.com/org-arl/UnderwaterAcoustics.jl/blob/master/CONTRIBUTING.md), as well as the contribution guidelines of NumPy and SciPy, and the MATLAB Style Guide.
