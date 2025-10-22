import discord

from discord.ext import commands
from colorama import Fore, Style, init
from tasks.dailyverse_task import start_dailyverse_task

init(autoreset=True)

def setup_ready_event(client: commands.Bot):
    @client.event
    async def on_ready():
        print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Logged in as: {Fore.CYAN}{client.user}")
        await client.change_presence(activity=discord.Activity(name='Bible', type=discord.ActivityType.watching))
        
        try:
            synced = await client.tree.sync()
            print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Synchronized {Fore.YELLOW}{len(synced)}{Style.RESET_ALL} commands")
        except Exception as e:
            print(f"{Fore.RED}[X] Command synchronization error: {e}")

        start_dailyverse_task(client)