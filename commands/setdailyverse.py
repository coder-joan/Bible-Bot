import discord, pytz

from discord import app_commands
from utils.autocomplete import timezone_autocomplete
from config.colors import SUCCESS_COLOR, ERROR_COLOR
from services.dailyverse_settings_db import set_dailyverse_settings

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

    if hour < 1 or hour > 12:
        error_embed = discord.Embed(
            title="Error",
            description="Hour must be between 1 and 12",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)
        return
    
    if timezone not in pytz.all_timezones:
        error_embed = discord.Embed(
            title="Error",
            description="An incorrect time zone was provided. Please use autocomplete",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)
        return
    
    hour_24 = hour % 12
    if period.value == "PM":
        hour_24 += 12
        
    set_dailyverse_settings(interaction.user.id, channel.id, hour_24, timezone)

    embed = discord.Embed(
        title="Daily verse automation enabled",
        description=(
            f"Channel: {channel.mention}\n"
            f"Time: `{hour} {period.value}`\n"
            f"Timezone: `{timezone}`"
        ),
        color=SUCCESS_COLOR
    )
    await interaction.followup.send(embed=embed, ephemeral=True)