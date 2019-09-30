#!/bin/usr/env python3
import sys
import time
import hashlib
import requests
from urllib.parse import unquote


def get_data(domain):
    file_name = domain.replace("*.","") + ".txt"
    url = "http://web.archive.org/cdx/search/cdx?url={}/*&output=text&fl=original&collapse=urlkey"
    res = requests.get(url.format(domain), stream=True, timeout=60)
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(unquote(res.text))

def main():
    try:
        domain = [sys.argv[1]]
    except IndexError:
        domain = sys.stdin
        if domain.isatty(): print("[x] Domain is missing"); exit()

    for dom in domain:
        dom = dom.rstrip("\n")
        print( "[i] Getting urls for: %s" % dom )
        get_data(dom)

if __name__ == "__main__":
    main()