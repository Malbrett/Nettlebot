import asyncio
import cards
import discord
# import time
from discord.ext import commands
# from dataclasses import dataclass

import config

client = discord.Client()
perms = discord.AllowedMentions(everyone=False)
bot = commands.Bot(command_prefix=config.PREFIX, allowed_mentions=perms)

card_games = ('blackjack', 'poker', 'uno')
either_or = (['Based', 'Cringe'], ['Yanny', 'Laurel'], ["GIF", "JIF"])
numbers = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')

# TODO: Create new Cog for handling user data (inventory, bank, high scores, etc..)


async def parse_move(ctx, moves, player):
    text = f'Moves: \n'
    opt = 1
    async with ctx.typing():
        for move in moves:
            text += f":{numbers[opt]}: = :{move}: \n"
            opt += 1
        text = await ctx.send(text)
        for num in range(1, opt):
            # await text.add_reaction(f':{numbers[num]}:')  this doesn't work yet
            await text.add_reaction(f'{move}')

    def check(r, u):
        return r.emoji in moves and r.message.id == text.id and u == player
    try:
        choice = await bot.wait_for("reaction_add", check=check, timeout=60)
    except asyncio.TimeoutError:
        return None
    else:
        return 1  # this needs to return what the choice is
    finally:
        text.delete()


def has_been_replied_to(ctx):
    def replied(m):
        return m.reference.message_id == ctx.message_id
    if ctx.channel.history(limit=10, check=replied):
        return True
    return False


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    activity = discord.CustomActivity(config.STATUS)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print(f'Status set to {activity}')
    return


@bot.command()
async def hello(ctx):
    """The bot is quite polite, and will say hello back"""
    async with ctx.typing():
        await ctx.send('Hello!')
    return


@bot.command()
async def echo(ctx, arg):
    """Make the bot say something, maybe even a bad word"""
    async with ctx.typing():
        await ctx.send(arg, allowed_mentions=perms)
    return


@bot.command()
async def ping(ctx):
    """Annoying and pointless"""
    await ctx.reply("Pong!")
    return


@bot.command()
async def rps(ctx):
    """Play 'Rock, Paper, Scissors' with the bot"""
    moves = (':fist:', ':raised_hand:', ':v:')
    pc = await parse_move(ctx, moves, ctx.author)
    npc = 0
    async with ctx.typing():
        if pc == npc:
            result = "We tied!"
        elif pc - npc == 1 or -2:
            result = "You win!"
        elif pc - npc == -1 or 2:
            result = "I win!"
        await ctx.send(f'Your choice: {moves[pc]}\n'
                       f'My choice: {moves[npc]}\n'
                       f'{result}')
    return


@bot.command()
@commands.is_owner()
async def archive(ctx, arg=0):
    """Export messages into .txt from Discord"""
    if ctx.message.reference:
        msgs = [await ctx.channel.fetch_message(ctx.message.reference.message_id)]
        if arg:
            for msg in await ctx.channel.history(limit=arg, after=msgs[0]).flatten():
                print(msg.id)
                msgs.append(msg)
        for msg in msgs:
            with open(f"ChatArchive/{msg.id}.txt", "w") as file:
                file.write(f"{str(msg.author)}\n{msg.clean_content}")
        return

    ctx.reply("Please reply to the message you wish to archive")
    return


@bot.command()
@commands.is_owner()
async def clear(ctx):
    """Clear messages en masse, either a specific number or up to a specified message"""
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
                return
            for user in authors:
                if authors.count(user) > 1:
                    return
            counter += 1
    if counter >= 3:
        if "http" in message.content:
            await message.channel.send(message.content.lower())  # I call this the spam enabler
        else:
            await message.channel.send(message.content.capitalize())


class CardGames(commands.Cog):
    """Used to play in-chat card games, such as """
    def __init__(self, bott):
        self.bot = bott
        self.game_name = None
        self.phase = 0
        self.host = None
        self.player_count = 0
        self.players = []
        self.gui = None

