import unicodedata


def strip_accents(string):
    """ Strip accents from a string """

    text = ''.join((c for c in unicodedata.normalize('NFD', str(string))
                    if unicodedata.category(c) != 'Mn'))
    return text.replace('œ', 'oe').replace('Œ', 'OE').replace(',', '_')\
        .replace('&', '_et_').replace('\'', '').replace('\"', '')


def searchalize(string):
    return strip_accents(string.lower()).replace("-", " ")\
        .replace('saint', 'st')
