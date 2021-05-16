import discord
import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def main():
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'Bot has logged in as {client.user}.')

    @client.event
    async def on_message(message):
        # Ignore self.
        if message.author == client.user:
            return
        if message.content.startswith('\'hello'):
            await message.channel.send('Hello!')

    client.run(TOKEN)


if __name__ == '__main__':
    main()
