import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

# Supported file types
FILE_TYPES = [("PDF files", "*.pdf"), ("JPEG files", "*.jpg"), ("PNG files", "*.png")]

# Document types
DOC_TYPES = ["Admission Form", "Fee Receipt", "Exam Result"]

class DocumentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Preston Higher Secondary School - Document Manager")
        self.root.geometry("500x400")
        
        # File path variable
        self.selected_file = None

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Browse button
        self.browse_btn = tk.Button(self.root, text="Browse Document", command=self.browse_file)
        self.browse_btn.pack(pady=10)

        # File label
        self.file_label = tk.Label(self.root, text="No file selected")
        self.file_label.pack()

        # Document name entry
        tk.Label(self.root, text="Document Name:").pack(pady=(20, 0))
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.pack()

        # Document type dropdown
        tk.Label(self.root, text="Document Type:").pack(pady=(10, 0))
        self.type_var = tk.StringVar(value=DOC_TYPES[0])
        self.type_menu = tk.OptionMenu(self.root, self.type_var, *DOC_TYPES)
        self.type_menu.pack()

        # Save button
        self.save_btn = tk.Button(self.root, text="Save Document", command=self.save_document)
        self.save_btn.pack(pady=20)

        # Status label
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=FILE_TYPES)
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
        else:
            self.selected_file = None
            self.file_label.config(text="No file selected")

    def save_document(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a document file.")
            return

        doc_name = self.name_entry.get().strip()
        if not doc_name:
            messagebox.showerror("Error", "Please enter a document name.")
            return

        doc_type = self.type_var.get()
        # Ask user for destination folder
        dest_folder = filedialog.askdirectory(title="Select Destination Folder")
        if not dest_folder:
            return

        # Get file extension
        _, ext = os.path.splitext(self.selected_file)
        # Build new filename
        new_filename = f"{doc_name}_{doc_type.replace(' ', '_')}{ext}"
        dest_path = os.path.join(dest_folder, new_filename)

        try:
            shutil.copy2(self.selected_file, dest_path)
            self.status_label.config(text=f"Document saved as {new_filename}", fg="green")
            messagebox.showinfo("Success", f"Document saved successfully:\n{new_filename}")
        except Exception as e:
            self.status_label.config(text="Failed to save document.", fg="red")
            messagebox.showerror("Error", f"Failed to save document:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentManagerApp(root)
    root.mainloop()