# TODO: Actually fucking make the games now goddamnit.
#   Lobbies work now, that's cool. Now it's about putting it into practice. My idea is basically
#   def different functions for each game that get run after the host uses the start command again.
#   This might get messy with listeners for moves and stuff, but basically these functions will dictate
#   the flow of the games (turn order, making moves, betting, scoring, etc.)

    class Player:
        def __init__(self, user):
            self.user = user
            self.hand = cards.Deck(True)
            self.hand_gui = None
            self.score = 0
            self.stand = False
            self.bust = False

        def show_hand(self, hide=False):
            string = f"{self.user}'s hand: {self.hand.list(hide)}"
            string += f"Total: {self.hand.list(val=True, hide=hide)}"
            return string

    async def update_gui(self, ctx=None):
        output = f"```{self.host}'s game of {self.game_name}\n"
        for player in self.players:
            player.hand_gui.edit(player.show_hand())
            output += player.show_hand(True)
        if ctx:
            self.gui = await ctx.send(output)
            return
        self.gui.edit(output)
        return

    @commands.command()
    async def games(self, ctx):
        """Lists available games you can play"""
        await ctx.reply('Blackjack')
        return

    async def blackjack(self, ctx):
        moves = ('hit', 'stand')
        async with ctx.typing():
            deck = cards.Deck()
            deck.shuffle()
            for player in self.players:
                player.hand.insert(deck.draw(hidden=True))
                player.hand.insert(deck.draw())
                player.hand_gui = await player.user.dm_channel.send(player.show_hand())
            await self.update_gui(ctx)

        while True:
            passed = 0
            for player in self.players:
                if player.stand or player.bust:
                    passed += 1
                    continue
                print(f"{player.name}'s turn:")
                while True:
                    move = parse_move(ctx, moves, player)
                    if move == "hit":
                        player.hand.insert(deck.draw())
                        player.show_hand(player)
                        if player.hand.list(val=True) > 21:
                            player.bust = True
                            player.score = 0
                            print(f"{player.name} has bust!")
                            passed += 1
                            continue
                        continue
                    if move == "stand":
                        player.stand = True
                        player.score = player.hand.list(val=True)
                        print(f"{player.name} stood")
                        passed += 1
                        continue
                    print(f"Invalid move")
            if passed == self.player_count:  # detects if it's time to score the round
                break

        winner = self.players[0]
        for player in self.players:
            if player.score > winner.score:
                winner = player
        print(f"{winner.name} wins!!")
        return

    async def poker(self, ctx):
        async with ctx.typing():
            deck = cards.Deck()
            deck.shuffle()
            for player in self.players:
                player.hand.insert(deck.draw(hidden=True))
                player.hand.insert(deck.draw(hidden=True))
                player.hand_gui = await player.user.dm_channel.send(f'Your cards are: {player.hand.list()}\n')
            await self.update_gui(ctx)
        return

    async def uno(self, ctx):
        await ctx.send("Uno doesn't work yet lol")
        return

    @commands.command()
    async def play(self, ctx, gmd=None):
        """Used to create a card game lobby"""
        for game in card_games:
            if gmd == game:
                self.game_name = game
                break

        if self.phase == 0:
            if gmd is None:
                await ctx.reply('Please specify what game you want to play')
                return

            if ctx.author.dm_channel is None:  # Check if the member has been DMed before
                await ctx.author.create_dm()
            async with ctx.typing():
                try:
                    await ctx.author.dm_channel.send(f'You\'ve opened a {self.game_name} lobby!\n' +
                                                     f'Use the `{config.PREFIX}play` command again to start the game')
                except discord.Forbidden:  # Make sure they can be DMed in the first place
                    await ctx.reply('You must be able to receive bot DMs to use this feature')
                    return

                await ctx.send('{0.mention}'.format(ctx.author) +
                               f' is starting a game of {self.game_name}!\n'
                               f'Type `{config.PREFIX}join` to play with them')

            self.phase = 1
            self.host = ctx.author
            self.players.append(self.Player(ctx.author))
            self.player_count = 1
            print(f'{self.host} has started a game of {self.game_name}')
            return

        if self.phase == 1:
            if ctx.author != self.host:
                await ctx.reply(f'There is already an open lobby!\n'
                                f'Type `{config.PREFIX}join` to play with them')
                return

            self.phase = 2
            print('Game started')
            if self.game_name == 'blackjack':
                await self.blackjack(ctx)
            if self.game_name == 'poker':
                await self.poker(ctx)
            if self.game_name == 'uno':
                await self.uno(ctx)

            await ctx.send('The game is over. Thanks for playing!')
            self.game_name = None
            self.phase = 0
            self.host = None
            self.player_count = 0
            self.players = []
            print('Game ended')
            return

        await ctx.reply(f'There is already an active game started')

    @commands.command()
    async def join(self, ctx):
        """Joins the active lobby"""
        for player in self.players:  # If you're already in the lobby
            if player.user == ctx.author:
                await ctx.reply('You are already in the lobby')
                return

        if self.phase == 0:  # If there's no game running
            await ctx.reply('There is nothing to join right now\n'
                            f'Try using the `{config.PREFIX}play` command to change that!')
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
                await ctx.send(f'{ctx.author.mention} has joined the lobby')
            except discord.Forbidden:  # Make sure they can be DMed in the first place
                await ctx.reply('You must be able to receive bot DMs to use this feature')
                return

        self.players.append(self.Player(ctx.author))
        self.player_count += 1
        # print(self.players)
        print(f'{ctx.author} has joined the lobby')
        print(f'{self.player_count} players in lobby')
        return


bot.add_cog(CardGames(bot))
bot.run(config.TOKEN)
