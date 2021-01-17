import discord
from discord.ext import commands
import random
import os
import youtube_dl
from dotenv import load_dotenv
import json
from read_methods import read_file
from config import *
load_dotenv()

# Settings:
client = commands.Bot(command_prefix='?')


co_alias = read_file('co_aliases')
client.remove_command('help')
players = {}


# Startup:
@client.event
async def on_ready():
    print('Bot is ready.')


# Commands:
@client.command(aliases=co_alias)
async def co(ctx, *, question=''):
    choice = get_random_number_unless_specified(question)
    await send_pic_or_txt_on_choice(ctx, choice)


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)


@client.command()
async def secret(ctx, *, message):
    channel = client.get_channel(int(os.getenv("RESPONSE_CHANNEL")))
    embed_var = discord.Embed(title=f"{message}", color=0xff770f)
    await channel.send(embed=embed_var)


@client.command()
async def help(ctx):
    embed_var = discord.Embed(title="Komendy:", description="przed komenda dodaj \"?\"", color=0x00ff00)
    help_json = "".join(read_file('help'))
    for name, value in json.loads('{'+help_json+'}').items():
        embed_var.add_field(name=name, value=value, inline=False)
    await ctx.send(embed=embed_var)


# Youtube commands:
@client.command()
async def play(ctx, url: str):
    song_there = os.path.isfile(f"{mp3_dir}/{temp_mp3_name}")
    try:
        if song_there:
            os.remove(f"{mp3_dir}/{temp_mp3_name}")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return
    await download_and_play_video(ctx, url)


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


def get_random_number_unless_specified(question):
    if question == '1':
        return '1'
    elif question == '2':
        return '2'
    return f'{random.randint(1, 8)}'


async def send_pic_or_txt_on_choice(ctx, choice):
    if choice == '1':
        await ctx.send(file=discord.File(f'{pic_dir}/{random.randint(1, 4)}.jpg'))
    elif choice == '2':
        await ctx.send(file=discord.File(f'{pic_dir}/{random.randint(1, 4)}.png'))
    else:
        responses = read_file('responses')
        await ctx.send(f'{random.choice(responses)}')


async def download_and_play_video(ctx, url):
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name="Ogólne")
    await voice_channel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir(f"./"):
        if file.endswith(".mp3"):
            os.rename(file, temp_mp3_name)
    os.replace(temp_mp3_name, f"{mp3_dir}/{temp_mp3_name}")
    voice.play(discord.FFmpegPCMAudio(f"{mp3_dir}/{temp_mp3_name}"))


client.run(os.getenv("DSC_BOT_KEY"))
