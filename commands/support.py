import discord, os

from dotenv import load_dotenv
from discord import app_commands
from config.colors import STANDARD_COLOR

load_dotenv()

SERVER_LINK = os.getenv("SERVER_LINK")

class InviteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Join the server", url=SERVER_LINK))

@app_commands.command(name="support", description="Support Server")
async def support(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Support Server",
        description=(
            "Have questions, suggestions or want to report a problem? "
            "Join our support server, where you'll get help from the community and the bot developer!"
        ),
        color=STANDARD_COLOR
    )
    view = InviteView()
    await interaction.response.send_message(embed=embed, view=view)