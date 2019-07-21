#!/bin/usr/env python3
import sys
import time
import hashlib
import requests
from urllib.parse import unquote

#read domain string
domain = sys.argv[1]

#create name hash
file_time = time.time()
file_name = hashlib.md5(domain.encode("utf-8")).hexdigest() + "-" + str(file_time).split(".")[0] + ".txt"

#url
url = "http://web.archive.org/cdx/search/cdx?url={}/*&output=text&fl=original&collapse=urlkey"

res = requests.get(url.format(domain), stream=True)

with open(file_name, "a", encoding="utf-8") as file:
    file.write(unquote(res.text))