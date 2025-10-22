import discord

from random import randint
from discord import app_commands

from config.paths import TRANSLATIONS
from config.colors import STANDARD_COLOR

from utils.load_json import load_json
from utils.text_format import italic_font
from utils.autocomplete import translation_autocomplete

from utils.error_embed import (
    verse_not_found_embed,
    incorrect_translation_embed,
    set_default_translation_embed
)

from services.user_translation_db import get_user_settings

from services.bibles_db import (    
    get_random_verse, 
    get_bible_connection, 
    get_following_verses
)

@app_commands.command(name="random", description="Displays a random verse")
@app_commands.describe(translation="Select a Bible translation")
@app_commands.autocomplete(translation=translation_autocomplete)
async def random(interaction: discord.Interaction, translation: str = None):
    user_id = interaction.user.id
    user_data = get_user_settings(user_id)

    translations = load_json(TRANSLATIONS)

    if translation:
        chosen_translation = translation
    elif user_data:
        chosen_translation = user_data[1]
    else:
        await interaction.response.send_message(embed=set_default_translation_embed(), ephemeral=True)
        return

    translations = load_json(TRANSLATIONS)
    
    if chosen_translation not in translations:
        await interaction.response.send_message(embed=incorrect_translation_embed(translation), ephemeral=True)
        return

    conn = get_bible_connection()
    cursor = conn.cursor()

    row = get_random_verse(cursor, chosen_translation)

    if not row:
        await interaction.response.send_message(embed=verse_not_found_embed(), ephemeral=True)
        return
    
    await interaction.response.defer()

    book_name, book_number, chapter, start_verse, text = row
    number_of_verses = randint(1, 10)

    verses = get_following_verses(
        cursor, 
        chosen_translation, 
        book_number, chapter, 
        start_verse, 
        number_of_verses
    )

    conn.close()

    first_verse, last_verse = verses[0][0], verses[-1][0]
    passages = ""
    
    for verse_number, passage in verses:
        formatted_text = italic_font(passage).replace("\n", " ").replace("  ", " ").strip()
        passages += f"**({verse_number})** {formatted_text} "

    if first_verse == last_verse:
        title = f"{book_name} {chapter}:{first_verse}"
    else:
        title = f"{book_name} {chapter}:{first_verse}-{last_verse}"

    embed = discord.Embed(
        title=title,
        description=passages[:4093],
        color=STANDARD_COLOR
    )
    embed.set_footer(text=translations.get(chosen_translation, chosen_translation))
    await interaction.followup.send(embed=embed)