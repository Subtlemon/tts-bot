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
GOOGLE_APPLICATION_CREDENTIALS={path to key file}
TTS_SPECIAL_CLIENT_URL={URL for the special client's HTTP endpoint}
```

If `TTS_SPECIAL_CLIENT_URL` is unset, special voices will be disabled and removed from the list of voices.

### Google Cloud Text-To-Speech

We use the Google Cloud Text-To-Speech API. You must enable the API and set up authentication: https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#before-you-begin

For local development, download service account credentials following [these instructions](https://cloud.google.com/text-to-speech/docs/libraries#setting_up_authentication) and point the GOOGLE_APPLICATION_CREDENTIALS environment variable to the downloaded file.

If you are running the bot on Google Compute Engine, enable authenitcation by selecting "Allow full access to all Cloud APIs" during VM creation or while editing a stopped VM.

### Run the bot

From the root directory (same directory that this README is in), run:

```
python -m main
```

### Overriding the command key

The default command key is `'`. To override this to another character, set the `DEV_CMD` in your env file:

```
DEV_CMD=!
```

### Add bot to a server

https://discord.com/api/oauth2/authorize?client_id=843357047192944709&permissions=3214336&scope=bot
