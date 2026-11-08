# Lexicon dependencies for both booths. Existing full local pools take precedence.
init python:
    if "adj_desperate" not in VT_LEXICON:
        vt_register_words("adj_desperate", [
            {"when": {"register": ["demure", "shy"]}, "words": ["needy", "eager"]},
            {"when": {"register": "neutral"}, "words": ["worked up", "eager"]},
            {"when": {"register": "direct"}, "words": ["turned on", "desperate"]},
            {"when": {"register": "explicit"}, "words": ["desperate", "needy for it"]},
            {"when": {"register": "crude"}, "words": ["fucking desperate", "starving for it"]},
            {"when": {}, "words": ["eager"]},
        ])
    if "adj_praise" not in VT_LEXICON:
        vt_register_words("adj_praise", [
            {"when": {"register": ["demure", "shy"]}, "words": ["lovely", "beautiful"]},
            {"when": {"register": "neutral"}, "words": ["beautiful", "gorgeous"]},
            {"when": {"register": "direct"}, "words": ["gorgeous", "sexy"]},
            {"when": {"register": "explicit"}, "words": ["sexy as hell", "irresistible"]},
            {"when": {"register": "crude"}, "words": ["so fucking hot", "unbelievably sexy"]},
            {"when": {}, "words": ["beautiful"]},
        ])
    if "noun_ass" not in VT_LEXICON:
        vt_register_words("noun_ass", [
            {"when": {"register": ["demure", "shy"]}, "words": ["backside", "rear"]},
            {"when": {"register": "neutral"}, "words": ["ass", "behind"]},
            {"when": {"register": "direct"}, "words": ["ass"]},
            {"when": {"register": "explicit"}, "words": ["ass"]},
            {"when": {"register": "crude", "corruption": {"lt": 80}}, "words": ["ass"]},
            {"when": {"register": "crude", "corruption": {"ge": 80}}, "words": ["asshole", "back door"]},
            {"when": {}, "words": ["ass"]},
        ])
    if "noun_breasts" not in VT_LEXICON:
        vt_register_words("noun_breasts", [
            {"when": {"register": ["demure", "shy"], "intellect": {"lt": 35}}, "words": ["chest", "top area"]},
            {"when": {"register": ["demure", "shy"], "intellect": {"ge": 35}}, "words": ["breasts"]},
            {"when": {"register": "neutral"}, "words": ["breasts", "chest"]},
            {"when": {"register": "direct"}, "words": ["tits"]},
            {"when": {"register": "explicit"}, "words": ["tits", "breasts"]},
            {"when": {"register": "crude", "corruption": {"lt": 80}}, "words": ["tits"]},
            {"when": {"register": "crude", "corruption": {"ge": 80}}, "words": ["titties", "knockers"]},
            {"when": {}, "words": ["breasts"]},
        ])
    if "noun_mouth" not in VT_LEXICON:
        vt_register_words("noun_mouth", [
            {"when": {"register": ["demure", "shy"]}, "words": ["lips", "mouth"]},
            {"when": {"register": "neutral"}, "words": ["mouth"]},
            {"when": {"register": "direct"}, "words": ["mouth"]},
            {"when": {"register": "explicit"}, "words": ["mouth", "throat"]},
            {"when": {"register": "crude", "corruption": {"lt": 80}}, "words": ["mouth"]},
            {"when": {"register": "crude", "corruption": {"ge": 80}}, "words": ["throat"]},
            {"when": {}, "words": ["mouth"]},
        ])
    if "noun_penis" not in VT_LEXICON:
        vt_register_words("noun_penis", [
            {"when": {"register": ["demure", "shy"], "intellect": {"lt": 35}}, "words": ["thing", "part"]},
            {"when": {"register": ["demure", "shy"], "intellect": {"ge": 35}}, "words": ["penis"]},
            {"when": {"register": "neutral"}, "words": ["penis", "cock"]},
            {"when": {"register": "direct"}, "words": ["dick", "cock"]},
            {"when": {"register": "explicit"}, "words": ["cock", "big cock"]},
            {"when": {"register": "crude", "corruption": {"lt": 80}}, "words": ["cock", "dick"]},
            {"when": {"register": "crude", "corruption": {"ge": 80}}, "words": ["huge cock", "big fat cock", "monster cock"]},
            {"when": {}, "words": ["penis"]},
        ])
    if "noun_pussy" not in VT_LEXICON:
        vt_register_words("noun_pussy", [
            {"when": {"register": ["demure", "shy"], "intellect": {"lt": 35}}, "words": ["down there", "private area"]},
            {"when": {"register": ["demure", "shy"], "intellect": {"ge": 35}}, "words": ["vagina"]},
            {"when": {"register": "neutral"}, "words": ["pussy", "vagina"]},
            {"when": {"register": "direct"}, "words": ["pussy"]},
            {"when": {"register": "explicit"}, "words": ["pussy", "wet pussy"]},
            {"when": {"register": "crude", "corruption": {"lt": 80}}, "words": ["pussy", "cunt"]},
            {"when": {"register": "crude", "corruption": {"ge": 80}}, "words": ["cunt", "soaked cunt", "hungry little cunt"]},
            {"when": {}, "words": ["vagina"]},
        ])
    if "verb_climax_ed" not in VT_LEXICON:
        vt_register_words("verb_climax_ed", [
            {"when": {"register": ["demure", "shy"]}, "words": ["finished", "climaxed"]},
            {"when": {"register": "neutral"}, "words": ["finished", "orgasmed"]},
            {"when": {"register": "direct"}, "words": ["came", "orgasmed"]},
            {"when": {"register": "explicit"}, "words": ["came"]},
            {"when": {"register": "crude"}, "words": ["came", "got off"]},
            {"when": {}, "words": ["finished"]},
        ])
    if "verb_command" not in VT_LEXICON:
        vt_register_words("verb_command", [
            {"when": {"register": ["demure", "shy"]}, "words": ["come sit closer to me", "come here and let me hold you"]},
            {"when": {"register": "neutral"}, "words": ["come sit next to me", "come closer to me"]},
            {"when": {"register": "direct"}, "words": ["get over here", "come here, now"]},
            {"when": {"register": "explicit"}, "words": ["get on your knees for me", "come here and get on your knees"]},
            {"when": {"register": "crude"}, "words": ["get on your knees and beg for it", "crawl over here and beg for it"]},
            {"when": {}, "words": ["come here"]},
        ])
    if "verb_desire" not in VT_LEXICON:
        vt_register_words("verb_desire", [
            {"when": {"register": ["demure", "shy"]}, "words": ["want", "long for"]},
            {"when": {"register": "neutral"}, "words": ["want", "need"]},
            {"when": {"register": "direct"}, "words": ["need", "want"]},
            {"when": {"register": "explicit"}, "words": ["crave", "need"]},
            {"when": {"register": "crude"}, "words": ["fucking need", "crave"]},
            {"when": {}, "words": ["want"]},
        ])
    if "verb_have_sex" not in VT_LEXICON:
        vt_register_words("verb_have_sex", [
            {"when": {"register": ["demure", "shy"]}, "words": ["be intimate", "be together"]},
            {"when": {"register": "neutral"}, "words": ["have sex", "sleep together"]},
            {"when": {"register": "direct"}, "words": ["have sex", "fuck"]},
            {"when": {"register": "explicit"}, "words": ["fuck"]},
            {"when": {"register": "crude"}, "words": ["fuck", "screw"]},
            {"when": {}, "words": ["have sex"]},
        ])
