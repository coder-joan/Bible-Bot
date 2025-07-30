import discord

from discord import app_commands
from config.colors import STANDARD_COLOR

@app_commands.command(name="information", description="Information about the bot")
async def information(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Information",
        description=(
            f"**Bible** is a bot designed to study the Word of God on Discord. "
             "Allows comparison of Bible translations in **16** languages\n\n"

             "**Website:** https://bible-bot.netlify.app/\n\n"

             "[Terms of Service](https://bible-bot.netlify.app/terms-of-service) • [Privacy Policy](https://bible-bot.netlify.app/privacy-policy)"
        ),
        color=STANDARD_COLOR)

    await interaction.response.send_message(embed=embed)