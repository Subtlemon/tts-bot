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
* `sudo apt-get install ffmpeg`
* `sudo apt-get install libopus0`

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

## Discord Bot Setup

### Create a Discord Bot

Follow instructions online, such as https://realpython.com/how-to-make-a-discord-bot-python/.

### Token

Create a .env file in the root directory and put your token in it:
```
# .env
DISCORD_TOKEN={your-bot-token}
```

### Google Cloud Text-To-Speech

We use the Google Cloud Text-To-Speech API. For local development, download service account credentials following [these instructions](https://cloud.google.com/text-to-speech/docs/libraries#setting_up_authentication) and point the GOOGLE_APPLICATION_CREDENTIALS environment variable to the downloaded file.

### Run the bot

From the root directory (same directory that this README is in), run:

```
python -m main
```
