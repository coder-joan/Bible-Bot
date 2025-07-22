import re
from utils.load_json import load_json
from config.paths import ALTERNATIVE_BOOK_NAMES

def find_bible_references(text):
    books = load_json(ALTERNATIVE_BOOK_NAMES)

    pattern = r"\b("
    pattern += "|".join(books.keys())
    pattern += r"|"
    pattern += "|".join([abbr for abbrs in books.values() for abbr in abbrs])
    pattern += r")\s+(\d+)(?::(\d+))?(?:-(\d+))?\b"

    regex = re.compile(pattern, re.IGNORECASE)
    matches = regex.findall(text)

    references = []
    for match in matches:
        full_book_name = next(
            (book for book, abbreviations in books.items() if match[0].lower() in abbreviations), match[0])
        references.append((
            full_book_name,
            int(match[1]),
            int(match[2]) if match[2] else None,
            int(match[3]) if match[3] else None
        ))
    return references