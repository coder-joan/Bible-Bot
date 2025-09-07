import discord

from discord import app_commands
from utils.load_json import load_json
from config.paths import TRANSLATIONS
from config.colors import STANDARD_COLOR
from services.user_translation_db import get_user_settings
from services.dailyverse_settings_db import get_dailyverse_settings

@app_commands.command(name="mysettings", description="Displays the current user settings")
async def mysettings(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    translations = load_json(TRANSLATIONS)

    user_id = interaction.user.id
    guild_id = interaction.guild.id

    user_data = get_user_settings(user_id)
    dailyverse_data = get_dailyverse_settings(user_id, guild_id)

    translation = user_data[1] if user_data else "-"
    translation = translations.get(translation, translation)

    if dailyverse_data:
        channel_id, hour, timezone = dailyverse_data

        period = "AM" if hour < 12 else "PM"
        hour_12 = hour % 12
        hour_12 = 12 if hour_12 == 0 else hour_12

        dailyverse_text = (
                f"Daily verse automation: **enabled**\n"
                f"- Channel: <#{channel_id}>\n"
                f"- Hour: `{hour_12} {period}`\n"
                f"- Timezone: `{timezone}`"
        )
    else:
        dailyverse_text = (
                f"Daily verse automation: **disabled**\n"
                f"- Channel: -\n"
                f"- Hour: -\n"
                f"- Timezone: -"
        )

    embed = discord.Embed(
        title="Your settings",
        description=f"{dailyverse_text}\n\nBible translation: `{translation}`",
        color=STANDARD_COLOR
    )

    await interaction.followup.send(embed=embed, ephemeral=True)