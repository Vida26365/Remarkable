import os
import time
import json
from remarkable.spremenljivke import folder_out, metadata_file, old_path
from remarkable.metadatanje import get_family, get_visible_name_brez_klb
        
def ensure_folder_and_metadata_exists(folder_out, metadata_file):
    if os.path.exists(folder_out) == False:
        os.makedirs(folder_out)
    metadata_path = os.path.join(folder_out, metadata_file)
    if os.path.exists(metadata_path) == False:
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump({}, f)
    return

def get_old_data(path):
    # json.decoder.JSONDecodeError
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            print("Corrupted metadata file")
            return {}

def get_old_pages(hash):
    old_data = get_old_data(old_path)
    if hash in old_data:
        return old_data[hash]["pages"]
    return []

def get_old_pdf(metadata):
    name = get_visible_name_brez_klb(metadata)
    family = get_family(metadata)
    path = os.path.join(folder_out, *family, name + ".pdf")
    if os.path.exists(path):
        return
    return

def get_path(name, family):
    return os.path.join(folder_out, *family, name + ".pdf")

def get_metadata_path():
    return os.path.join(folder_out, metadata_file)

def get_hash(name, family):
    data = get_old_data(get_metadata_path())
    for hash, value in data.items():
        if value["name"] == name and value["family"] == family:
            return hash
        
# def get_name_family_from_hash(hash, data):
#     return get_visible_name_brez_klb(data[hash]["name"]), data[hash]["family"]

def remove_pdf(name, family):
    hash = get_hash(name, family) # could be none
    path = get_path(name, family)
    metadata_path = os.path.join(folder_out, metadata_file)
    data = get_old_data(metadata_path)
    
    if hash != None:
        data.pop(hash)
    if os.path.exists(path):
        os.remove(path)
        
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    