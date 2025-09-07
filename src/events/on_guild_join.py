import discord, os

from dotenv import load_dotenv
from colorama import Fore, init
from discord.ext import commands
from config.colors import STANDARD_COLOR

load_dotenv()
init(autoreset=True)

SERVER_LINK = os.getenv("SERVER_LINK")

class InviteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Join the bot support server", url=SERVER_LINK))

def setup_guild_join_event(client: commands.Bot):
    @client.event
    async def on_guild_join(guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="Thank you for adding Bible Bot!",
                    description=(
                        "I'm excited to be part of your server!\n\n"

                        "**Bot features:**\n"
                        "- 📅 sending the verse of the day\n"
                        "- 🎲 sending a random Bible verse\n"
                        "- 🔍 searching for Bible passages\n"
                        "- 📖 ability to use book abbreviations\n"
                        "- 📚 setting a default Bible translation\n"
                        "- 🔁 automatically sending the daily verse\n"
                        "- 📑 comparing passages in different Bible translations\n\n"

                        "**Getting started:**\n"
                        "1. Set your default Bible translation: `/setversion`\n"
                        "2. Configure automation of the daily verse: `/setdailyverse`\n\n"
                        
                        "Have questions, suggestions or want to report a problem? **Join the support server**, "
                        "where you'll get help from the community and the bot developer!"
                    ),
                    color=STANDARD_COLOR
                )

                view = InviteView()
                
                try:
                    await channel.send(embed=embed, view=view)
                except discord.errors.Forbidden:
                    print(f"{Fore.RED}[X] Error sending message to server: Missing Permissions")
                except Exception as e:
                    print(f"{Fore.RED}[X] Unexpected error in on_guild_join: {e}")
                break