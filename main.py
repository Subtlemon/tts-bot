import os

from discord.ext import commands
from dotenv import load_dotenv
from command_prefix import get_command_prefix


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def main():
    bot = commands.Bot(command_prefix=get_command_prefix())

    @bot.event
    async def on_ready():
        print(f'Bot has logged in as {bot.user}.')

    bot.load_extension('cogs.tts')
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
