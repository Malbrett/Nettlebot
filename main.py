# import cards
import discord
import asyncio
from discord.ext import commands

import config

client = discord.Client()
perms = discord.AllowedMentions(everyone=False)
bot = commands.Bot(command_prefix=config.PREFIX, allowed_mentions=perms)

either_or = (['Yanny', 'Laurel'], ["GIF", "JIF"])


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
        await ctx.send(arg, allowed_mentions=perms)


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
    authors = []
    async for history in message.channel.history(limit=5):
        if history.content.capitalize() == message.content.capitalize():
            authors.append(history.author)
            if bot.user in authors:
                return  # hopefully this part doesn't break other things
            for user in authors:
                if authors.count(user) > 1:
                    return
            counter += 1
    if counter >= 3:
        if "http" in message.content:
            await message.channel.send(message.content.lower())  # I call this the spam enabler
        else:
            await message.channel.send(message.content.capitalize())


class Game(commands.Cog):
    def __init__(self, user):
        self.bot = user

    async def lobby(self, ctx):
        member = ctx.author


class Blackjack(Game):
    @commands.command()
    async def blackjack(self, ctx):
        """Starts a game of blackjack"""
        member = ctx.author
        print(f'{member} has started a hand of blackjack')
        await ctx.send('{0.mention}'.format(member))


bot.add_cog(Blackjack(bot))
bot.run(config.TOKEN)
