import discord, re

from discord import app_commands
from services.bibles_db import get_verses

from config.colors import STANDARD_COLOR
from config.paths import TRANSLATIONS, BOOKS

from utils.load_json import load_json
from utils.text_format import italic_font

from utils.error_embed import (
    verse_not_found_embed,
    incorrect_book_name_embed,
    incorrect_translation_embed,
    incorrect_verse_format_embed
)

from utils.autocomplete import (
    book_name_autocomplete,
    translation_autocomplete
)

@app_commands.command(
    name="compare", 
    description="Compares a passage in different Bible translations"
)

@app_commands.describe(
    book="Select a book",
    chapter="Enter a chapter number",
    verses="Enter a verse range, for example: 1 or 16-17",
    translation_1="Select a first Bible translation",
    translation_2="Select a second Bible translation",
    translation_3="Select a third Bible translation",
    translation_4="Select a fourth Bible translation"
)

@app_commands.autocomplete(
    translation_1=translation_autocomplete, 
    translation_2=translation_autocomplete,
    translation_3=translation_autocomplete,
    translation_4=translation_autocomplete,
    book=book_name_autocomplete
)

async def compare(
    interaction: discord.Interaction,
    book: str,
    chapter: int,
    verses: str,
    translation_1: str,
    translation_2: str,
    translation_3: str = None,
    translation_4: str = None
):
    book_names = load_json(BOOKS)
    translations = load_json(TRANSLATIONS)

    if book not in book_names:
        await interaction.response.send_message(embed=incorrect_book_name_embed(book), ephemeral=True)
        return
    
    selected_translations = [
        translation for translation in [
            translation_1, 
            translation_2, 
            translation_3, 
            translation_4
        ] 
        if translation
    ]
    
    for translation in selected_translations:
        if translation not in translations:
            await interaction.response.send_message(embed=incorrect_translation_embed(translation), ephemeral=True)
            return
    
    match = re.match(r"^(\d+)(?:-(\d+))?$", verses)

    if not match:
        await interaction.response.send_message(embed=incorrect_verse_format_embed(verses), ephemeral=True)
        return

    start_verse = int(match.group(1))
    end_verse = int(match.group(2)) if match.group(2) else start_verse

    await interaction.response.defer()

    passages = []

    for translation in selected_translations:
        result = get_verses(translation, book, chapter, start_verse, end_verse)

        if not result:
            await interaction.followup.send(embed=verse_not_found_embed())
            return
        
        passages.append((translation, result))
    
    def format_passage(verses_list):
        return " ".join(
            f"**({verse_number})** {italic_font(text)}" for verse_number, text in verses_list
        )

    embed = discord.Embed(
        title=f"Comparison of the passage: {book} {chapter}:{verses}",
        color=STANDARD_COLOR
    )

    for translation, verses in passages:
        embed.add_field(
            name=translations[translation], 
            value=format_passage(verses), 
            inline=False
        )
    await interaction.followup.send(embed=embed)