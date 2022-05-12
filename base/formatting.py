import re


def format_string(string: str):
    return re.sub("[^a-z]+", " ", string.lower()).strip()


def compare_strings(string1: str, string2: str):
    string1 = format_string(string1).replace(" ", "")
    string2 = format_string(string2)
    for c in string1:
        if c not in string2:
            return False
    return True
