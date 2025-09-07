import discord, pytz, requests

from bs4 import BeautifulSoup
from datetime import datetime
from discord.ext import tasks
from colorama import Fore, init
from utils.load_json import load_json
from utils.get_passage import get_passage
from utils.italic_font import italic_font
from config.colors import STANDARD_COLOR
from config.paths import TRANSLATIONS, ALTERNATIVE_BOOK_NAMES
from services.user_translation_db import get_user_settings
from services.dailyverse_settings_db import get_all_dailyverse_settings

init(autoreset=True)

bot_instance = None

def get_canonical_book_name(book, books):
    for canonical_book_name, aliases in books.items():
        if book in aliases:
            return canonical_book_name
    return book

@tasks.loop(minutes=1)
async def dailyverse_task():
    now_utc = datetime.utcnow()
    settings = get_all_dailyverse_settings()

    books = load_json(ALTERNATIVE_BOOK_NAMES)
    translations = load_json(TRANSLATIONS)

    try:
        response = requests.get("https://www.biblestudytools.com/bible-verse-of-the-day/")
        soup = BeautifulSoup(response.text, 'html.parser')
        reference_div = soup.find("div", class_="w-full mb-5")
        link = reference_div.find("a", href=True)
        verse_reference = link.text.strip()

        book, chapter_verse = verse_reference.rsplit(" ", 1)
        chapter, verses = chapter_verse.split(":")
        chapter = int(chapter)
        verse_range = verses.split("-")
        start_verse = int(verse_range[0])
        end_verse = int(verse_range[1]) if len(verse_range) > 1 else start_verse

        canonical_book_name = get_canonical_book_name(book, books)

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

            passage = get_passage(translation, canonical_book_name, chapter, start_verse, end_verse)

            if not passage:
                continue

            desc = ""
            for verse in passage["verses"]:
                verse_text = italic_font(verse["text"]).replace("\n", " ").replace("  ", " ").strip()
                desc += f"**({verse['verse']})** {verse_text} "

            desc = (desc[:4093] + '...') if len(desc) > 4093 else desc

            title = f"{book} {chapter}:{start_verse}" if start_verse == end_verse else f"{book} {chapter}:{start_verse}-{end_verse}"

            embed = discord.Embed(title=title, description=desc, color=STANDARD_COLOR)
            embed.set_footer(text=translations.get(translation, translation))

            channel = bot_instance.get_channel(channel_id)

            if channel:
                await channel.send(embed=embed)

        except Exception as e:
            print(f"{Fore.RED}[X] Error sending daily verse to user {user_id}: {e}")

def start_dailyverse_task(bot):
    global bot_instance
    bot_instance = bot
    dailyverse_task.start()