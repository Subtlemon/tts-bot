import discord


TOKEN = 'ODQzMzU3MDQ3MTkyOTQ0NzA5.YKCrdA.DFAoLq0kf7_5-L2S5VoeSW74Cl0'


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
