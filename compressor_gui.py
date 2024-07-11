import os
import customtkinter as ctk
import zipfile
import tarfile
import gzip
import shutil
import py7zr
from cryptography.fernet import Fernet

def compress_zip(file_paths, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file_path in file_paths:
            archive.write(file_path, os.path.basename(file_path))

def compress_tar(file_paths, output_path):
    with tarfile.open(output_path, 'w') as archive:
        for file_path in file_paths:
            archive.add(file_path, arcname=os.path.basename(file_path))

def compress_gzip(file_paths, output_path):
    with tarfile.open(output_path, 'w:gz') as archive:
        for file_path in file_paths:
            archive.add(file_path, arcname=os.path.basename(file_path))

def compress_7z(file_paths, output_path, level=5, password=None):
    with py7zr.SevenZipFile(output_path, 'w', password=password) as archive:
        for file_path in file_paths:
            archive.write(file_path, os.path.basename(file_path))

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    with open(file_path, 'wb') as file:
        file.write(encrypted)

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted)

def start_compression(file_paths, compression_type, output_path, level, password):
    if compression_type == "ZIP":
        compress_zip(file_paths, output_path)
    elif compression_type == "TAR":
        compress_tar(file_paths, output_path)
    elif compression_type == "GZIP":
        compress_gzip(file_paths, output_path)
    elif compression_type == "7z":
        compress_7z(file_paths, output_path, level, password)
    else:
        raise ValueError("Unsupported compression type")

# إعداد واجهة المستخدم
def create_gui():
    root = ctk.CTk()
    root.title("MyCompressor")
    root.geometry("600x400")

    # إعداد مكونات الواجهة
    # ...

    root.mainloop()

if __name__ == "__main__":
    create_gui()
