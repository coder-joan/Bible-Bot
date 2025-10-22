import discord
from discord import app_commands

from config.colors import SUCCESS_COLOR
from utils.error_embed import no_data_embed

from services.dailyverse_automation_db import (
    delete_dailyverse_automation, 
    get_dailyverse_automation_settings
)

@app_commands.command(name="cleardailyverse", description="Deletes daily verse automation")
async def cleardailyverse(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    user_id = interaction.user.id
    guild_id = interaction.guild.id

    settings = get_dailyverse_automation_settings(user_id, guild_id)

    if settings:
        delete_dailyverse_automation(user_id, guild_id)

        embed = discord.Embed(
            title="Deleted successfully",
            description="Daily verse automation has been deleted",
            color=SUCCESS_COLOR
        )
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(embed=no_data_embed())