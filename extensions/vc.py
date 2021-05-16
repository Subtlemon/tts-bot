from discord import FFmpegPCMAudio
from discord.ext import commands
from gtts import gTTS


@commands.command()
async def join(ctx):
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


@commands.command()
async def say(ctx, text):
    if not ctx.author.voice:
        return await ctx.send('You are not in a voice channel!')

    print(text)
    speech = gTTS(text)
    speech.save('speech.mp3')

    voice_channel = ctx.author.voice.channel
    try:
        await voice_channel.connect()
    except:
        pass
    voice = ctx.guild.voice_client
    if not voice.is_playing():
        voice.play(FFmpegPCMAudio('speech.mp3'))


def setup(bot):
    bot.add_command(join)
    bot.add_command(leave)
    bot.add_command(say)
