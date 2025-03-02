from spremenljivke import kljucna_beseda, old_path
from metadatanje import get_family
from zvezkanje import get_old_data


def find_kljucna_beseda(metadata, klb):
    name = metadata["visibleName"]
    family = get_family(metadata)
    if klb in name:
        return True
    for p in family:
        if klb in p.lower():
            return True
    return False   
    

def pogoj(metadata, content, hash):
    
    if content == None or metadata == None:
        return False
    if metadata["type"] != "DocumentType":
        return False
    
    mod_time = metadata["lastModified"]
    old_data = get_old_data(old_path)
    if hash in old_data:
        old_time = old_data[hash]["last modified"]
    else:
        old_time = 0
    
    return (
        "cPages" in content and
        old_time < int(mod_time)/1000 and
        find_kljucna_beseda(metadata, kljucna_beseda)
        )