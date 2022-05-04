# import cards
import discord
# import asyncio
# import time
from discord.ext import commands

import config

client = discord.Client()
perms = discord.AllowedMentions(everyone=False)
bot = commands.Bot(command_prefix=config.PREFIX, allowed_mentions=perms)

cardgames = ('blackjack', 'poker')
either_or = (['Yanny', 'Laurel'], ["GIF", "JIF"])


def has_been_replied_to(ctx):
    def replied(m):
        return m.reference.message_id == ctx.message_id
    if ctx.channel.history(limit=10, check=replied):
        return True
    return False


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
@commands.is_owner()
async def clear(ctx):
    if ctx.message.reference:
        msg_id = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        deleted = await ctx.channel.purge(limit=1000, after=msg_id)
        print('Deleted {} message(s)'.format(len(deleted)))
        return

    def is_mine(m):
        return (m.author == bot.user) | m.content.startswith(config.PREFIX)

    deleted = await ctx.channel.purge(limit=10, check=is_mine)
    print('Deleted {} message(s)'.format(len(deleted)))
    return


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


class CardGame(commands.Cog):
    def __init__(self, bott):
        self.bot = bott
        self.game_name = None
        self.phase = 0
        self.host = None
        self.player_count = 0
        self.members = []

    @commands.command()
    async def start(self, ctx, gmd=None):
        """Initiates a card game"""
        for game in cardgames:
            if gmd == game:
                self.game_name = game

        if self.phase == 0:
            if gmd is None:
                await ctx.reply('Please specify what game you want to start')
                return

            if ctx.author.dm_channel is None:  # Check if the member has been DMed before
                await ctx.author.create_dm()
            async with ctx.typing():
                try:
                    await ctx.author.dm_channel.send(f'You\'ve opened a {self.game_name} lobby!\n' +
                                                     f'Use the `{config.PREFIX}start` command again to start the game`')
                except discord.Forbidden:  # Make sure they can be DMed in the first place
                    await ctx.reply('You must be able to receive bot DMs to use this feature')
                    return

                await ctx.send('{0.mention}'.format(ctx.author) +
                               f' has started a game of {self.game_name}!\n'
                               f'Type `{config.PREFIX}join` to play with them')

            self.phase = 1
            self.host = ctx.author
            self.members.append(ctx.author)
            self.player_count = 1
            print(f'{self.host} has started a game of {self.game_name}')
            return

        if self.phase == 1:
            if ctx.author != self.host:
                await ctx.reply(f'There is already an open lobby!\n'
                                f'Type `{config.PREFIX}join` to play with them')
                return

            self.phase = 2
            await ctx.send("This doesn't actually work yet lol")
            print('Game started')
            return

        await ctx.reply(f'There is already an active game started')

    @commands.command()
    async def join(self, ctx):
        """Joins the active lobby"""
        if ctx.author in self.members:  # If you're already in the lobby
            await ctx.reply('You are already in the lobby')
            return

        if self.phase == 0:  # If there's no game running
            await ctx.reply('There is nothing to join right now\n'
                            f'Try using the `{config.PREFIX}start` command to change that!')
            return

        if self.phase == 2:  # If there's an in-progress game
            await ctx.reply('The game is already in progress, try again next time')
            return

        if ctx.author.dm_channel is None:  # Check if the member has been DMed before
            await ctx.author.create_dm()
        async with ctx.typing():
            try:
                await ctx.author.dm_channel.send(f"You've joined {self.host}'s lobby!\n"
                                                 f"Sit tight, the game will start soon")
                await ctx.send('{0.mention}'.format(ctx.author) + ' has joined the lobby')
            except discord.Forbidden:  # Make sure they can be DMed in the first place
                await ctx.reply('You must be able to receive bot DMs to use this feature')
                return

        self.members.append(ctx.author)
        self.player_count += 1
        # print(self.members)
        print(f'{self.members[self.player_count-1]} has joined the lobby')
        print(f'{self.player_count} players in lobby')
        return


bot.add_cog(CardGame(bot))
bot.run(config.TOKEN)
