"""
This file holds a censor function for when any profane words in a Command
are being sent in a SFW channel.
"""

def censor(text, inCodeBlock = False):
    """Returns a censored version of a string given.

    Parameters:
        text: The text to censor.
        inCodeBlock: Whether or not the text is going into a code block. (Defaults to False)
    
    Returns:
        censoredText (str)
    """

    # The list of profane words
    profaneWords = [
        "asshole", "a$shole", "as$hole", "assh0le", "asshol3", "a$$hole", "a$sh0le", "a$shol3", "as$h0le", "as$hol3", "assh0l3", "a$$h0le", "a$$hol3", "a$sh0l3", "as$h0l3", "a$$h0l3",
        "bastard", "b4stard", "ba5tard", "bast4rd", "b45tard", "b4st4rd", "ba4t4rd", "b45t4rd",
        "bitch", "b1tch",
        "cock", "c0ck", "dick",  "d1ck",
        "cunt", 
        "pussy", "pu5sy", "pus5y", "pu55y",
        "fuck", "fvck",
        "shit", "5hit", "sh1t", "5h1t",
        "chode", "ch0de", "chod3", "ch0d3", "choad", "ch0ad", "cho4d", "ch04d",
        "wanker", "w4nker", "wank3r", "w4nk3r",
        "twat", "tw4t",
        "nigger", "n1gger", "nigg3r", "n1gg3r", "nigga", "n1gga", "nigg4", "n1gg4",
        "tits", "t1ts", "tit5", "t1t5", "tit", "t1t",
        "jizz", "j1zz",
        "dildo", "d1ldo", "di1do", "dild0", "d11do", "d1ld0", "di1d0", "d11d0",
        "douche", "d0uche", "dovche", "douch3", "d0vche", "d0uch3", "dovch3", "d0vch3"
    ]

    profanityUsed = [
        profanity
        for profanity in profaneWords
        if profanity.lower() in text.lower()
    ]

    # Replace text; Keep first and last letters; All middle letters replace with an asterisk (*)
    for profanity in profanityUsed:
        censored = (
            "{}{}{}".format(
                profanity[0],
                "{}".format(
                    "*" if inCodeBlock else "\\*"
                ) * (len(profanity) - 2),
                profanity[len(profanity) - 1]
            )
        )
        text = text.replace(profanity, censored)
    
    return text