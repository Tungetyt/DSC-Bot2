import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix='?')
client.remove_command('help')

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
