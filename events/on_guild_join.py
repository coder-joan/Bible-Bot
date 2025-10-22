import discord

from colorama import Fore, init
from discord.ext import commands

from config.colors import STANDARD_COLOR
from config.links import (
    INVITE_LINK,
    SERVER_LINK, 
    WEBSITE_LINK, 
    TOP_GG_LINK, 
    DISCORD_BOT_LIST_LINK
)

init(autoreset=True)

class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__()
        for buttons in [
            discord.ui.Button(label="Add Bible Bot", url=INVITE_LINK),
            discord.ui.Button(label="Support Server", url=SERVER_LINK),
            discord.ui.Button(label="Website", url=WEBSITE_LINK)
        ]:
            self.add_item(buttons)

def setup_guild_join_event(client: commands.Bot):
    @client.event
    async def on_guild_join(guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="Thank you for adding Bible Bot!",
                    description=(
                        "I'm excited to be part of your server!\n\n"

                        "**Getting started:**\n"
                        "1. Set your default Bible translation: `/setversion`\n"
                        "2. Configure automation of the daily verse: `/setdailyverse`\n\n"

                        f"Enjoying the bot? Don’t stop there - vote now and share your thoughts on "
                        f"[top.gg]({TOP_GG_LINK}) and [discordbotlist.com]({DISCORD_BOT_LIST_LINK})!"
                    ),
                    color=STANDARD_COLOR
                )
                
                view = Buttons()
                
                try:
                    await channel.send(embed=embed, view=view)
                except discord.errors.Forbidden:
                    print(f"{Fore.RED}[X] Missing permissions to send message in guild")
                except discord.errors.HTTPException as e:
                    print(f"{Fore.RED}[X] HTTP error sending message in guild: {e}")
                except discord.errors.NotFound:
                    print(f"{Fore.RED}[X] Channel not found in guild")
                except Exception as e:
                    print(f"{Fore.RED}[X] Unexpected error in on_guild_join: {e}")
                break