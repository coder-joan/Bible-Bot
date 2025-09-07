import sqlite3

def get_bible_connection():
    return sqlite3.connect("data/bibles.db")

def get_passages():
    return '''
        SELECT book_name, chapter, verse, text FROM bible
        WHERE translation = ?
          AND book_name = ?
          AND chapter = ?
          AND verse BETWEEN ? AND ?
        GROUP BY verse
        ORDER BY verse
    '''

def get_random_verse(cursor, translation: str):
    cursor.execute('''
        SELECT book_name, book, chapter, verse, text
        FROM bible
        WHERE translation = ?
        ORDER BY RANDOM()
        LIMIT 1
    ''', (translation,))
    return cursor.fetchone()

def get_following_verses(cursor, translation: str, book: int, chapter: int, start_verse: int, limit: int = 10):
    cursor.execute('''
        SELECT verse, text
        FROM bible
        WHERE translation = ? AND book = ? AND chapter = ? AND verse >= ?
        GROUP BY verse
        ORDER BY verse
        LIMIT ?
    ''', (translation, book, chapter, start_verse, limit))
    return cursor.fetchall()

def search_verses(translation: str, words: list[str]) -> list[tuple]:
    filters = " AND ".join(["text LIKE ?"] * len(words))
    params = [f"%{word}%" for word in words]
    params.insert(0, translation)

    query = f"""
        SELECT DISTINCT book_name, book, chapter, verse, text
        FROM bible
        WHERE translation = ?
        AND {filters}
    """

    conn = get_bible_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    return results

def count_verses(translation: str, words: list[str]) -> int:
    filters = " AND ".join(["text LIKE ?"] * len(words))
    params = [f"%{word}%" for word in words]
    params.insert(0, translation)

    query = f"""
        SELECT COUNT(*) FROM (
            SELECT DISTINCT book, chapter, verse
            FROM bible
            WHERE translation = ?
            AND {filters}
        ) AS subquery
    """

    conn = get_bible_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)
    count = cursor.fetchone()[0]
    conn.close()

    return count

def get_verses(translation, book, chapter, start_verse, end_verse):
    conn = get_bible_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT DISTINCT verse, text
        FROM bible
        WHERE translation = ? AND book_name = ? AND chapter = ? AND verse BETWEEN ? AND ?
        ORDER BY verse
    ''', (translation, book, chapter, start_verse, end_verse))

    result = cursor.fetchall()
    conn.close()

    return result