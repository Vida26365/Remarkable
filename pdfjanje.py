import os
import json
from PyPDF2 import PdfWriter
# import re
# import time
from spremenljivke import path, kljucna_beseda, folder_out, zacasna_mapa, ups
from add_metadata import generate_metadata
from pogoji import pogoj, get_family, get_visible_name_brez_klb

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
        try:
            merger.append(pdf)
        except:
            merger.append(ups)
            print("Errror :(")

    # family.append(visible_name + ".pdf")
    family.reverse()
    write_to_path = os.path.join(folder_out, *family)
    if write_to_path == "":
        write_to_path = "no_folder"
        
    print(family)
    print(visible_name)
    print("____________________________________")
    os.makedirs(write_to_path, exist_ok=True)
    # write_to = write_to_path 
    write_to = os.path.join(write_to_path, visible_name + ".pdf")
    merger.write(write_to)
    merger.close()
    
    for file in os.listdir(zacasna_mapa):
        if file == "":
            continue
        file_path = os.path.join(zacasna_mapa, file)
        os.remove(file_path)
    # add metadata here
    
def clear_temoporary_folder():
    for file in os.listdir(zacasna_mapa):
        if file == "":
            continue
        file_path = os.path.join(zacasna_mapa, file)
        os.remove(file_path)
    return

def pdfjanje():
    clear_temoporary_folder()
    
    for (ime, _, _) in os.walk(path):
        print("____________________________________")
        print(ime)
        content = get_content(ime)           
        metadata = get_metadata(ime)
        hash = os.path.basename(ime)
        
        if content == None or metadata == None:
            continue
        if metadata["type"] != "DocumentType":
            continue
        
        # visible_name = metadata["visibleName"]
        visible_name = get_visible_name_brez_klb(metadata)
        family = get_family(metadata)
        mod_time = metadata["lastModified"]
        
        # find_klb = find_kljucna_beseda(visible_name, family, kljucna_beseda)
        if pogoj(metadata, hash) == False:
            continue
        
        if "cPages" not in content:
            continue
        pages = content["cPages"]["pages"] # list of dicts
        sorted_pages = sorted(pages, key=lambda x: x["idx"]["value"])

        pdfs_to_join = make_pdfs_to_join(ime, sorted_pages)
        # pdfs_to_join = []
        # for file in os.listdir(zacasna_mapa):
        #     if file == "":
        #         continue
        #     file_path = os.path.join(zacasna_mapa, file)
        #     pdfs_to_join.append(file_path)

        if pdfs_to_join == []:
            continue
        
        join_pdfs(pdfs_to_join, visible_name, family)
        
        generate_metadata(hash, visible_name, family, mod_time)
        # add_metadata(family, visible_name, mod_time)
        # Add metadata here
        
    return


        



