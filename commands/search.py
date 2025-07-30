import discord, re

from discord import app_commands
from utils.load_json import load_json
from utils.italic_font import italic_font
from utils.paginator_view import PaginatorView
from utils.autocomplete import translation_autocomplete
from config.paths import TRANSLATIONS
from config.colors import STANDARD_COLOR, ERROR_COLOR
from services.user_translation_db import get_user_settings
from services.bibles_db import search_verses, count_verses

def create_embed(title: str, message: str, translation: str, verse_count: int) -> discord.Embed:
    description = f"Verses count: **{verse_count}**\nBible translation: **{translation}**\n\n{message}"
    return discord.Embed(
        title=title,
        description=description,
        color=STANDARD_COLOR
    )

@app_commands.command(name="search", description="Searching passages in the Bible")
@app_commands.describe(text="Enter a word or phrase", translation="Select a Bible translation")
@app_commands.autocomplete(translation=translation_autocomplete)
async def search(interaction: discord.Interaction, text: str, translation: str = None):
    await interaction.response.defer()

    user_id = interaction.user.id
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

    translations = load_json(TRANSLATIONS)

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

    words = text.split()
    total_verses = count_verses(chosen_translation, words)
    results = search_verses(chosen_translation, words)

    if not results:
        error_embed = discord.Embed(
            title="Error",
            description=f'No verses found containing: **{text}**',
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return

    title = f"Search results for: {text}"

    embeds = []
    message = ""

    for row in results:
        book_name, book_number, chapter, verse_number, verse_text = row

        bold_text = verse_text

        for word in words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            bold_text = pattern.sub(lambda m: f"**{m.group(0)}**", bold_text)

        italic_bold_text = italic_font(bold_text)
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