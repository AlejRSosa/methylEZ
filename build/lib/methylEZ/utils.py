import tkinter as tk
import pyperclip
from tkinter import filedialog, messagebox

def copy_command_to_clipboard(self):
    """Copy the generated command to the clipboard."""
    try:
        command = self.command_text.get("1.0", tk.END).strip()
        if not command:
            raise ValueError("The command text is empty. Please generate a command first.")
        pyperclip.copy(command)
        messagebox.showinfo("Copied", "Command copied to clipboard.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while copying the command: {e}")

def select_directory(self):
    """Open a directory selection dialog and set the output directory."""
    try:
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)
        else:
            messagebox.showwarning("No Selection", "No directory was selected.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while selecting a directory: {e}")
