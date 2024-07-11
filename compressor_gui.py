import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import py7zr
import zipfile
import tarfile
import gzip
import shutil

# Function to compress files
def compress_files(method, level, password, files):
    if method == "zip":
        with zipfile.ZipFile("output.zip", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=level) as zipf:
            for file in files:
                zipf.write(file, os.path.basename(file))
    elif method == "7z":
        with py7zr.SevenZipFile("output.7z", 'w', password=password) as archive:
            archive.writeall(files)
    elif method == "tar":
        with tarfile.open("output.tar.gz", "w:gz") as tar:
            for file in files:
                tar.add(file)
    elif method == "gzip":
        with gzip.open("output.gz", "wb") as gz:
            for file in files:
                with open(file, "rb") as f:
                    shutil.copyfileobj(f, gz)

# Function to extract files
def extract_files(file):
    if file.endswith(".zip"):
        with zipfile.ZipFile(file, "r") as zipf:
            zipf.extractall()
    elif file.endswith(".7z"):
        with py7zr.SevenZipFile(file, 'r') as archive:
            archive.extractall()
    elif file.endswith(".tar.gz"):
        with tarfile.open(file, "r:gz") as tar:
            tar.extractall()
    elif file.endswith(".gz"):
        with gzip.open(file, "rb") as gz:
            with open(file.replace(".gz", ""), "wb") as f:
                shutil.copyfileobj(gz, f)

# GUI Setup
class CompressorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Compressor GUI")
        self.geometry("400x300")

        self.method_label = ctk.CTkLabel(self, text="Compression Method:")
        self.method_label.pack(pady=10)
        
        self.method_option = ctk.CTkOptionMenu(self, values=["zip", "7z", "tar", "gzip"])
        self.method_option.pack(pady=10)

        self.level_label = ctk.CTkLabel(self, text="Compression Level:")
        self.level_label.pack(pady=10)
        
        self.level_slider = ctk.CTkSlider(self, from_=1, to_=22)
        self.level_slider.pack(pady=10)

        self.password_label = ctk.CTkLabel(self, text="Password (optional):")
        self.password_label.pack(pady=10)
        
        self.password_entry = ctk.CTkEntry(self)
        self.password_entry.pack(pady=10)

        self.select_button = ctk.CTkButton(self, text="Select Files", command=self.select_files)
        self.select_button.pack(pady=10)

        self.compress_button = ctk.CTkButton(self, text="Start Compression", command=self.start_compression)
        self.compress_button.pack(pady=10)

        self.extract_button = ctk.CTkButton(self, text="Extract Files", command=self.extract_files)
        self.extract_button.pack(pady=10)

        self.files = []

    def select_files(self):
        self.files = filedialog.askopenfilenames()
        messagebox.showinfo("Selected Files", "\n".join(self.files))

    def start_compression(self):
        method = self.method_option.get()
        level = int(self.level_slider.get())
        password = self.password_entry.get()
        compress_files(method, level, password, self.files)
        messagebox.showinfo("Compression Complete", "Files have been compressed successfully!")

    def extract_files(self):
        file = filedialog.askopenfilename()
        extract_files(file)
        messagebox.showinfo("Extraction Complete", "Files have been extracted successfully!")

if __name__ == "__main__":
    app = CompressorGUI()
    app.mainloop()
