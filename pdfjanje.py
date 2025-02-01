import os
import json
from PyPDF2 import PdfWriter
import re
from spremenljivke import path, kljucna_beseda, folder_out, zacasna_mapa

def remove_klb(name, klb):
    return re.sub(klb, "", name)

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
        
def find_klb(name, family, klb):
    if klb in name:
        name = remove_klb(name, klb)
        return True
    for p in family:
        if klb in p:
            p = remove_klb(p, klb)
            return True
    return False

def make_pdfs_to_join(ime, sorted_pages):
    pdfs_to_join = []
    for page in sorted_pages:
        file_path = os.path.join(ime, page["id"] + ".rm")
        dump_file = page["id"] + ".pdf"
        dump_path = os.path.join(zacasna_mapa, dump_file)
        os.makedirs(zacasna_mapa, exist_ok=True)
        os.system(f"rmc -t pdf -o {dump_path} {file_path}")
        pdfs_to_join.append(dump_path)
    return pdfs_to_join

def join_pdfs(pdfs_to_join, visible_name, family):
    merger = PdfWriter()

    for pdf in pdfs_to_join:
        merger.append(pdf)

    # family.append(visible_name + ".pdf")
    family.reverse()
    write_to_path = os.path.join(folder_out, *family)
    if write_to_path == "":
        write_to_path = "no_folder"
        
    print(family)
    print(visible_name)
    print("____________________________________")
    os.makedirs(write_to_path, exist_ok=True)
    write_to = os.path.join(write_to_path, visible_name + ".pdf")
    merger.write(write_to)
    merger.close()
    
    for file in os.listdir(zacasna_mapa):
        if file == "":
            continue
        file_path = os.path.join(zacasna_mapa, file)
        os.remove(file_path)
    # add metadata here

def pdfjanje():
    # TODO break down into smaller functions
    for (ime, _, _) in os.walk(path):
        content = get_content(ime)           
        metadata = get_metadata(ime)
        
        if content == None or metadata == None:
            continue
        if metadata["type"] != "DocumentType":
            continue
        
        
        
        visible_name = metadata["visibleName"]
        family = get_family(metadata)
        
        find_klb = find_klb(visible_name, family, kljucna_beseda)
        if find_klb == False:
            continue
        
        pages = content["cPages"]["pages"] # list of dicts
        sorted_pages = sorted(pages, key=lambda x: x["idx"]["value"])

        pdfs_to_join = make_pdfs_to_join(ime, sorted_pages)

        if pdfs_to_join == []:
            continue
        
        join_pdfs(pdfs_to_join, visible_name, family)
        # Add metadata here
        
    return


