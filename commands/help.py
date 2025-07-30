import discord

from discord import app_commands
from config.colors import STANDARD_COLOR
from utils.paginator_view import PaginatorView

@app_commands.command(name="help", description="How to use the Bible Bot")
async def help(interaction: discord.Interaction):
    description = [
        f'Before you start searching for Bible passages, '
         'set a default Bible translation using the `/setversion` command\n\n'

         '**Bible passage search format:**\n'
         '- `[book] [chapter]:[verses] [translation]`\n\n'

         '**Examples:**\n'
         '- `John 3:16` - single verse\n'
         '- `John 3:1-8` - range of verses\n'
         '- `John 1:12-13 KJV` - range of verses with Bible translation\n\n'

         'If you have a default Bible translation set, you don’t need to include its abbreviation',

        f'List of commands:\n\n'

         '- `/dailyverse` - displays the verse of the day\n'
         '- `/maps` - displays selected map from the Bible\n'
         '- `/passage` - displays a passage from the Bible\n'
         '- `/search` - searches for passages in the Bible\n'
         '- `/setversion` - sets a default Bible translation\n'
         '- `/setdailyverse` - sets up daily verse automation\n'
         '- `/mysettings` - displays the current user settings\n'
         '- `/versions` - shows available Bible translations\n'
         '- `/random` - displays a random verse from the Bible\n'
         '- `/information` - displays information about the bot\n'
         '- `/invite` - provides an invitation link to the server\n'
         '- `/cleardailyverse` - deletes daily verse automation\n'
         '- `/cleartranslation` - deletes the user-set translation\n'
         '- `/compare` - compares a passage in different Bible translations\n\n'

        'Have questions or suggestions? Use the `/support` command'
    ]

    embeds = [discord.Embed(title="Help", description=desc, color=STANDARD_COLOR) for desc in description]
    view = PaginatorView(embeds)
    await interaction.response.send_message(embed=view.initial, view=view)