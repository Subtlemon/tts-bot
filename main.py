import discord
import os

from discord.ext.commands import Bot
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def main():
    intents = discord.Intents.default()
    bot = Bot(intents=intents, command_prefix='\'')


    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello!')


    @bot.event
    async def on_ready():
        print(f'Bot has logged in as {bot.user}.')

    bot.load_extension('extensions.vc')
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
