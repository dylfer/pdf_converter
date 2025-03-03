import os
from fpdf import FPDF
import regex

ignoredFileExtensions = ['pdf', 'txt', 'jpg', 'png', 'bmp', 'mp3', 'mp4', 'wav', 'jpeg']
ignoredFileNames = ['converter.py', 'readme.md']
ignoredFolderExpression = regex.compile(r'^\..*')

def add_txt_extension(directory):
    for root, dirs, files in os.walk(directory):
        dirs[:] = [dir for dir in dirs if not ignoredFolderExpression.match(dir)]
        for filename in files:
            if filename in ignoredFileNames or any(filename.endswith(extension) for extension in ignoredFileExtensions):
                continue
            new_name = f"{filename}.txt"
            os.rename(os.path.join(root, filename), os.path.join(root, new_name))

def create_pdf_from_txt(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                directory = root
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                with open(os.path.join(directory, filename), 'r') as file:
                    for line in file:
                        pdf.cell(200, 10, txt=line, ln=True)
                pdf.output(os.path.join(directory, f"{os.path.splitext(filename)[0]}.pdf"))

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    add_txt_extension(directory)
    create_pdf_from_txt(directory)
