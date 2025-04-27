import zipfile
import os
import io

def extract_zip(zip_file):
    extracted_files = {}
    with zipfile.ZipFile(zip_file) as z:
        for file_name in z.namelist():
            if file_name.endswith(('.py', '.js', '.ts', '.jsx', '.tsx' , '.txt')):
                with z.open(file_name) as f:
                    extracted_files[file_name] = f.read().decode("utf-8", errors="ignore")
    return extracted_files
def create_fixed_zip(fixed_files_dict):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for filename, content in fixed_files_dict.items():
            zip_file.writestr(filename, content)
    zip_buffer.seek(0)
    return zip_buffer