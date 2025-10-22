import discord, re
from discord import app_commands

from config.colors import STANDARD_COLOR
from config.paths import TRANSLATIONS, BOOKS

from utils.load_json import load_json
from utils.text_format import italic_font
from utils.get_passage import get_passage
from utils.paginator_view import PaginatorView

from utils.autocomplete import (
    translation_autocomplete, 
    book_name_autocomplete
)

from utils.error_embed import (
    search_error_embed,
    incorrect_book_name_embed,
    incorrect_translation_embed,
    incorrect_verse_format_embed,
    set_default_translation_embed
)

from services.user_translation_db import get_user_settings

@app_commands.command(
    name="passage", 
    description="Displays a passage from the Bible"
)

@app_commands.describe(
    book="Select a book",
    chapter="Enter a chapter number",
    verses="Enter a verse range, for example: 1 or 16-17",
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
    verses: str = None,
    translation: str = None
):
    user_id = interaction.user.id
    user_data = get_user_settings(user_id)

    book_names = load_json(BOOKS)
    translations = load_json(TRANSLATIONS)

    if book not in book_names:
        await interaction.response.send_message(embed=incorrect_book_name_embed(book), ephemeral=True)
        return
    
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

    if verses:
        match = re.match(r"^(\d+)(?:-(\d+))?$", verses)

        if not match:
            await interaction.followup.send(embed=incorrect_verse_format_embed(verses), ephemeral=True)
            return

        start_verse = int(match.group(1))
        end_verse = int(match.group(2)) if match.group(2) else start_verse
    else:
        start_verse = 1
        end_verse = 300

    passages = get_passage(chosen_translation, book, chapter, start_verse, end_verse)

    if not passages or "passages" not in passages:
        await interaction.followup.send(embed=search_error_embed(), ephemeral=True)
        return

    title = f'{passages["book_name"]} {passages["chapter"]}:{passages["verses_range"]}'
    bible_translation = translations.get(chosen_translation, chosen_translation)
    
    embeds = []
    description = ""

    for verse_item in passages["passages"]:
        formatted_text = italic_font(verse_item["text"]).replace("\n", " ").replace("  ", " ").strip()
        formatted_passages = f"**({verse_item['verse']})** {formatted_text} "
    
        if len(description) + len(formatted_passages) > 1500:

            embed = discord.Embed(
                title=title,
                description=description.strip(),
                color=STANDARD_COLOR
            )
            embeds.append(embed)
            description = ""

        description += formatted_passages

    if description:
        embed = discord.Embed(
            title=title, 
            description=description.strip(), 
            color=STANDARD_COLOR
        )
        embeds.append(embed)

    if len(embeds) == 1:
        embeds[0].set_footer(text=bible_translation)
        await interaction.followup.send(embed=embeds[0])
    else:
        view = PaginatorView(embeds, bible_translation=bible_translation)
        await interaction.followup.send(embed=view.initial, view=view)