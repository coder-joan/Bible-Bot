import discord, requests
from discord import app_commands

from utils.load_json import load_json
from utils.text_format import italic_font
from utils.get_passage import get_passage
from utils.autocomplete import translation_autocomplete

from utils.error_embed import (
    verse_not_found_embed,
    incorrect_translation_embed,
    set_default_translation_embed
)

from config.colors import STANDARD_COLOR
from config.paths import TRANSLATIONS, ALTERNATIVE_BOOK_NAMES

from services.user_translation_db import get_user_settings
from services.dailyverse_automation_db import get_dailyverse_automation_settings

def get_alternative_book_name(book, books):
    for alternative_book_name, aliases in books.items():
        if book in aliases:
            return alternative_book_name
    return book

@app_commands.command(name="dailyverse", description="Displays the verse of the day")
@app_commands.describe(translation="Select a Bible translation")
@app_commands.autocomplete(translation=translation_autocomplete)

async def dailyverse(interaction: discord.Interaction, translation: str = None):
    translations = load_json(TRANSLATIONS)
    books = load_json(ALTERNATIVE_BOOK_NAMES)

    user_id = interaction.user.id
    guild_id = interaction.guild.id

    user_data = get_user_settings(user_id)
    user_settings = get_dailyverse_automation_settings(user_id, guild_id)

    if translation:
        chosen_translation = translation
    elif user_data:
        chosen_translation = user_data[1]
    else:
        await interaction.response.send_message(embed=set_default_translation_embed(), ephemeral=True)
        return

    if chosen_translation not in translations:
        await interaction.response.send_message(embed=incorrect_translation_embed(translation), ephemeral=True)
        return
    
    await interaction.response.defer()

    try:
        response = requests.get("https://beta.ourmanna.com/api/v1/get/?format=json", timeout=10)

        if response.status_code != 200:
            await interaction.followup.send(embed=verse_not_found_embed())
            return

        data = response.json()
        verse_data = data["verse"]["details"]
        reference = verse_data["reference"]

        try:
            book, chapter_verse = reference.rsplit(" ", 1)
            chapter, verses = chapter_verse.split(":")
            chapter = int(chapter)
            verse_range = verses.split("-")

            start_verse = int(verse_range[0])
            end_verse = int(verse_range[1]) if len(verse_range) > 1 else start_verse

        except Exception:
            await interaction.followup.send(embed=verse_not_found_embed(), ephemeral=True)
            return

        book_name = get_alternative_book_name(book, books)
        passage = get_passage(chosen_translation, book_name, chapter, start_verse, end_verse)

        if passage:
            description = ""

            for verse in passage["passages"]:
                formatted_text = italic_font(verse["text"]).replace("\n", " ").replace("  ", " ").strip()
                description += f"**({verse['verse']})** {formatted_text} "
        else:
            await interaction.followup.send(embed=verse_not_found_embed(), ephemeral=True)

        if start_verse == end_verse:
            title = f"{book} {chapter}:{start_verse}" 
        else:
            title = f"{book} {chapter}:{start_verse}-{end_verse}"

        description = (description[:4093] + '...') if len(description) > 4093 else description

        embed = discord.Embed(
            title=title,
            description=description,
            color=STANDARD_COLOR
        )
        embed.set_footer(text=translations.get(chosen_translation, chosen_translation))
        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(embed=verse_not_found_embed(), ephemeral=True)