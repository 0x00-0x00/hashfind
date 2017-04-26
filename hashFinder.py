#!/usr/bin/env python3.6
import re
import requests
import argparse
import sys


def match_content(content):
    if type(content) is bytes:
        content = content.decode()
    regex = "Decrypted text for <b>(?P<hash>[a-fA-F0-9]+)<\/b>\s+is\s+<b>(?P<data>[a-zA-Z0-9]+)<\/b>"
    m = re.findall(regex, content)
    if not m:
        return None
    return m[0]


def do_request(url):
    req = requests.get(url)
    if req.status_code != 200:
        return None
    else:
        return req.content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--hash", help="Hash to find for", required=True)
    args = parser.parse_args()

    base_url = "https://hashdecryption.com/h/gost/"
    if not base_url.endswith("/"):
        base_url = base_url + "/"
    base_url += args.hash
    content = do_request(base_url)
    return_val = match_content(content)
    if not return_val:
        print("Hash \033[092m{0}\033[0m is not found.".format(args.hash))
        sys.exit(1)

    hash_val, plain = return_val[0], return_val[1]
    print("Hash \033[092m{0}\033[0m is derived from \033[092m{1}\033[0m".format(hash_val, plain))
    return 0

if __name__ == "__main__":
    main()

