import discord, re

from discord import app_commands
from config.paths import TRANSLATIONS, BOOKS
from config.colors import STANDARD_COLOR, ERROR_COLOR
from services.bibles_db import get_verses
from services.user_translation_db import get_user_settings
from utils.load_json import load_json
from utils.italic_font import italic_font
from utils.autocomplete import translation_autocomplete, book_name_autocomplete

@app_commands.command(name="passage", description="Displays a passage from the Bible")

@app_commands.describe(
    book="Select a book",
    chapter="Enter a chapter number",
    verses="Enter a verse range e.g. 16-17",
    translation="Select a Bible translation",
)

@app_commands.autocomplete(
    translation=translation_autocomplete, 
    book=book_name_autocomplete
)

async def passage(
    interaction: discord.Interaction,
    book: str,
    chapter: int,
    verses: str,
    translation: str = None
):
    await interaction.response.defer()

    user_id = interaction.user.id
    user_data = get_user_settings(user_id)

    translations = load_json(TRANSLATIONS)
    book_names = load_json(BOOKS)

    if book not in book_names:
        error_embed = discord.Embed(
            title="Error",
            description=(
                f"Invalid book name"
            ),
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return
    
    if translation:
        chosen_translation = translation
    elif user_data:
        chosen_translation = user_data[1]
    else:
        embed = discord.Embed(
            title="Set a default Bible translation",
            description=(
                'Before you start searching for Bible passages, '
                'set a default Bible translation using the `/setversion` command'
            ),
            color=STANDARD_COLOR
        )
        await interaction.followup.send(embed=embed)
        return

    if chosen_translation not in translations:
        error_embed = discord.Embed(
            title="Error",
            description=(
                "An incorrect Bible translation was provided. Use autocomplete or "
                "check the available translation abbreviations in the `/versions` command"
            ),
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return
    
    match = re.match(r"^(\d+)(?:-(\d+))?$", verses)

    if not match:
        error_embed=discord.Embed(
            title="Error",
            description="Invalid verse format. Enter for example `1` or `1-3`",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return

    start_verse = int(match.group(1))
    end_verse = int(match.group(2)) if match.group(2) else start_verse

    verse = get_verses(chosen_translation, book, chapter, start_verse, end_verse)

    passage = f"{book} {chapter}:{verses}"

    if not verse:
        error_embed = discord.Embed(
            title="Search error",
            description=(
                "The following are possible causes of the error:\n\n"

                "- the verse does not exist\n"
                "- the translation does not include the specified book\n"
                "- the translation does not include the Old or New Testament\n\n"
                
                "Please make sure the input data is correct and try again"
            ),
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return
    
    def format_passage(verses_list):
        return " ".join(
            f"**({verse_number})** {italic_font(text)}" for verse_number, text in verses_list
        )

    embed = discord.Embed(
        title=f"{passage}",
        description=(
            f"{format_passage(verse)}"
        ),
        color=STANDARD_COLOR
    )
    embed.set_footer(text=translations[chosen_translation])
    await interaction.followup.send(embed=embed)
