import discord

from dotenv import load_dotenv
from discord import app_commands

from config.colors import STANDARD_COLOR
from utils.paginator_view import PaginatorView

load_dotenv()

@app_commands.command(name="help", description="How to use the Bible Bot")
async def help(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    description = [
        f'Before you start searching for Bible passages, '
         'set a default Bible translation using the `/setversion` command\n\n'

         '**Bible passage search format:**\n'
         '- `[book] [chapter] [translation]`\n'
         '- `[book] [chapter]:[verses] [translation]`\n\n'

         '**Examples:**\n'
         '- `John 3:16` - single verse\n'
         '- `John 3:1-8` - range of verses\n'
         '- `John 1 KJV` - chapter with Bible translation\n'
         '- `John 1:12-13 KJV` - range of verses with Bible translation\n\n'

         'If you don’t want to set a default Bible translation - you can '
         'choose the translation in slash commands\n\n',

        f'List of commands:\n\n'

         '- `/maps` - displays selected map\n'
         '- `/random` - displays a random verse\n'
         '- `/dailyverse` - displays the verse of the day\n'
         '- `/passage` - displays a passage from the Bible\n'
         '- `/versions` - shows available Bible translations\n'
         '- `/setversion` - sets a default Bible translation\n'
         '- `/setdailyverse` - sets up daily verse automation\n'
         '- `/mysettings` - displays the current user settings\n'
         '- `/information` - displays information about the bot\n'
         '- `/cleardailyverse` - deletes daily verse automation\n'
         '- `/cleartranslation` - deletes the default translation\n'
         '- `/compare` - compares a passage in different Bible translations\n'
         '- `/search` - searches for passages containing a specific word or phrase'
    ]

    embeds = [discord.Embed(title="Help", description=desc, color=STANDARD_COLOR) for desc in description]
    view = PaginatorView(embeds)

    await interaction.followup.send(embed=view.initial, view=view)