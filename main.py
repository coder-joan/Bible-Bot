import os

from dotenv import load_dotenv
from core.client import create_client
from core.loader import load_events, load_slash_commands

load_dotenv()
client = create_client()
load_events(client)
load_slash_commands(client)

client.run(os.environ["BOT_TOKEN"])