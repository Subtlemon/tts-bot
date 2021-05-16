from discord.ext import commands


@commands.command(name='join')
async def joinAuthorVoiceChannel(ctx):
    await ctx.send('No')


def setup(bot):
    bot.add_command(joinAuthorVoiceChannel)
