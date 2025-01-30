import os
import json
from PyPDF2 import PdfWriter



path = r"C:\Users\vidam\AppData\Roaming\remarkable\desktop"
for (ime, dir, files) in os.walk(path):
    if ime == "":
        continue
    metadata_path = os.path.join(path, ime + ".metadata")
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    visible_name = metadata["visibleName"]
    parent = metadata["parent"]
    
    family = [] # vrstni red je pomemben
    while parent != "":
        p_path = os.path.join(path, parent + ".metadata")
        with open(p_path, "r") as f:
            p_metadata = json.load(f)
        p = p_metadata["parent"]
        family.append(p)
    
    pdfs_to_join = []
    if any(["upl" in c for c in family]):
        for file in files:
            dump_path = os.join(path, ime, file + "pdf")
            os.system(f"rmc -t pdf -o {dump_path} {file}")
            pdfs_to_join.append(dump_path)
            
    else:
        for file in files:
            if "upl" in visible_name:
                dump_path = os.join(path, ime, file + "pdf")
                os.system(f"rmc -t pdf -o {dump_path} {file}")
                pdfs_to_join.append(dump_path)


    merger = PdfWriter()

    for pdf in pdfs_to_join:
        merger.append(pdf)

    merger.write(visible_name)
    merger.close()
    