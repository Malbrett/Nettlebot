import cards
import discord
import asyncio
from discord.ext import commands

import config

client = discord.Client()
bot = commands.Bot(command_prefix=config.PREFIX)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    message.content = message.content.lower()

    if message.author == client.user:
        return

    if message.content.startswith(f'{config.PREFIX}clear'):
        def is_mine(m):
            return (m.author == client.user) | m.content.startswith(config.PREFIX)
        deleted = await message.channel.purge(limit=10, check=is_mine)
        print('Deleted {} message(s)'.format(len(deleted)))

    if message.content.startswith(f'{config.PREFIX}hello'):
        await message.channel.send('Hello!')

    if message.content.startswith(f'{config.PREFIX}piss'):
        await message.channel.send('Fuck you Arthur')


client.run(config.TOKEN)
