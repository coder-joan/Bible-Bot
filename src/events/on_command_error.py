from discord.ext import commands

def setup_command_error_event(client):
    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        raise error