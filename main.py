# import cards
import discord
import asyncio
from discord.ext import commands

import config

client = discord.Client()
bot = commands.Bot(command_prefix=config.PREFIX)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    game = discord.Game(config.STATUS)
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print(f'Status set to {game}')


@bot.command()
async def hello(ctx):
    async with ctx.typing():
        await ctx.send('Hello!')


@bot.command()
async def echo(ctx, arg):
    async with ctx.typing():
        await ctx.send(arg)


@bot.command()
async def ping(ctx):
    await ctx.reply("Pong!")


@bot.command()
async def clear(ctx):
    def is_mine(m):
        return (m.author == bot.user) | m.content.startswith(config.PREFIX)

    deleted = await ctx.channel.purge(limit=10, check=is_mine)
    print('Deleted {} message(s)'.format(len(deleted)))


@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    counter = 0
    async for history in message.channel.history(limit=5):
        if history.content.capitalize() == message.content.capitalize():
            if history.author == bot.user:
                return  # hopefully this part doesn't break other things
            counter += 1
    if counter >= 3:
        await message.channel.send(message.content.capitalize())    # I call this the spam enabler

bot.run(config.TOKEN)
