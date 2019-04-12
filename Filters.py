"""
Casey Edmonds-Estes
Project 2
10/31/18
"""

import re

EXTS = ["jpg", "jpeg", "svg", "png", "pdf",
        "gif", "bmp", "mp3", "dvi"]
EMAIL_REGEX = r'[a-zA-Z0-9!#$%&\'*+-/=?^_`{|}~.]+@[a-zA-Z0-9\-]+[.][a-zA-Z-]+'
PHONE_REGEX = r'[\d]{3}[\D]*[2-9][0-9]{2}[\D]*[0-9]{4}'


# '<a' + _not >_ + 'href=' + _quote_ + 'http://' + _nonquote_ + _quote_
URL_REGEX = '''<a[^>]+href\s*=\s*["'](http://\S+{}\.{}[^"']+?)["']'''

def filter_urls(text, domain='bowdoin.edu'):
    """
    returns a list of urls found in the string 'text'
    """
    def extension_is_valid(url):
        """ Checks if the potential URL is valid.
        Media files, for example, are not.
        """
        EXTS = ["jpg", "jpeg", "svg", "png", "pdf",
                "gif", "bmp", "mp3", "dvi"]
        for e in EXTS:
            if url.lower().endswith(e):
                return False
        return True

    domain, tld = domain.split(".")
    regex = re.compile(URL_REGEX.format(domain, tld))

    urls = re.findall(regex, text)
    return [url for url in urls if extension_is_valid(url)]


def filter_emails(text):
    """Looks through a string and returns a list of all the email adresses"""
    return re.findall(EMAIL_REGEX, text)

def filter_phones(text):
    """Looks through a string and returns a list of all the phone number"""
    unformatted_numbers = re.findall(PHONE_REGEX, text)
    formatted_numbers = []
    for number in unformatted_numbers:
        formatted_number = ''
        for char in number:
            if re.match(r'[0-9]', char):
                formatted_number += str(char)
        formatted_number = (formatted_number[0:3] + '-'+
                            formatted_number[3:6] + '-' + formatted_number[6::])
        formatted_numbers.append(formatted_number)
    return formatted_numbers
