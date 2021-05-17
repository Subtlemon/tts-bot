import os

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def get_command_prefix():
    prefix = os.getenv('DEV_CMD')
    if prefix:
        return prefix
    else:
        return "'"


def main():
    bot = commands.Bot(command_prefix=get_command_prefix())

    @bot.event
    async def on_ready():
        print(f'Bot has logged in as {bot.user}.')

    bot.load_extension('cogs.tts')
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
