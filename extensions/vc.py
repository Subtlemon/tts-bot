from discord.ext import commands


@commands.command(name='join')
async def joinAuthorVoiceChannel(ctx):
    '''Joins the voice channel of the context's author.'''
    if not ctx.author.voice:
        return await ctx.send('You are not in a voice channel!')
    
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()


@commands.command()
async def leave(ctx):
    '''Leaves current voice channel.'''
    if not ctx.guild.voice_client:
        return await ctx.send('I was not in a voice channel')

    await ctx.guild.voice_client.disconnect()
    await ctx.send('Left voice channel!')


def setup(bot):
    bot.add_command(joinAuthorVoiceChannel)
    bot.add_command(leave)
