import re

def name_to_slug(name):
    slug = re.sub(r"\s+", "+", name)
    slug = re.sub(r"[^\w+\-.]", "_", slug)
    return slug

