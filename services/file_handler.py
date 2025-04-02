from config import UPLOAD_DIR, OUTPUT_DIR
import shutil
import os
from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

def save_file(file_obj):
    """Saves the provided file to a the specified path."""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    if file_obj is None:
        return "No file uploaded"
    
    file_path = file_obj.name
    
    # Define the destination path
    filename = os.path.basename(file_path)
    destination_path = os.path.join(UPLOAD_DIR, filename) 

    # Copy the file
    shutil.copy(file_path, destination_path)
    return f"File saved to: {destination_path}"

def output_file(file_obj, response_text) -> str:
    """Saves the provided file to a the specified path."""

    pdf = MarkdownPdf(toc_level=2)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if file_obj is None:
        return "No file uploaded"
    
    file_path = file_obj.name

    content = response_text.strip("'''")
    
    # Define the destination path
    filename = "updated_" + os.path.basename(file_path).split('.')[0]
    # filename = Path(file_path).stem
    destination_path = os.path.join(OUTPUT_DIR, filename + '.md')
    with open(destination_path, "w") as f:
        f.write(content)

    
    with open(destination_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    pdf.add_section(Section(markdown_content))
    final_output = os.path.join(OUTPUT_DIR, filename + '.pdf')
    pdf.save(final_output)

    

    # typst.compile(destination_path, output=OUTPUT_DIR + "/updated.pdf")


    return destination_path
    