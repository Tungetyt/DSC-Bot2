import discord
from discord.ext import commands
import random
import os
import youtube_dl
from dotenv import load_dotenv
import json
import codecs

load_dotenv()

# Settings:
client = commands.Bot(command_prefix='?')
mp3_dir = "music"
pic_dir = 'co_memes'
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with open(f'co_aliases.txt') as rs:
    co_alias = rs.read().splitlines()
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
    jaks_slownik = {
        "co": "nie wiem",
        "clear {ilosc}": "wyczysc podana ilosc wiadomosci",
        "play {link}": "pusc film z youtube",
        "pause": "zapauzuj film",
        "stop": "zatrzymaj film",
        "leave": "opusc kanal glosowy",
        "???": "i inne sekretne..."
    }
    for name, value in jaks_slownik.items():
        embed_var.add_field(name=name, value=value, inline=False)
    await ctx.send(embed=embed_var)


# Youtube commands:
@client.command()
async def play(ctx, url: str):
    song_there = os.path.isfile(f"{mp3_dir}/song.mp3")
    try:
        if song_there:
            os.remove(f"{mp3_dir}/song.mp3")
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
        with open(f'responses.txt') as rs:
            responses = rs.readlines()
        await ctx.send(f'{random.choice(responses)}')


async def download_and_play_video(ctx, url):
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name="Ogólne")
    await voice_channel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir(f"./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    os.replace("song.mp3", f"{mp3_dir}/song.mp3")
    voice.play(discord.FFmpegPCMAudio(f"{mp3_dir}/song.mp3"))


client.run(os.getenv("DSC_BOT_KEY"))
