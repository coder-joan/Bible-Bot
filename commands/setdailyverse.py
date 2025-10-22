import discord, pytz
from discord import app_commands

from config.colors import SUCCESS_COLOR

from utils.autocomplete import timezone_autocomplete
from utils.error_embed import (
    hour_error_embed,    
    incorrect_timezone_embed,
    set_default_translation_embed
)

from services.user_translation_db import get_user_settings
from services.dailyverse_automation_db import set_dailyverse_automation

@app_commands.command(name="setdailyverse", description="Sets up daily verse automation")

@app_commands.describe(
    channel="Select a channel to send the daily verse",
    hour="Enter the hour (1–12)",
    period="Select a time period (AM/PM)",
    timezone="Select a time zone"
)

@app_commands.choices(period=[
    app_commands.Choice(name="AM", value="AM"),
    app_commands.Choice(name="PM", value="PM")
])

@app_commands.autocomplete(timezone=timezone_autocomplete)

async def setdailyverse(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    hour: int,
    period: app_commands.Choice[str],
    timezone: str
):
    await interaction.response.defer(ephemeral=True)

    user_data = get_user_settings(interaction.user.id)

    if not user_data or not user_data[1]:  
        await interaction.followup.send(embed=set_default_translation_embed())
        return

    if hour < 1 or hour > 12:
        await interaction.followup.send(embed=hour_error_embed())
        return
    
    if timezone not in pytz.all_timezones:
        await interaction.followup.send(embed=incorrect_timezone_embed())
        return
    
    hour_24 = hour % 12
    if period.value == "PM":
        hour_24 += 12
        
    set_dailyverse_automation(interaction.user.id, interaction.guild.id, channel.id, hour_24, timezone)

    embed = discord.Embed(
        title="Daily verse automation enabled",
        description=(
            f"Channel: {channel.mention}\n"
            f"Time: `{hour} {period.value}`\n"
            f"Timezone: `{timezone}`"
        ),
        color=SUCCESS_COLOR
    )
    await interaction.followup.send(embed=embed)