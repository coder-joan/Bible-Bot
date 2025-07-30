import discord, re

from discord import app_commands
from services.bibles_db import get_verses
from config.paths import TRANSLATIONS
from config.colors import STANDARD_COLOR, ERROR_COLOR
from utils.load_json import load_json
from utils.italic_font import italic_font
from utils.autocomplete import translation_autocomplete, book_name_autocomplete

@app_commands.command(name="compare", description="Compares a passage in different Bible translations")

@app_commands.describe(
    book="Select a book",
    chapter="Enter a chapter number",
    verses="Enter a verse range e.g. 16-17",
    translation_1="Select a first Bible translation",
    translation_2="Select a second Bible translation"
)

@app_commands.autocomplete(
    translation_1=translation_autocomplete, 
    translation_2=translation_autocomplete, 
    book=book_name_autocomplete
)

async def compare(
    interaction: discord.Interaction,
    book: str,
    chapter: int,
    verses: str,
    translation_1: str,
    translation_2: str
):
    await interaction.response.defer()

    translations = load_json(TRANSLATIONS)

    if book not in book:
        error_embed = discord.Embed(
            title="Error",
            description=(
                f"Invalid book name"
            ),
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return

    if translation_1 not in translations or translation_2 not in translations:
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

    verse_1 = get_verses(translation_1, book, chapter, start_verse, end_verse)
    verse_2 = get_verses(translation_2, book, chapter, start_verse, end_verse)

    verse = f"{book} {chapter}:{verses}"

    if not verse_1 or not verse_2:
        error_embed = discord.Embed(
            title="Error",
            description=f"Verse not found",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return
    
    def format_passage(verses_list):
        return " ".join(
            f"**({verse_number})** {italic_font(text)}" for verse_number, text in verses_list
        )

    embed = discord.Embed(
        title=f"Comparison of the passage: {verse}",
        description=(
            f"**{translations[translation_1]}**\n{format_passage(verse_1)}\n\n"
            f"**{translations[translation_2]}**\n{format_passage(verse_2)}"
        ),
        color=STANDARD_COLOR
    )
    await interaction.followup.send(embed=embed)