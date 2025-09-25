import discord, os

from dotenv import load_dotenv
from discord.ext import commands

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.events.on_ready import setup_ready_event
from src.events.on_message import setup_message_event
from src.events.on_guild_join import setup_guild_join_event
from src.events.on_command_error import setup_command_error_event

from src.commands.cleardailyverse import cleardailyverse
from src.commands.cleartranslation import cleartranslation
from src.commands.compare import compare
from src.commands.dailyverse import dailyverse
from src.commands.help import help
from src.commands.information import information
from src.commands.invite import invite
from src.commands.maps import maps
from src.commands.mysettings import mysettings
from src.commands.passage import passage
from src.commands.random import random
from src.commands.search import search
from src.commands.setdailyverse import setdailyverse
from src.commands.setversion import setversion
from src.commands.stats import stats
from src.commands.support import support
from src.commands.versions import versions

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

client.tree.add_command(cleardailyverse)
client.tree.add_command(cleartranslation)
client.tree.add_command(compare)
client.tree.add_command(dailyverse)
client.tree.add_command(help)
client.tree.add_command(information)
client.tree.add_command(invite)
client.tree.add_command(maps)
client.tree.add_command(mysettings)
client.tree.add_command(passage)
client.tree.add_command(random)
client.tree.add_command(search)
client.tree.add_command(setdailyverse)
client.tree.add_command(setversion)
client.tree.add_command(support)
client.tree.add_command(versions)
client.add_command(stats)

load_dotenv()
setup_ready_event(client)
setup_message_event(client)
setup_guild_join_event(client)
setup_command_error_event(client)

client.run(os.environ['TOKEN'])
