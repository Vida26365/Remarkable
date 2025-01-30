import os
import json
from PyPDF2 import PdfWriter
import re


kljucna_beseda = "formule"

zacasna_mapa = "zacansa_mapa"


path = r"C:\Users\vidam\AppData\Roaming\remarkable\desktop"
for (ime, dir, files) in os.walk(path):
    # print(files)
    # print("_______________________________")
    # print(ime)
    metadata_path = ime + ".metadata"
    # print(metadata_path)
    # if re.match(r"{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}", ime) == False:
    #     continue
        
    if os.path.exists(metadata_path) == False:
        continue
    # print(metadata_path)
    # os.path.join(path, ime + ".metadata")
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    visible_name = metadata["visibleName"]
    parent = metadata["parent"]
    p_name = metadata["visibleName"]
    
    if metadata["type"] != "DocumentType":
        continue
    
    family = [] # vrstni red je pomemben
    i = 0 
    while parent != "" or i>10:
        family.append(p_name)
        # print(parent)
        p_path = os.path.join(path, parent + ".metadata")
        if os.path.exists(p_path) == False:
            break
        with open(p_path, "r", encoding="utf-8") as f:
            p_metadata = json.load(f)
        parent = p_metadata["parent"]
        p_name = p_metadata["visibleName"]
        i += 1
    
    pdfs_to_join = []
    if any([kljucna_beseda in c for c in family]):
        pass
        # TODO
        # for file in files:
        #     if ".rm" not in file:
        #         continue
        #     # dump_path = os.join(path, ime, file + "pdf")
        #     # print(file)
        #     dump_path = os.path.join(ime, file + "pdf")
        #     os.system(f"rmc -t pdf -o {dump_path} {file}")
        #     pdfs_to_join.append(dump_path)
            
    else:
        for file in files:
            if kljucna_beseda in visible_name.lower():
                if not file.endswith(".rm"):
                    continue
                file_path = os.path.join(ime, file)
                dump_file = file.removesuffix(".rm") + ".pdf"
                dump_path = os.path.join(zacasna_mapa, dump_file)
                os.makedirs(zacasna_mapa, exist_ok=True)
                os.system(f"rmc -t pdf -o {dump_path} {file_path}")
                pdfs_to_join.append(dump_path)


    if pdfs_to_join == []:
        continue
    
    merger = PdfWriter()

    for pdf in pdfs_to_join:
        merger.append(pdf)

    # family.append(visible_name + ".pdf")
    write_to_path = os.path.join(*family)
    if write_to_path == "":
        write_to_path = "no_folder"
    # else:
    #     write_to_path = os.path.join(*family)
    print(family)
    print("____________________________________")
    print(write_to_path)
    os.makedirs(write_to_path, exist_ok=True)
    write_to = os.path.join(write_to_path, visible_name + ".pdf")
    merger.write(write_to)
    merger.close()
    
    for file in os.listdir(zacasna_mapa):
        if file == "":
            continue
        file_path = os.path.join(zacasna_mapa, file)
        os.remove(file_path)
    