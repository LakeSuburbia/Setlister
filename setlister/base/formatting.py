import re
import unicodedata


def format_string(string: str):
    byte_string = unicodedata.normalize("NFD", string).encode("ascii", "ignore")
    string = byte_string.decode("utf8")
    return re.sub("[^a-z]+", " ", string.lower()).strip()


def compare_strings(string1: str, string2: str):
    if format_string(string1) != format_string(string2):
        return False
    return True
