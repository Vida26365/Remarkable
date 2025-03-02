import os
from PyPDF2 import PdfWriter
from spremenljivke import path, folder_out, zacasna_mapa
from pogoji import pogoj
from zvezkanje import get_old_pdf, get_old_pages, ensure_folder_and_metadata_exists
from metadatanje import get_content, get_metadata, get_write_to_path, generate_metadata


def clear_temoporary_folder(zacasna_mapa):
    for file in os.listdir(zacasna_mapa):
        if file == "":
            continue
        file_path = os.path.join(zacasna_mapa, file)
        os.remove(file_path)
    return

def make_pdfs_to_join(ime, sorted_pages, old_pages, metadata):
    old_pages_hashes = [c["id"] for c in old_pages]
    old_pdf = get_old_pdf(metadata)
    if old_pdf  == None:
        pdfs_to_join = []
    else:
        pdfs_to_join = [old_pdf]
    for page in sorted_pages:
        if page["id"] in old_pages_hashes:
            continue
        file_path = os.path.join(ime, page["id"] + ".rm")
        dump_file = page["id"] + ".pdf"
        dump_path = os.path.join(zacasna_mapa, dump_file)
        os.makedirs(zacasna_mapa, exist_ok=True)
        os.system(f"rmc -t pdf -o {dump_path} {file_path}")
        pdfs_to_join.append(dump_path)
    return pdfs_to_join

def join_pdfs(pdfs_to_join, metadata):
    merger = PdfWriter()
    # Join pdfs
    for pdf in pdfs_to_join:
        try:
            merger.append(pdf)
        except:
            # merger.append(ups)
            print("Errror :(")

    write_to_file_path = get_write_to_path(metadata)
    
    merger.write(write_to_file_path)
    merger.close()
    
    clear_temoporary_folder(zacasna_mapa)
    
def pdfjanje():
    clear_temoporary_folder(zacasna_mapa)
    ensure_folder_and_metadata_exists(folder_out, "metadata.json")
    
    for (ime, _, _) in os.walk(path):
        content = get_content(ime)           
        metadata = get_metadata(ime)
        hash = os.path.basename(ime)
        
        if pogoj(metadata, content, hash) == False:
            continue
        
        pages = content["cPages"]["pages"] # list of dicts
        sorted_pages = sorted(pages, key=lambda x: x["idx"]["value"])
        old_pages = get_old_pages(hash)

        pdfs_to_join = make_pdfs_to_join(ime, sorted_pages, old_pages, metadata)

        if pdfs_to_join == []:
            continue
        
        join_pdfs(pdfs_to_join, metadata)
        
        generate_metadata(metadata, pages, hash)
        
    return


        



