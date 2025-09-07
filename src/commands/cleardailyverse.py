import discord

from discord import app_commands
from config.colors import SUCCESS_COLOR, ERROR_COLOR
from services.dailyverse_settings_db import delete_dailyverse_settings, get_dailyverse_settings

@app_commands.command(
    name="cleardailyverse",
    description="Deletes daily verse automation"
)

async def cleardailyverse(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    user_id = interaction.user.id
    guild_id = interaction.guild.id

    settings = get_dailyverse_settings(user_id, guild_id)

    if settings:
        delete_dailyverse_settings(user_id, guild_id)

        embed = discord.Embed(
            title="Deleted successfully",
            description="Daily verse automation has been deleted",
            color=SUCCESS_COLOR
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    else:
        error_embed = discord.Embed(
            title="No data",
            description="Your data not found in the database",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)