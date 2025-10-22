import discord, psutil
from discord import app_commands

from core.client import create_client
from config.colors import STANDARD_COLOR

from services.user_translation_db import get_user_count
from services.dailyverse_automation_db import get_dailyverse_automation_user_count

client = create_client()

@app_commands.command(name="stats", description="Bot statistics")
async def stats(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    latency_ms = round(interaction.client.latency * 1000)
    ram_usage_mb = psutil.Process().memory_info().rss / 1024 / 1024

    embed = discord.Embed(
        title="Statistics",
        description=(
            "These are the current stats for **Bible** bot. "
            "Please note that these stats are not 100% accurate"
        ),
        color=STANDARD_COLOR
    )  

    embed.add_field(name="Ping", value=f"{latency_ms} ms", inline=True)
    embed.add_field(name="RAM Usage", value=f"{ram_usage_mb:.2f} MB", inline=True)
    embed.add_field(name="Shards", value=str(interaction.client.shard_count or 1), inline=True)
    embed.add_field(name="Servers", value=f"{len(interaction.client.guilds)}", inline=True)
    embed.add_field(name="Users", value=f"{get_user_count()}", inline=True)
    embed.add_field(name="Daily verse automation users", value=f"{get_dailyverse_automation_user_count()}", inline=True)

    await interaction.followup.send(embed=embed)