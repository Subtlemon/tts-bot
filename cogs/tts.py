import uuid

from audio_sources.composable_pcm import ComposablePCM
from audio_sources.resource_owning_source import ResourceOwningSource
from command_prefix import get_command_prefix
from discord import FFmpegPCMAudio, Member, VoiceState
from discord.ext import commands
from engine.tts_engine import TTSEngine
from persistence.local_store import LocalStore
from ratelimit import limits, RateLimitException


LOCALSTORE_PATH = '.runtime_data/persistence.db'
# Max size of a text-to-speech message.
MAX_TEXT_SIZE = 160
# Max number of text-to-speech requests every minute.
MAX_TTS_PER_MINUTE = 60
RATE_LIMIT_ERROR_MESSAGE = 'Bot is being rate limited. Try again later.'


class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._tts_engine = TTSEngine()
        self._store = LocalStore(LOCALSTORE_PATH)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self._bot.user:
            return
        if message.content.startswith(f'{get_command_prefix()} '):
            ctx = await self._bot.get_context(message)
            try:
                await self._say(ctx, message.content[2:])
            except RateLimitException:
                return await ctx.send(RATE_LIMIT_ERROR_MESSAGE)

    @commands.command()
    async def leave(self, ctx: commands.Context):
        '''Leaves current voice channel.'''
        if not ctx.guild.voice_client:
            return await ctx.send('I was not in a voice channel')

        await ctx.guild.voice_client.disconnect()

    @commands.command()
    async def say(self, ctx: commands.Context, *, text):
        '''Say text. An empty command will also trigger text-to-speech.'''
        try:
            await self._say(ctx, text)
        except RateLimitException:
            return await ctx.send(RATE_LIMIT_ERROR_MESSAGE)

    @limits(calls=MAX_TTS_PER_MINUTE, period=60)
    async def _say(self, ctx: commands.Context, text):
        if not ctx.author.voice:
            return await ctx.send('You are not in a voice channel!')
        if ctx.guild.voice_client is not None and ctx.author.voice.channel.id != ctx.guild.voice_client.channel.id:
            return await ctx.send('You are not in the same voice channel as me! You can make me leave the other channel using the `leave` command.')
        if len(text) > MAX_TEXT_SIZE:
            return await ctx.send(f'Text cannot be longer than {MAX_TEXT_SIZE} characters.')

        file_path = f's_{uuid.uuid1()}.mp3'
        voice = self._store.get_voice(ctx.guild.id, ctx.author.id)
        self._tts_engine.text_to_speech(text, voice, file_path)
        new_source = ResourceOwningSource(FFmpegPCMAudio(file_path), file_path)

        voice_channel = ctx.author.voice.channel
        try:
            await voice_channel.connect()
        except:
            pass
        voice_client = ctx.guild.voice_client
        if not voice_client.is_playing():
            voice_client.play(ComposablePCM(new_source))
        else:
            if not voice_client.source.add_source(new_source):
                voice_client.stop()
                voice_client.play(ComposablePCM(new_source))

    @commands.command()
    async def setvoice(self, ctx: commands.Context, voice):
        '''Sets the voice for your text.'''
        if not self._tts_engine.is_voice_valid(voice):
            return await ctx.send(f'{voice} is not a valid voice. Check the `voices` command for valid voices.')
        self._store.set_voice(ctx.guild.id, ctx.author.id, voice)

    @commands.command()
    async def voices(self, ctx: commands.Context):
        '''List available voices.'''
        return await ctx.send(', '.join(self._tts_engine.all_voices()))

    @commands.command()
    async def myvoice(self, ctx: commands.Context):
        '''Shows what voice you're using.'''
        return await ctx.send(f'{ctx.author.name}, your voice is {self._store.get_voice(ctx.guild.id, ctx.author.id)}.')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if member == self._bot.user:
            return
        for voice_client in self._bot.voice_clients:
            num_members = len(voice_client.channel.members)
            if before.channel == voice_client.channel and after.channel != voice_client.channel:
                # Lost a channel member. Check if we have any channel members left.
                if num_members <= 1:
                    # Bot is all alone in the channel. Leave now. Also return because no other channels are affected.
                    return await voice_client.disconnect()


async def setup(bot: commands.Bot):
    await bot.add_cog(TextToSpeech(bot))
