import uuid

from audio_sources.composable_pcm import ComposablePCM
from audio_sources.resource_owning_source import ResourceOwningSource
from discord import FFmpegPCMAudio
from discord.ext import commands
from gtts import gTTS


@commands.command()
async def join(ctx: commands.Context):
    '''Joins the voice channel of the context's author.'''
    if not ctx.author.voice:
        return await ctx.send('You are not in a voice channel!')
    
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()


@commands.command()
async def leave(ctx: commands.Context):
    '''Leaves current voice channel.'''
    if not ctx.guild.voice_client:
        return await ctx.send('I was not in a voice channel')

    await ctx.guild.voice_client.disconnect()
    await ctx.send('Left voice channel!')


@commands.command()
async def say(ctx: commands.Context, *, text):
    if not ctx.author.voice:
        return await ctx.send('You are not in a voice channel!')

    print(text)
    speech = gTTS(text)
    file_path = f's_{uuid.uuid1()}.mp3'
    speech.save(file_path)
    new_source = ResourceOwningSource(FFmpegPCMAudio(file_path), file_path)

    voice_channel = ctx.author.voice.channel
    try:
        await voice_channel.connect()
    except:
        pass
    voice = ctx.guild.voice_client
    if not voice.is_playing():
        voice.play(ComposablePCM(new_source))
    else:
        if not voice.source.add_source(new_source):
            voice.stop()
            voice.play(ComposablePCM(new_source))


def setup(bot: commands.Bot):
    bot.add_command(join)
    bot.add_command(leave)
    bot.add_command(say)
