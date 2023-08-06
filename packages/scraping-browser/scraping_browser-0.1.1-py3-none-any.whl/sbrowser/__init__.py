#!/usr/bin/env python3

from time import sleep, perf_counter
from random import choice
from urllib.parse import urlsplit

import requests

IDLETIME = 4

DESKTOP_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko"
    ") Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Geck"
    "o) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHT"
    "ML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Geck"
    "o) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML"
    ", like Gecko) Chrome/54.0.2840.98 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML"
    ", like Gecko) Chrome/54.0.2840.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko"
    ") Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like "
    "Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
]


SITES = {}
COOKIES = {}
lasturl = "about:blank"


def goto(site, payload=None, method="GET"):
    print("[Browser] Going to site " + site)

    # finding out the hostname
    hostname = urlsplit(site).hostname.lower()
    tld = hostname[hostname.rfind("."):]
    hostname = hostname[: hostname.rfind(".")]
    if "." in hostname:
        hostname = hostname[hostname.rfind(".") + 1:]
    hostname = hostname + tld

    curr_time = perf_counter()
    if hostname in SITES.keys():
        last_time = SITES[hostname]
        if curr_time - last_time < IDLETIME:
            sleptime = IDLETIME - (curr_time - last_time)
            print(
                "[Browser] Request to frequent, sleeping {0:.1f} seconds "
                "before going there.".format(sleptime)
            )
            sleep(sleptime)
    SITES[hostname] = perf_counter()

    headers = {
        "User-Agent": choice(DESKTOP_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/webp,*/*;q=0.8",
    }

    cookie = {}
    if hostname in COOKIES.keys():
        cookie = COOKIES[hostname]

    try:
        if method == "GET":
            req = requests.get(
                site,
                headers=headers,
                data=payload,
                cookies=cookie,
                timeout=(6.05, 60),
            )
        elif method == "POST":
            req = requests.post(
                site,
                headers=headers,
                data=payload,
                cookies=cookie,
                timeout=(6.05, 60),
            )
        elif method == "PUT":
            req = requests.post(
                site,
                headers=headers,
                data=payload,
                cookies=cookie,
                timeout=(6.05, 60),
            )
        else:
            raise AttributeError('No such method"{}"'.format(method))
        global lasturl
        lasturl = req.url
        cookie = req.cookies
        if cookie:
            COOKIES[hostname] = cookie
        SITES[hostname] = perf_counter()
        return req.content
    except Exception:
        print("Some error with the browser.")
        raise
