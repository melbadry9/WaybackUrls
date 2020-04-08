#!/usr/bin/env python3
import os 
import sys
import requests
import threading
from urllib.parse import unquote

threads = 5
download_lock = threading.Semaphore(threads)

def usage():
    print("[i] Usage: ./way_urls.py domain.com")
    print("[i] Usage: cat file.txt | ./way_urls.py")

def create_dir():
    try:
        os.mkdir("way_urls")
    except FileExistsError:
        pass

def get_data(domain):
    with download_lock:
        print_domain(domain)
        file_name = "way_urls/" + domain.replace("*.","") #+ ".txt"
        url = "http://web.archive.org/cdx/search/cdx?url={}&output=text&fl=original&collapse=urlkey"
        try:
            res = requests.get(url.format(domain), stream=True, timeout=60)
            with open(file_name, "a", encoding="utf-8") as file:
                file.write(unquote(res.text))
        except requests.exceptions.ConnectionError:
            print_error(domain)

def print_domain(domain):
    sys.stdout.write('\033[1K')
    sys.stdout.write('\033[0G')
    sys.stdout.write("[+] Getting urls for: {0}".format(domain))
    sys.stdout.flush()

def print_error(domain):
    sys.stdout.write('\033[1K')
    sys.stdout.write('\033[0G')
    sys.stdout.write("[x] Error getting urls for: {0}".format(domain))
    sys.stdout.flush()

def main():
    # Create ways_urls directory if not exist
    create_dir()

    # Reading input 
    try:
        domain = [sys.argv[1]]
    except IndexError:
        domain = sys.stdin
        if domain.isatty():
            usage()
            print("[x] Domain is missing")
            exit()

    # Start threads
    for dom in domain:
        dom = dom.rstrip("\n")
        th = threading.Thread(target=get_data, args=(dom,))
        th.start()
    
    # Print new line after finshing
    th.join()
    print("")
    
if __name__ == "__main__":
    main()
