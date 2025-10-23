import re

def italic_font(text):
    return re.sub(r'\[([^\]]+)\]', r'*\1*', text)