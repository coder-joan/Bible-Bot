import discord
from config.colors import ERROR_COLOR

def create_error_embed(title: str, description: str) -> discord.Embed:
    return discord.Embed(title=title, description=description, color=ERROR_COLOR)

def set_default_translation_embed() -> discord.Embed:
    return create_error_embed(
        "Error",
        f"Set a default Bible translation using the `/setversion` command"
    )

def hour_error_embed() -> discord.Embed:
    return create_error_embed(
        "Error",
        f"Hour must be between 1 and 12"
    )

def verse_not_found_embed() -> discord.Embed:
    return create_error_embed(
        "Error",
        f"Verse not found"
    )

def map_not_found_embed() -> discord.Embed:
    return create_error_embed(
        "Error",
        f"Map not found"
    )

def no_data_embed() -> discord.Embed:
    return create_error_embed(
        "No data",
        f"Your data not found in the database"
    )

def no_verses_found_embed(text: str) -> discord.Embed:
    return create_error_embed(
        "Error",
        f"No verses found containing: **{text}**"
    )

def incorrect_timezone_embed() -> discord.Embed:
    return create_error_embed(
        "Error",
        f"An incorrect time zone has been provided. Use autocomplete"
    )

def incorrect_book_name_embed(book: str) -> discord.Embed:
    return create_error_embed(
        "Error",
        f"An incorrect book name has been provided. Use autocomplete"
    )

def incorrect_translation_embed(translation: str) -> discord.Embed:
    return create_error_embed(
        "Error",
        f"An incorrect Bible translation has been provided. Use autocomplete"
    )

def incorrect_verse_format_embed(verses: str) -> discord.Embed:
    return create_error_embed(
        "Error",
        f"An incorrect verse format has been provided. Use, for example: `1` or `1-3`"
    )

def search_error_embed() -> discord.Embed:
    return create_error_embed(
        "Search error",
        (
            "Possible reasons for the error:\n\n"

            "- the verse does not exist\n"
            "- the translation missing Old or New Testament\n"
            "- the book is not available in this translation\n\n"
            
            "Check your input and try again"
        )
    )