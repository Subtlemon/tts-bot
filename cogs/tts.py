import uuid

from audio_sources.composable_pcm import ComposablePCM
from audio_sources.resource_owning_source import ResourceOwningSource
from discord import FFmpegPCMAudio
from discord.ext import commands
from google.cloud import texttospeech
from persistence.local_store import LocalStore


LOCALSTORE_PATH = '.runtime_data/persistence.db'
VOICES = ['en-US', 'en-AU', 'en-IN', 'ja', 'en-GB']


class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._client = texttospeech.TextToSpeechClient()
        self._store = LocalStore(LOCALSTORE_PATH)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self._bot.user:
            return
        if message.content.startswith("' "):
            ctx = await self._bot.get_context(message)
            await self._say(ctx, message.content)

    @commands.command()
    async def join(self, ctx: commands.Context):
        '''Joins the voice channel of the context's author.'''
        if not ctx.author.voice:
            return await ctx.send('You are not in a voice channel!')

        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()


    @commands.command()
    async def leave(self, ctx: commands.Context):
        '''Leaves current voice channel.'''
        if not ctx.guild.voice_client:
            return await ctx.send('I was not in a voice channel')

        await ctx.guild.voice_client.disconnect()
        await ctx.send('Left voice channel!')


    @commands.command()
    async def say(self, ctx: commands.Context, *, text):
        await self._say(ctx, text)

    async def _say(self, ctx: commands.Context, text):
        if not ctx.author.voice:
            return await ctx.send('You are not in a voice channel!')

        synthesis_input = texttospeech.types.SynthesisInput(text=text)
        lang = VOICES[self._store.get_voice(ctx.guild.id, ctx.author.id)]
        voice = texttospeech.types.VoiceSelectionParams(language_code=lang, ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)
        response = self._client.synthesize_speech(input_=synthesis_input, voice=voice, audio_config=audio_config)
        
        file_path = f's_{uuid.uuid1()}.mp3'
        with open(file_path, 'wb') as out:
            out.write(response.audio_content)
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


    @commands.command()
    async def setvoice(self, ctx: commands.Context, voice_id_str):
        try:
            voice_id = int(voice_id_str)
        except ValueError:
            return await ctx.send(f'You provided an invalid voice ID. There are {len(VOICES)} voices.')
        if voice_id < 0 or voice_id >= len(VOICES):
            return await ctx.send(f'You provided an invalid voice ID. There are {len(VOICES)} voices.')
        self._store.set_voice(ctx.guild.id, ctx.author.id, voice_id)


def setup(bot: commands.Bot):
    bot.add_cog(TextToSpeech(bot))
