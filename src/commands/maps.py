import discord

from discord import app_commands
from config.paths import MAPS
from config.colors import STANDARD_COLOR, ERROR_COLOR

@app_commands.command(name="maps", description="Displays selected map")
@app_commands.describe(map="Select a map")
@app_commands.choices(map=[
    app_commands.Choice(name="Canaan in Old Testament Times", value="Canaan in Old Testament Times"),
    app_commands.Choice(name="Israel’s Exodus from Egypt and Entry into Canaan", value="Israel’s Exodus from Egypt and Entry into Canaan"),
    app_commands.Choice(name="Jerusalem at the Time of Jesus", value="Jerusalem at the Time of Jesus"),
    app_commands.Choice(name="Physical Map of the Holy Land", value="Physical Map of the Holy Land"),
    app_commands.Choice(name="The Assyrian Empire", value="The Assyrian Empire"),
    app_commands.Choice(name="The Division of the 12 Tribes", value="The Division of the 12 Tribes"),
    app_commands.Choice(name="The Empire of David and Solomon", value="The Empire of David and Solomon"),
    app_commands.Choice(name="The Holy Land in New Testament Times", value="The Holy Land in New Testament Times"),
    app_commands.Choice(name="The Missionary Journeys of the Apostle Paul", value="The Missionary Journeys of the Apostle Paul"),
    app_commands.Choice(name="The New Babylonian Empire and the Kingdom of Egypt", value="The New Babylonian Empire and the Kingdom of Egypt"),
    app_commands.Choice(name="The Persian Empire", value="The Persian Empire"),
    app_commands.Choice(name="The Roman Empire", value="The Roman Empire"),
    app_commands.Choice(name="The World of the Old Testament", value="The World of the Old Testament")
])

async def maps(interaction: discord.Interaction, map: app_commands.Choice[str]):
    await interaction.response.defer()

    file_path = f'{MAPS}{map.value}.png'

    try:
        image = discord.File(file_path, filename='map.png')

        embed = discord.Embed(
            title=map.name,
            color=STANDARD_COLOR
        )
        embed.set_image(url="attachment://map.png")

        await interaction.followup.send(embed=embed, file=image)

    except FileNotFoundError:
        error_embed = discord.Embed(
            title="Error",
            description="Map not found",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)