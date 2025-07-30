import discord

from discord.ext import commands
from config.colors import STANDARD_COLOR
from services.user_translation_db import get_user_count

@commands.command(name="stats")
async def stats(ctx):
    embed = discord.Embed(
        title="Statistics",
        description=f"Server count: **{len(ctx.bot.guilds)}**\n"
                    f"User count: **{get_user_count()}**",
        color=STANDARD_COLOR
    )
    await ctx.send(embed=embed)