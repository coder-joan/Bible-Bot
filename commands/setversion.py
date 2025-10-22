import discord
from discord import app_commands

from config.paths import TRANSLATIONS
from config.colors import SUCCESS_COLOR

from utils.load_json import load_json
from utils.autocomplete import translation_autocomplete
from utils.error_embed import incorrect_translation_embed

from services.user_translation_db import set_user_translation

@app_commands.command(name="setversion", description="Sets a default Bible translation")
@app_commands.describe(translation="Select a Bible translation")
@app_commands.autocomplete(translation=translation_autocomplete)
async def setversion(interaction: discord.Interaction, translation: str):
    await interaction.response.defer(ephemeral=True)

    translations = load_json(TRANSLATIONS)

    if translation not in translations.keys():
        await interaction.followup.send(embed=incorrect_translation_embed(translation))
        return

    set_user_translation(interaction.user.id, translation)
    translation = translations.get(translation, translation)

    embed = discord.Embed(
        title="Set successfully",
        description=f"Your default Bible translation is: `{translation}`",
        color=SUCCESS_COLOR
    )
    await interaction.followup.send(embed=embed)