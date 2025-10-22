import discord
from colorama import Fore, init

from config.paths import TRANSLATIONS
from config.colors import STANDARD_COLOR

from utils.load_json import load_json
from utils.text_format import italic_font
from utils.get_passage import get_passage
from utils.paginator_view import PaginatorView
from utils.error_embed import search_error_embed
from utils.find_bible_references import find_bible_references

from services.user_translation_db import get_user_settings

init(autoreset=True)

def setup_message_event(client):
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('/setversion'):
            return

        user_id = message.author.id
        user_data = get_user_settings(user_id)
        translation = user_data[1] if user_data else None

        if not translation:
            return
        
        words = message.content.split()

        if words:
            abbreviation = words[-1]
            translation_abbreviations = load_json(TRANSLATIONS)

            if abbreviation in translation_abbreviations:
                translation = abbreviation
                message.content = ' '.join(words[:-1])

        await client.process_commands(message)

        try:
            await process_message_with_translation(message, translation)
        except discord.errors.Forbidden:
            print(f"{Fore.RED}[X] Missing permissions to send message in channel")
        except discord.errors.HTTPException as e:
            print(f"{Fore.RED}[X] HTTP error sending message in channel: {e}")
        except discord.errors.NotFound:
            print(f"{Fore.RED}[X] Channel not found")
        except Exception as e:
            print(f"{Fore.RED}[X] Unexpected error in on_message: {e}")

async def process_message_with_translation(message, translation):
    translations = load_json(TRANSLATIONS)
    verses = find_bible_references(message.content)

    if not verses:
        return

    for verse in verses:
        book, chapter, start, end = verse

        if start is None and end is None:
            start, end = 1, 300
        elif start is not None and end is None:
            end = start

        passage = get_passage(translation, book, chapter, start, end)

        if not passage or "passages" not in passage:
            try:
                await message.channel.send(embed=search_error_embed())
            except discord.DiscordException as e:
                print(f"{Fore.RED}[X] Error sending search error embed: {e}")
            continue

        embeds = []
        description = ""
        
        header = f'{passage["book_name"]} {passage["chapter"]}:{passage["verses_range"]}'
        bible_translation = translations.get(translation, translation)

        for verse_item in passage["passages"]:
            formatted_text = italic_font(verse_item["text"]).replace("\n", " ").replace("  ", " ").strip()
            passages = f"**({verse_item['verse']})** {formatted_text} "

            if len(description) + len(passages) > 1500:
                embed = discord.Embed(title=header, description=description.strip(), color=STANDARD_COLOR)
                embeds.append(embed)
                description = ""

            description += passages

        if description:
            embed = discord.Embed(
                title=header, 
                description=description.strip(), 
                color=STANDARD_COLOR
            )
            embeds.append(embed)

        if len(embeds) == 1:
            embeds[0].set_footer(text=bible_translation)
            await message.channel.send(embed=embeds[0])
        else:
            view = PaginatorView(embeds, bible_translation=bible_translation)
            await message.channel.send(embed=view.initial, view=view)