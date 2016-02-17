import itertools
import json
import re
import sys
import time

import html2text
import requests
from pyquery import PyQuery as pq

# This code uses the Wiktionary REST API to retrieve definitions
# and transform them into a format more like that which is used by
# Wordnik.

# from https://gist.github.com/gregburek/1441055
def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)

    def decorate(func):
        lastTimeCalled = [0.0]

        def rateLimitedFunction(*args, **kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait > 0:
                time.sleep(leftToWait)
            ret = func(*args, **kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate


@RateLimited(5)  # 5 per second at most
def get_wiki_json(word):
    r = requests.get(
        "https://en.wiktionary.org/api/rest_v1/page/definition/" + word)
    if r.status_code is 200:
        return (r.json(), None)
    else:
        return (None, r.status_code)


def clean(txt):
    return re.sub(r"\[\d*\]", "", txt.replace("\n", "")).strip()


def xrefs(html):
    doc = pq(html)
    anchors = doc("a")
    return [anchor.text for anchor in anchors if '/wiki/' in anchor.attrib.get('href', '')]


def convert_one_def(pos, d):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_emphasis = True
    wd = {"src": "wiktionary"}
    definition = d.get("definition", "")
    wd["txt"] = clean(h.handle(definition))
    wd["pos"] = {"name": pos}
    xreffs = xrefs(definition)
    if len(xreffs) > 0:
        wd["xref"] = xreffs
    return wd


def wiki_def_to_defs(wiki_pos_def):
    pos = wiki_pos_def.get("partOfSpeech", "Unknown")
    return [convert_one_def(pos, d) for d in wiki_pos_def.get("definitions", [])]


def wiki_def_to_dfs(language, entry):
    defs = entry.get(language, [])
    list2d = [wiki_def_to_defs(d) for d in defs]
    return list(itertools.chain.from_iterable(list2d))


def wiki_entry_to_dict(word, entry, language="en"):
    d = {"word": word}
    d["df"] = wiki_def_to_dfs(language, entry)
    return d

for line in sys.stdin:
    word = line.strip()
    if len(word) > 0:
        entry, err = get_wiki_json(word)
        if err:
            sys.stderr.write("Couldn't get %s, reason: %s\n" % (word, err))
            sys.stderr.flush()
        else:
            print(json.dumps(wiki_entry_to_dict(word, entry)))
            sys.stdout.flush()
