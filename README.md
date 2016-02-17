# wiktionary_to_wordnik.py
Converts Wiktionary JSON entries to ones more like Wordnik's 

Requires:

    import html2text
    import requests
    from pyquery import PyQuery as pq
    
`pyquery` is really only used for finding cross-references, which could be 
done with a regular expression easily enough.

Assuming you have all the requirements:

    cat words.txt | python3 wiktionary_to_wordnik.py > definitions.jsonl 2> definitions.errors
    
`definitions.jsonl` will contain a definition, in JSON format, one per line
`definitions.errors` will contain words that could not be retrieved

Here is an example new definition:

    {
      "word": "ablator",
      "df": [
        {
          "src": "wiktionary",
          "txt": "A material that ablates, vaporizes, wears away, burns off, erodes, or abrades.",
          "pos": {
            "name": "Noun"
          },
          "xref": [
            "ablates",
            "vaporizes"
          ]
        }
      ]
    }
