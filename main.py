import asyncio
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import random
from random import randint, randrange


load_dotenv()

# intents = discord.Intents().all()
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='!')

@bot.command(name="kvic-help", help="Help menu")
async def print_help(ctx):
    await ctx.send(f"""
    !join: Joins your Voice Channel
    !leave: Leaves current Voice Channel
    !play: Play random Ludas sound
    !stop: Stops playing
    !pause: Pauses current sound
    !resume: Resumes and plays from where left off.
    """)

@bot.command(name='join', help="joins the audio channel")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel.".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name="leave", help="leave voice channel")
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("Bot is not connected to any channel.")

@bot.command(name="play", help="Play Ludas or Jirka")
async def play(ctx, *name):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        # await ctx.send(name[0])

        if len(name) == 0:
            playlist = ['ludas', 'jirka', 'jolanda']
            choice = random.choice(playlist)
            # await ctx.send('{}'.format(choice))
            await play(ctx, choice)
        elif name[0] == 'ludas':
            id = randint(1, 93)
            async with ctx.typing():
                voice_channel.play(discord.FFmpegPCMAudio(source='./ludas/' + str(id) + '.m4a'))
                await ctx.send('Ludas ID: {}'.format(id))
        elif name[0] == 'jirka':
            id = randint(1, 36)
            async with ctx.typing():
                voice_channel.play(discord.FFmpegPCMAudio(source='./jirka/' + str(id) + '.mp3'))
                await ctx.send('Jirka ID: {}'.format(id))
        elif name[0] == 'jolanda':
            id = randint(1, 13)
            async with ctx.typing():
                voice_channel.play(discord.FFmpegPCMAudio(source='./jolanda/' + str(id) + '.wav'))
                await ctx.send('Jolanda ID: {}'.format(id))
        else:
            await ctx.send("Who the fuck is {}".format(name[0]))
    except:
        await ctx.send("Bot is not connected to a voice channel or is already talking")

# @bot.command()
# async def testp(ctx, *arg):
#     await ctx.send(arg[0])
#     if len(arg) == 0:
#         await ctx.send('gay')

# ORIGINAL
# @bot.command(name="play", help="Play Ludas")
# async def play(ctx):
#     id = randint(1, 93)
#     try:
#         server = ctx.message.guild
#         voice_channel = server.voice_client

#         async with ctx.typing():
#             voice_channel.play(discord.FFmpegPCMAudio(source='./ludas/' + str(id) + '.m4a'))
#             # voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source='./ludas/' + str(id) + '.m4a'))
#         await ctx.send('ID: {}'.format(id))
#     except:
#         await ctx.send("Bot is not connected to a voice channel.")


@bot.command(name="playid", help="Plays sound from author with given ID")
async def playid(ctx, name, id):
    server = ctx.message.guild
    voice_channel = server.voice_client
    if name == 'ludas':
        if int(id) > 93 or int(id) == 0:
            await ctx.send("ID out of range")
        else:
            async with ctx.typing():
                voice_channel.play(discord.FFmpegPCMAudio(source='./ludas/' + id + '.m4a'))
                await ctx.send('Ludas ID: {}'.format(id))
    if name == 'jirka':
        if int(id) > 36 or int(id) == 0:
            await ctx.send("ID out of range")
        else:
            async with ctx.typing():
                voice_channel.play(discord.FFmpegPCMAudio(source='./jirka/' + id + '.mp3'))
                await ctx.send('Jirka ID: {}'.format(id))
    if name == 'jolanda':
        if int(id) > 13 or int(id) == 0:
            await ctx.send("ID out of range")
        else:
            async with ctx.typing():
                voice_channel.play(discord.FFmpegPCMAudio(source='./jolanda/' + id + '.wav'))
                await ctx.send('Jolanda ID: {}'.format(id))

# ORIGINAL
# @bot.command(name="playid", help="Plays sound with given ID")
# async def playid(ctx, id):
#     server = ctx.message.guild
#     voice_channel = server.voice_client
#     if int(id) >= 93 or int(id) == 0:
#         await ctx.send("ID out of range")
#     else:
#         async with ctx.typing():
#             voice_channel.play(discord.FFmpegPCMAudio(source='./ludas/' + id + '.m4a'))
#             await ctx.send('ID: {}'.format(id))

@bot.command(name="pause", help='Pauses the Bot')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("Bot is not playing anything atm.")

@bot.command(name="resume", help="Resumes the Bot")
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("Bot is not playing anything atm. Use !play")

@bot.command(name="stop", help="Stops the Bot")
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not running atm.")

bot.run(BOT_TOKEN) #BOT_TOKEN
