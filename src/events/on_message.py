import discord

from colorama import Fore, init
from utils.load_json import load_json
from utils.italic_font import italic_font
from utils.get_passage import get_passage
from utils.find_bible_references import find_bible_references
from config.paths import TRANSLATIONS
from config.colors import STANDARD_COLOR, ERROR_COLOR
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
            last_word = words[-1]

            abbreviation = load_json(TRANSLATIONS)

            if last_word in abbreviation:
                translation = last_word
                message.content = ' '.join(words[:-1])

        await client.process_commands(message)

        try:
            await process_message_with_translation(message, translation)
        except discord.errors.Forbidden:
            print(f"{Fore.RED}[X] Error sending message to channel {message.channel.id}: Missing Permissions")
        except Exception as e:
            print(f"{Fore.RED}[X] Unexpected error in on_message: {e}")

async def process_message_with_translation(message, translation):
    bible_translations = load_json(TRANSLATIONS)

    bible_passage = []
    bible_verses = find_bible_references(message.content)

    for verse in bible_verses:
        book, chapter, start, end = verse
        if start is not None and end is not None:
            passage = get_passage(translation, book, chapter, start, end)
            bible_passage.append(passage)
        elif start is not None:
            passage = get_passage(translation, book, chapter, start, start)
            bible_passage.append(passage)

    for verses in bible_passage:
        if verses and "verses" in verses:
            header = f'{verses["book_name"]} {verses["chapter"]}:{verses["verses_range"]}'
            desc = ""

            for verse in verses["verses"]:
                verse_text = italic_font(verse["text"]).replace("\n", " ").replace("  ", " ").strip()
                desc += f"**({verse['verse']})** {verse_text} "

            desc = (desc[:4093] + '...') if len(desc) > 4093 else desc

            embed = discord.Embed(title=header, description=desc, color=STANDARD_COLOR)
            embed.set_footer(text=bible_translations.get(translation, translation))

            await message.channel.send(embed=embed)
            
        else:
            error_embed = discord.Embed(
                title="Search error",
                description=(
                    "The following are possible causes of the error:\n\n"

                    "- the verse does not exist\n"
                    "- the translation does not include the specified book\n"
                    "- the translation does not include the Old or New Testament\n\n"
                    
                    "Please make sure the input data is correct and try again"
                ),
                color=ERROR_COLOR
            )
            await message.channel.send(embed=error_embed)