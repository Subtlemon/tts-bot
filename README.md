# Setup

## Repository setup

1. Add the git hooks.
   ```bash
   git config core.hooksPath .githooks
   ```
   * This will enable pre-commit checks.

## Python environment

### Prerequisites

* Anaconda3

### Import environment

```bash
conda env create -f environment.yml
```

### Update environment

Updates the current environment to be consistent with `environment.yml`.
```bash
conda env update --file environment.yml --prune
```

The `--prune` option likely does not work correctly for pip packages. To ensure that an environment is perfectly in sync with the yml, use:
```bash
conda env create --force -f environment.yml
```

### Export environment

Updates the `environment.yml` from the current environment.
```bash
conda env export | grep -v "^prefix: " > environment.yml
```

### Activate environment

```bash
conda activate tts_bot
```