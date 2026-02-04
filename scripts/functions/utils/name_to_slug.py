import re 

def name_to_slug(name): 
    return re.sub(r"\s+", "+", name) 

