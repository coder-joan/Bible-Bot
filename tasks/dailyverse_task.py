import discord, pytz, requests

from datetime import datetime
from discord.ext import tasks
from colorama import Fore, init

from utils.load_json import load_json
from utils.get_passage import get_passage
from utils.text_format import italic_font

from config.colors import STANDARD_COLOR
from config.paths import TRANSLATIONS, ALTERNATIVE_BOOK_NAMES

from services.user_translation_db import get_user_settings
from services.dailyverse_automation_db import get_all_dailyverse_automation_settings

init(autoreset=True)
bot_instance = None

def get_alternative_book_name(book, books):
    for alternative_book_name, aliases in books.items():
        if book in aliases:
            return alternative_book_name
    return book

@tasks.loop(minutes=1)
async def dailyverse_task():
    now_utc = datetime.utcnow()
    settings = get_all_dailyverse_automation_settings()

    translations = load_json(TRANSLATIONS)
    books = load_json(ALTERNATIVE_BOOK_NAMES)

    try:
        response = requests.get("https://beta.ourmanna.com/api/v1/get/?format=json", timeout=10)
        response.raise_for_status()

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
            print(f"{Fore.RED}[X] Failed to parse verse reference: {reference}")
            return

        book_name = get_alternative_book_name(book, books)

    except Exception as e:
        print(f"{Fore.RED}[X] Failed to fetch verse of the day: {e}")
        return

    for user_id, guild_id, channel_id, hour, timezone in settings:
        try:
            tz = pytz.timezone(timezone)
            user_time = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)

            if user_time.hour != hour or user_time.minute != 0:
                continue

            user_data = get_user_settings(user_id)

            if not user_data or not user_data[1]:
                continue

            translation = user_data[1]
            passage = get_passage(translation, book_name, chapter, start_verse, end_verse)

            if passage:
                description = ""

                for verse in passage["passages"]:
                    formatted_text = italic_font(verse["text"]).replace("\n", " ").replace("  ", " ").strip()
                    description += f"**({verse['verse']})** {formatted_text} "
            else:
                print(f"{Fore.RED}[X] Verse not found: {e}")

            description = (description[:4093] + '...') if len(description) > 4093 else description

            if start_verse == end_verse:
                title = f"{book} {chapter}:{start_verse}" 
            else:
                title = f"{book} {chapter}:{start_verse}-{end_verse}"

            embed = discord.Embed(title=title, description=description, color=STANDARD_COLOR)
            embed.set_footer(text=translations.get(translation, translation))

            channel = bot_instance.get_channel(channel_id)

            if channel:
                await channel.send(embed=embed)

        except Exception as e:
            print(f"{Fore.RED}[X] Error sending daily verse to user: {e}")

def start_dailyverse_task(bot):
    global bot_instance
    bot_instance = bot
    dailyverse_task.start()