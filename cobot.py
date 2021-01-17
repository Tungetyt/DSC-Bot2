import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix='?')

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
