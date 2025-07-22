import discord, os

from dotenv import load_dotenv
from discord.ext import commands
from events.on_ready import setup_ready_event
from events.on_message import setup_message_event
from events.on_command_error import setup_command_error_event

from commands.compare import compare
from commands.dailyverse import dailyverse
from commands.help import help
from commands.information import information
from commands.invite import invite
from commands.maps import maps
from commands.passage import passage
from commands.random import random
from commands.removeuserdata import removeuserdata
from commands.search import search
from commands.setversion import setversion
from commands.stats import stats
from commands.support import support
from commands.versions import versions

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

client.tree.add_command(compare)
client.tree.add_command(dailyverse)
client.tree.add_command(help)
client.tree.add_command(information)
client.tree.add_command(invite)
client.tree.add_command(maps)
client.tree.add_command(passage)
client.tree.add_command(random)
client.tree.add_command(removeuserdata)
client.tree.add_command(search)
client.tree.add_command(setversion)
client.tree.add_command(support)
client.tree.add_command(versions)
client.add_command(stats)

load_dotenv()
setup_ready_event(client)
setup_message_event(client)
setup_command_error_event(client)

client.run(os.environ['TOKEN'])