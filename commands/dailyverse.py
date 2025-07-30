import discord, requests

from discord import app_commands
from bs4 import BeautifulSoup
from utils.load_json import load_json
from utils.italic_font import italic_font
from utils.get_passage import get_passage
from utils.autocomplete import translation_autocomplete
from services.user_translation_db import get_user_settings
from services.dailyverse_settings_db import get_dailyverse_settings
from config.colors import STANDARD_COLOR, ERROR_COLOR
from config.paths import TRANSLATIONS, ALTERNATIVE_BOOK_NAMES

def get_canonical_book_name(book, books):
    for canonical_book_name, aliases in books.items():
        if book in aliases:
            return canonical_book_name
    return book

@app_commands.command(name="dailyverse", description="Displays the verse of the day")
@app_commands.describe(
    translation="Select a Bible translation"
)
@app_commands.autocomplete(translation=translation_autocomplete)
async def dailyverse(
    interaction: discord.Interaction,
    translation: str = None
):
    await interaction.response.defer()

    translations = load_json(TRANSLATIONS)
    books = load_json(ALTERNATIVE_BOOK_NAMES)

    user_id = interaction.user.id

    user_settings = get_dailyverse_settings(user_id)
    channel_id, hour, timezone = (user_settings if user_settings else (None, None, None))

    user_data = get_user_settings(user_id)

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

    try:
        response = requests.get("https://www.verseoftheday.com/")
        soup = BeautifulSoup(response.text, 'html.parser')
        reference_div = soup.find("div", class_="reference")
        link = reference_div.find("a", href=True)
        verse_reference = link.text.strip()

        book, chapter_verse = verse_reference.rsplit(" ", 1)
        chapter, verses = chapter_verse.split(":")
        chapter = int(chapter)

        verse_range = verses.split("-")
        start_verse = int(verse_range[0])
        end_verse = int(verse_range[1]) if len(verse_range) > 1 else start_verse

        canonical_book_name = get_canonical_book_name(book, books)

        passage = get_passage(chosen_translation, canonical_book_name, chapter, start_verse, end_verse)

        if not passage:
            error_embed = discord.Embed(
                title="Error",
                description="Verse not found in database",
                color=ERROR_COLOR
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return

        title = f"{book} {chapter}:{start_verse}" if start_verse == end_verse else f"{book} {chapter}:{start_verse}-{end_verse}"

        desc = ""
        for verse in passage["verses"]:
            verse_text = italic_font(verse["text"]).replace("\n", " ").replace("  ", " ").strip()
            desc += f"**({verse['verse']})** {verse_text} "

        desc = (desc[:4093] + '...') if len(desc) > 4093 else desc

        embed = discord.Embed(
            title=title,
            description=desc,
            color=STANDARD_COLOR
        )
        embed.set_footer(text=translations.get(chosen_translation, chosen_translation))

        await interaction.followup.send(embed=embed)

    except Exception as e:
        error_embed = discord.Embed(
            title="Error",
            description=f"Verse not found",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)