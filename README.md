# wiktionary_to_wordnik.py
Converts Wiktionary JSON entries to ones more like Wordnik's 

Requires:

    import html2text
    import requests
    from pyquery import PyQuery as pq
    
`pyquery` is really only used for finding cross-references, which could be 
done with a regular expression easily enough.

