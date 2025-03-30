from config import UPLOAD_DIR, OUTPUT_DIR
import shutil
import os

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

def output_file(file_obj) -> str:
    """Saves the provided file to a the specified path."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OuTPUT_DIR)

    if file_obj is None:
        return "No file uploaded"
    
    file_path = file_obj.name
    
    # Define the destination path
    filename = "updated_" + os.path.basename(file_path)
    destination_path = os.path.join(OUTPUT_DIR, filename) 

    return destination_path
    