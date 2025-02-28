import os
import time
import json
from spremenljivke import folder_out, metadata_file

def generate_metadata(hash, name, family, mod_time):
    mod_time = int(mod_time)/1000
    metdata_path = os.path.join(folder_out, metadata_file)
    if os.path.exists(metdata_path) == False:
        data = {hash: {"name": name, "family": family, "last modified": mod_time, "convertet time": time.time()}}
    else:
        with open(metdata_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data[hash] = {"name": name, "family": family, "last modified": mod_time, "convertet time": time.time()}
    with open(metdata_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_metadata(family, name, mod_time):
    metadata_path = os.path.join(folder_out, metadata_file)
    if os.path.exists(metadata_path) == False:
        data = {"files": {}, "folders": {}}
    else:
        with open(metadata_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    add_dict(data, name, family, int(mod_time)/1000)

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
        
def add_dict(dict_path, name, rest_family, mod_time):
    file_name = name
    if rest_family == []:
        if "files" in dict_path:
            slovar = dict_path["files"]
            slovar[file_name] = {"last modified": mod_time, "convertet time": time.time()}
            dict_path["files"] = slovar
            return
        dict_path["files"][file_name] = {"last modified": mod_time, "convertet time": time.time()}
        return
    folder_name = rest_family[0]
    
    if folder_name not in dict_path:
        dict_path["folders"][folder_name] = {"folders": {}, "files": {}}
    # dict_path["folders"][folder_name]["time"] = time.time()
    return add_dict(dict_path["folders"][folder_name], file_name, rest_family[1:], mod_time)