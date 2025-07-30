import discord, os

from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

INVITE_LINK = os.getenv("INVITE_LINK")

class InviteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Add the bot", url=INVITE_LINK))

@app_commands.command(name="invite", description="Add the bot to your server")
async def invite(interaction: discord.Interaction):
    view = InviteView()
    await interaction.response.send_message(view=view)