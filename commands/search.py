import discord, re
from discord import app_commands

from utils.load_json import load_json
from utils.text_format import italic_font
from utils.paginator_view import PaginatorView
from utils.autocomplete import translation_autocomplete

from utils.error_embed import (
    no_verses_found_embed,
    incorrect_translation_embed,
    set_default_translation_embed
)

from config.paths import TRANSLATIONS
from config.colors import STANDARD_COLOR

from services.user_translation_db import get_user_settings
from services.bibles_db import search_verses, count_verses

def create_embed(title: str, message: str, translation: str, verse_count: int) -> discord.Embed:
    description = f"Verses count: **{verse_count}**\nBible translation: **{translation}**\n\n{message}"
    return discord.Embed(
        title=title,
        description=description,
        color=STANDARD_COLOR
    )

@app_commands.command(name="search", description="Searches for passages containing a specific word or phrase")
@app_commands.describe(text="Enter a word or phrase", translation="Select a Bible translation")
@app_commands.autocomplete(translation=translation_autocomplete)
async def search(interaction: discord.Interaction, text: str, translation: str = None):
    user_id = interaction.user.id
    user_data = get_user_settings(user_id)

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

    words = text.split()
    total_verses = count_verses(chosen_translation, words)
    results = search_verses(chosen_translation, words)

    if not results:
        await interaction.response.send_message(embed=no_verses_found_embed(text), ephemeral=True)
        return
    
    await interaction.response.defer()

    title = f"Search results for: {text}"

    embeds = []
    message = ""

    for row in results:
        book_name, book_number, chapter, verse_number, verse_text = row

        bold_text = verse_text
        italic_bold_text = italic_font(bold_text)

        for word in words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            bold_text = pattern.sub(lambda m: f"**{m.group(0)}**", bold_text)

        passage = f"**{book_name} {chapter}:{verse_number}** \n{italic_bold_text}\n\n"

        if len(message) + len(passage) < 600:
            message += passage
        else:
            embeds.append(create_embed(title, message, translations[chosen_translation], total_verses))
            message = passage

    if message:
        embeds.append(create_embed(title, message, translations[chosen_translation], total_verses))

    view = PaginatorView(embeds)
    await interaction.followup.send(embed=view.initial, view=view)