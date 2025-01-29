import json
import os
import rmc.cli
from pathlib import Path
# from pypdf import PdfMerger

path = r"C:\Users\vidam\AppData\Roaming\remarkable\desktop"
folder = "32bc463c-da4a-43d2-8017-77c65f8bea61"
folder_path = os.path.join(path, folder)

rm_files = os.listdir(folder_path)

def content_path (path, name):
    return os.path.join(path, name) + ".content"
def metadata_path (path, name):
    return os.path.join(path, name) + ".metadata"

def get_metadata(path, name):
    with open(metadata_path(path, name), "r") as file:
        return json.load(file)
def get_content(path, name):
    with open(content_path(path, name), "r") as file:
        return json.load(file)

metadata = get_metadata(path, folder)
print(metadata["visibleName"], get_metadata(path, metadata["parent"])["visibleName"])


# rmc.convert_rm(file, "pdf", metadata["visibleName"] + ".pdf")


def get_rm_file_path(path, folder, name):
    return os.path.join(path, folder, name)

rmc.cli.convert_rm(get_rm_file_path(path, folder, rm_files[0]), "pdf", metadata["visibleName"] + ".pdf")

# pdfs = list(map(lambda x: rmc.cli.convert_rm(, "pdf", "page"), rm_files))
# print(type(pdf))

# from PyPDF2 import PdfWriter

# merger = PdfWriter()

# for pdf in pdfs:
#     merger.append(pdf)

# merger.write("merged-pdf.pdf")
# merger.close()
# from PyPDF2 import PdfReader, PdfWriter

# def pdf_cat(input_files, output_stream):
#     input_streams = []
#     try:
#         # First open all the files, then produce the output file, and
#         # finally close the input files. This is necessary because
#         # the data isn't read from the input files until the write
#         # operation. Thanks to
#         # https://stackoverflow.com/questions/6773631/problem-with-closing-python-pypdf-writing-getting-a-valueerror-i-o-operation/6773733#6773733
#         for input_file in input_files:
#             input_streams.append(open(input_file, 'rb'))
#         writer = PdfWriter()
#         for reader in map(PdfReader, input_streams):
#             for n in range(len(reader.pages)):
#                 writer.add_page(reader.pages[n])
#         writer.write(output_stream)
#     finally:
#         for f in input_streams:
#             f.close()
#         output_stream.close()
        
# pdf_cat(pdfs, open(metadata["visibleName"] + ".pdf", "wb"))

# if __name__ == '__main__':
#     if sys.platform == "win32":
#         import os, msvcrt
#         msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
#     pdf_cat(sys.argv[1:], sys.stdout)



# result = fitz.open()

# for pdf in pdfs:
#     with fitz.open(pdf) as mfile:
#         result.insert_pdf(mfile)
    
# result.save(metadata["visibleName"] + ".pdf")

# merger = PdfMerger()

# for pdf in pdfs:
#     merger.append(pdf)

# merger.write(metadata["visibleName"] + ".pdf")
# merger.close()



