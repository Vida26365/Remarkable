import os
import time
import json
from spremenljivke import folder_out, metadata_file

def parse_folder(path, slovar = None):
    if slovar == None:
        slovar = {"files": {}, "folders": {}}
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            slovar["folders"][file] = {}
            slovar["folders"][file]["content"] = (parse_folder(file_path))
            slovar["folders"][file]["time"] = time.time()
        else:
            slovar["files"][file] = {}
            slovar["files"][file]["time"] = time.time()
    return slovar

def add_metadata():
    metadata = parse_folder(folder_out)
    metadata_path = os.path.join(folder_out, metadata_file)
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
        