import re
from html import unescape

from poems.models import Poem


def remove_html_tags(text):
    # Pattern to remove any HTML tags
    text = unescape(text)
    clean_text = re.sub('<.*?>', '', text)
    clean_text = re.sub('[\r\t]+', '', clean_text)
    clean_text = re.sub(' +', ' ', clean_text).strip()
    return clean_text


def main():
    poems = Poem.objects.all()
    for poem in poems:
        poem.text = remove_html_tags(poem.text)
        poem.save()
