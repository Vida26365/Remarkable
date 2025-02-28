import os
import json
from spremenljivke import path, kljucna_beseda, old_path
import time

def get_old_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def remove_klb(name, klb):
    name.replace(klb, "")
    return name
    # return re.sub(klb, "", name)

def get_visible_name_brez_klb(metadata):
    name = metadata["visibleName"]
    name.replace(kljucna_beseda, "")
    return name

def find_kljucna_beseda(name, family, klb):
    if klb in name:
        name = remove_klb(name, klb)
        return True
    for p in family:
        if klb in p.lower():
            p = remove_klb(p, klb)
            return True
    return False

def get_family(metadata):
    parent = metadata["parent"]
    p_name = metadata["visibleName"]
    family = [] # vrstni red je pomemben
    while parent != "":
        p_path = os.path.join(path, parent + ".metadata")
        if os.path.exists(p_path) == False:
            break
        with open(p_path, "r", encoding="utf-8") as f:
            p_metadata = json.load(f)
        parent = p_metadata["parent"]
        p_name = p_metadata["visibleName"]
        family.append(p_name)
    return family

def pogoj(metadata, hash):    
    visible_name = metadata["visibleName"]
    family = get_family(metadata)
    mod_time = metadata["lastModified"]
    old_data = get_old_data(old_path)
    if hash in old_data:
        old_time = old_data[hash]["last modified"]
    else:
        old_time = 0
    
    return (
        old_time < int(mod_time)/1000 and
        find_kljucna_beseda(visible_name, family, kljucna_beseda)
        )