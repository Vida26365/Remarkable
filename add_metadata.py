import os
import time
import json
from spremenljivke import folder_out, metadata_file

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
    
        
def add_dict(dict_path, file_name, rest_family, mod_time):
    if rest_family == []:
        dict_path["files"][file_name] = {"last modified": mod_time, "convertet time": time.time()} # POZOR: različna formata za čas
        return
    folder_name = rest_family[0]
    
    if folder_name not in dict_path:
        dict_path["folders"][folder_name] = {"content": {"folders": {}, "files": {}}}
    # dict_path["folders"][folder_name]["time"] = time.time()
    return add_dict(dict_path["folders"][folder_name]["content"], file_name, rest_family[1:], mod_time)