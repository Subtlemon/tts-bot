import os

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from command_prefix import get_command_prefix


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def main():
    intents = Intents(guilds=True, messages=True, message_content=True, voice_states=True)
    bot = commands.Bot(command_prefix=get_command_prefix(), intents=intents)

    @bot.event
    async def on_ready():
        await bot.load_extension('cogs.tts')
        print(f'Bot has logged in as {bot.user}.')

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
