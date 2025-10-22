import discord
from discord import app_commands

from config.colors import SUCCESS_COLOR
from utils.error_embed import no_data_embed

from services.user_translation_db import (
    get_user_settings, 
    delete_user_translation
)

@app_commands.command(name="cleartranslation", description="Deletes the default translation")
async def cleartranslation(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    user_id = interaction.user.id
    user_data = get_user_settings(user_id)

    if user_data:
        delete_user_translation(user_id)

        embed = discord.Embed(
            title="Deleted successfully",
            description=("Your default translation has been deleted"),
            color=SUCCESS_COLOR
        )
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(embed=no_data_embed())