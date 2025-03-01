import os
import json
import time
from remarkable.spremenljivke import path, kljucna_beseda, folder_out, metadata_file

def get_metadata(ime):
    metadata_path = ime + ".metadata"
    if os.path.exists(metadata_path) == False:
        return None
    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_content(ime):
    content_path = ime + ".content"
    if os.path.exists(content_path) == False:
        return None
    with open(content_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_visible_name_brez_klb(metadata):
    return metadata["visibleName"].replace(kljucna_beseda, "")

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
        family.reverse()
    return family

def get_write_to_path(metadata):
    family = get_family(metadata)
    write_to_path = os.path.join(folder_out, *family)
    os.makedirs(write_to_path, exist_ok=True)
    visible_name = get_visible_name_brez_klb(metadata)
    return os.path.join(write_to_path, visible_name + ".pdf")

def json_format(name, family, mod_time, pages):
    return {"name": name, "family": family, "last modified": mod_time, "convertet time": time.time(), "pages": pages}

def generate_metadata(metadata, pages, hash):
    # hash = metadata["hash"]
    name = get_visible_name_brez_klb(metadata)
    family = get_family(metadata)
    # pages = content["cPages"]["pages"] # list of dicts
    mod_time = int(metadata["lastModified"])/1000
    
    metdata_path = os.path.join(folder_out, metadata_file)
    if os.path.exists(metdata_path) == False:
        data = {hash: json_format(name, family, mod_time, pages)}
    else:
        with open(metdata_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data[hash] = json_format(name, family, mod_time, pages)
    with open(metdata_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)