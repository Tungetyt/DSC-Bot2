import discord
from discord.ext import commands
import random
import os
import youtube_dl
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix='?')
client.remove_command('help')

players = {}

@client.event
async def on_ready():
    print('Bot is ready.')


@client.command(aliases=['cO','Co','CO','co?','CO?','cot',''])
async def co(ctx, *, question=''):
    choice = get_random_number_unless_specified(question)
    await send_pic_or_txt_on_choice(ctx, choice)

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

@client.command()
async def secret(ctx, *, message):
    channel = client.get_channel(int(os.getenv("RESPONSE_CHANNEL")))
    embed_var = discord.Embed(title=f"{message}", color=0xff770f)
    await channel.send(embed=embed_var)

@client.command()
async def help(ctx):
    embed_var = discord.Embed(title="Komendy:",description="przed komenda dodaj \"?\"", color=0x00ff00)
    embed_var.add_field(name="co",value="nie wiem", inline=False)
    embed_var.add_field(name="clear", value="wyczysc podana ilosc wiadomosci", inline=False)
    embed_var.add_field(name="???", value="i inne sekretne...", inline=False)
    await ctx.send(embed=embed_var)



@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

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














# @client.command(pass_context=True)
# async def join(ctx):
#     channel = ctx.message.author.voice.voice_channel
#     await client.join_voice_channel(channel)
#
# @client.command(pass_context=True)
# async def leave(ctx):
#     server = ctx.message.server
#     voice_client = client.voice_client_in(server)
#     player = await voice_client.disconnect()
#
# @client.command(pass_context=True)
# async def play(ctx, url):
#     server = ctx.message.server
#     voice_client = client.voice_client_in(server)
#     player = await voice_client.create_ytdl_player(url)
#     players[server.id] = player
#     player.start()

def get_random_number_unless_specified(question):
    if question == '1':
        return '1'
    elif question == '2':
        return '2'
    return f'{random.randint(1,8)}'

async def send_pic_or_txt_on_choice(ctx, choice):
    dirname = 'resources'
    if choice == '1':
        await ctx.send(file=discord.File(f'{dirname}/{random.randint(1,4)}.jpg'))
    elif choice == '2':
        await ctx.send(file=discord.File(f'{dirname}/{random.randint(1,4)}.png'))
    else:
        with open(f'{dirname}/responses.txt') as rs:
            responses = rs.readlines()
        await ctx.send(f'{random.choice(responses)}')


client.run(os.getenv("DSC_BOT_KEY"))
