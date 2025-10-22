from discord.ext import commands
from importlib import import_module

def load_events(client: commands.Bot):
    event_modules = {
        'events.on_ready': 'setup_ready_event',
        'events.on_message': 'setup_message_event',
        'events.on_guild_join': 'setup_guild_join_event',
        'events.on_command_error': 'setup_command_error_event'
    }

    for module_name, setup_function_name in event_modules.items():
        module = import_module(module_name)
        setup_function = getattr(module, setup_function_name)
        setup_function(client)


def load_slash_commands(client: commands.Bot):
    slash_commands = [
        'cleardailyverse', 'cleartranslation', 'compare', 'dailyverse', 
        'help', 'information', 'maps', 'mysettings', 'passage', 'stats',
        'random', 'search', 'setdailyverse', 'setversion', 'versions'
    ]

    for command_name in slash_commands:
        module = import_module(f'commands.{command_name}')
        command = getattr(module, command_name)
        client.tree.add_command(command)