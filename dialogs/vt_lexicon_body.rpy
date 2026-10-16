# Focused pullout lexicon: only slots required by 03_vt_pullout_coercion.rpy.
init python:
    vt_register_words("verb_climax", [
        {"when": {"register": ["demure", "shy"]}, "words": ["finish", "climax"]},
        {"when": {"register": "neutral"}, "words": ["finish", "orgasm"]},
        {"when": {"register": "direct"}, "words": ["cum", "orgasm"]},
        {"when": {"register": "explicit"}, "words": ["cum"]},
        {"when": {"register": "crude"}, "words": ["cum", "get off"]},
        {"when": {}, "words": ["finish"]},
    ])

    # Gerund form ("keep %verb_climax_ing% in me", "I love %verb_climax_ing% inside you").
    vt_register_words("verb_climax_ing", [
        {"when": {"register": ["demure", "shy"]}, "words": ["finishing", "climaxing"]},
        {"when": {"register": "neutral"}, "words": ["finishing", "orgasming"]},
        {"when": {"register": "direct"}, "words": ["cumming", "orgasming"]},
        {"when": {"register": "explicit"}, "words": ["cumming"]},
        {"when": {"register": "crude"}, "words": ["cumming", "getting off"]},
        {"when": {}, "words": ["finishing"]},
    ])

    # Past form ("I %verb_climax_ed%", "she %verb_climax_ed% before I did").
