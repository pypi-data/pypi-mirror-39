import collections

from click import prompt


def silent_prompt(**kwargs):
    return prompt('', prompt_suffix='', **kwargs)

from random import choice, randint

#TODO: Allow this stuff as session? :D
MIN_NUM = 100
MAX_NUM = 999
adjs = [
    "autumn", "hidden", "bitter", "misty", "silent", "empty", "dry", "dark",
    "summer", "icy", "delicate", "quiet", "white", "cool", "spring", "winter",
    "patient", "twilight", "dawn", "crimson", "wispy", "weathered", "blue",
    "billowing", "broken", "cold", "damp", "falling", "frosty", "green", "long",
    "late", "lingering", "bold", "little", "morning", "muddy", "old", "red",
    "rough", "still", "small", "sparkling", "throbbing", "shy", "wandering",
    "withered", "wild", "black", "young", "holy", "solitary", "fragrant",
    "aged", "snowy", "proud", "floral", "restless", "divine", "polished",
    "ancient", "purple", "lively", "nameless"
]
nouns = [
    "waterfall", "river", "breeze", "moon", "rain", "wind", "sea", "morning",
    "snow", "lake", "sunset", "pine", "shadow", "leaf", "dawn", "glitter",
    "forest", "hill", "cloud", "meadow", "sun", "glade", "bird", "brook",
    "butterfly", "bush", "dew", "dust", "field", "fire", "flower", "firefly",
    "feather", "grass", "haze", "mountain", "night", "pond", "darkness",
    "snowflake", "silence", "sound", "sky", "shape", "surf", "thunder",
    "violet", "water", "wildflower", "wave", "water", "resonance", "sun",
    "wood", "dream", "cherry", "tree", "fog", "frost", "voice", "paper", "frog",
    "smoke", "star"
]

def random_job_name():
    return "-".join(
        [choice(adjs),
        choice(nouns),
        str(randint(MIN_NUM, MAX_NUM))])


def deep_update(d, u):
    """
    updates deeply nested dict in a recursive manner - like applying a patch
    """

    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
