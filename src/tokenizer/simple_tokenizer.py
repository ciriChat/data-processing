import re

NON_ALPHA_REGEX = re.compile('[^A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ ]+')


def remove_non_word_chars(text: str):
    return NON_ALPHA_REGEX.sub('', text).strip()


def get_words(text: str):
    return text.lower().split()


def tokenize(text: str):
    return get_words(remove_non_word_chars(text))
