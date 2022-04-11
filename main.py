# import cards
import discord
# import asyncio
# import time
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
    async for history in message.channel.history(limit=8):
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
    def __init__(self, bott):
        self.phase = 0
        self.bot = bott
        self.host = None
        self.player_count = 0
        self.members = []

    @commands.command()
    async def join(self, ctx):
        """Joins the active lobby"""
        if self.phase == 0:
            await ctx.reply('There is nothing to join right now')
            return
        elif self.phase == 2:
            await ctx.reply('This game is already in progress, try next time')
            return   # maybe have this delete the messages after
        elif self.phase == 1:
            # if dms are off:
            #   let them know they need dms on to join
            #   return
            if ctx.author in self.members:
                await ctx.reply('You are already in the lobby')
                return
            self.members[self.player_count] = ctx.author  # this is also fucked
            self.player_count += 1
            await ctx.send('{0.mention}'.format(ctx.author)+' has joined the lobby')
            print(self.members)
            print(self.player_count)
            return

    @commands.command()
    async def start(self, ctx):
        """Closes the lobby and starts the game"""
        if ctx.author != self.host:
            await ctx.send('Only the host can start the lobby early')
            return
        self.phase = 2
        print('Game started')


class Blackjack(Game):
    @commands.command()
    async def blackjack(self, ctx):
        """Opens a blackjack lobby"""
        if self.phase == 0:
            self.phase = 1
            self.host = ctx.author
            self.members.append(ctx.author)
            self.player_count = 1
            print(f'{self.host} has started a game of blackjack')
            await ctx.send('{0.mention}'.format(self.host)+' has started a game of blackjack!\n'
                           f'Type {config.PREFIX}join to play with them')
        else:
            await ctx.send(f'There is already an active blackjack lobby')


bot.add_cog(Blackjack(bot))
bot.run(config.TOKEN)
