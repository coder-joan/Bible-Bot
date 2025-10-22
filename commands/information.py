import discord
from discord import app_commands

from config.colors import STANDARD_COLOR
from config.links import (
    SERVER_LINK, 
    WEBSITE_LINK, 
    GITHUB_LINK, 
    TOP_GG_LINK, 
    DISCORD_BOT_LIST_LINK
)

@app_commands.command(name="information", description="Information about the bot")
async def information(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    embed = discord.Embed(
        title="Information",
        description=(
            "**Bible** is a bot designed to study the Word of God on Discord. "
            "Bible translations are available in **16** different languages\n\n"

            "**Links:**\n"
            f"- Website: {WEBSITE_LINK}\n"
            f"- Github: {GITHUB_LINK}\n"
            f"- Support Server: {SERVER_LINK}\n\n"

            "Enjoying the bot? Don’t stop there - vote now and share your thoughts on "
            f"[top.gg]({TOP_GG_LINK}) and [discordbotlist.com]({DISCORD_BOT_LIST_LINK})!"
        ),
        color=STANDARD_COLOR)
    
    await interaction.followup.send(embed=embed)