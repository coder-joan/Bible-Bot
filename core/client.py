import discord
from discord.ext import commands

def create_client() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True

    client = commands.AutoShardedBot(
        command_prefix="!",
        intents=intents,
        shard_count=None
    )
    return client