import pytz, discord

from discord import app_commands, Interaction
from utils.load_json import load_json
from config.paths import TRANSLATIONS, BOOKS

async def translation_autocomplete(
    interaction: Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    bible_translations = load_json(TRANSLATIONS)
    return [
        app_commands.Choice(name=full_name, value=abbreviation)
        for abbreviation, full_name in bible_translations.items()
        if current.lower() in full_name.lower()
    ][:25]

async def book_name_autocomplete(interaction: Interaction, current: str):
    book_names = load_json(BOOKS)
    return [
        app_commands.Choice(name=book_name, value=book_name)
        for book_name in book_names
        if current.lower() in book_name.lower()
    ][:25]

async def timezone_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=tz, value=tz)
        for tz in pytz.all_timezones if current.lower() in tz.lower()
    ][:25]
