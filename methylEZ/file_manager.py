import tkinter as tk
from tkinter import filedialog, messagebox

def add_files(self):
    filetypes = (("FASTQ files", "*.fastq *.fastq.gz *.fq *.fq.gz"), ("All files", "*.*"))
    new_files = filedialog.askopenfilenames(title="Select FASTQ files", filetypes=filetypes)
    
    duplicate_files = [file for file in new_files if file in self.file_paths]
    if duplicate_files:
        messagebox.showerror("Error", "These files are already added: \n" + "\n".join(duplicate_files))
        return

    self.file_paths.extend(new_files)
    for file in new_files:
        self.file_listbox.insert(tk.END, file)

def clear_all_files(self):
    self.file_listbox.delete(0, tk.END)
    self.file_paths = []
    self.file_type = {}
    self.sample_names = {}

def clear_selected_files(self):
    selected_indices = list(self.file_listbox.curselection())
    selected_indices.reverse()

    for index in selected_indices:
        file_path = self.file_listbox.get(index)
        self.file_listbox.delete(index)
        self.file_paths.remove(file_path)
        self.file_type.pop(file_path, None)
        self.sample_names.pop(file_path, None)

def move_up(self):
    selected_indices = list(self.file_listbox.curselection())
    for index in selected_indices:
        if index == 0:
            continue
        file_path = self.file_listbox.get(index)
        self.file_listbox.delete(index)
        self.file_listbox.insert(index - 1, file_path)
        self.file_listbox.select_set(index - 1)
        # keep underlying list in sync
        try:
            idx_in_list = self.file_paths.index(file_path)
            if idx_in_list > 0:
                self.file_paths[idx_in_list - 1], self.file_paths[idx_in_list] = (
                    self.file_paths[idx_in_list],
                    self.file_paths[idx_in_list - 1],
                )
        except ValueError:
            pass

def move_down(self):
    selected_indices = list(self.file_listbox.curselection())
    for index in reversed(selected_indices):
        if index == self.file_listbox.size() - 1:
            continue
        file_path = self.file_listbox.get(index)
        self.file_listbox.delete(index)
        self.file_listbox.insert(index + 1, file_path)
        self.file_listbox.select_set(index + 1)
        # keep underlying list in sync
        try:
            idx_in_list = self.file_paths.index(file_path)
            if idx_in_list < len(self.file_paths) - 1:
                self.file_paths[idx_in_list + 1], self.file_paths[idx_in_list] = (
                    self.file_paths[idx_in_list],
                    self.file_paths[idx_in_list + 1],
                )
        except ValueError:
            pass

def mark_files(self, mark_type):
    """Mark files as single-end, paired-end, or neutral."""
    selected_indices = self.file_listbox.curselection()
    for index in selected_indices:
        file_path = self.file_listbox.get(index)
        self.file_type[file_path] = mark_type
        if mark_type == "single":
            self.file_listbox.itemconfig(index, {'bg': '#A6E1FF'})  # Color for single-end
        elif mark_type == "paired":
            self.file_listbox.itemconfig(index, {'bg': '#FFEE98'})  # Color for paired-end
        else:
            self.file_listbox.itemconfig(index, {'bg': 'white'})  # Neutral
    # Deselect files after marking
    self.file_listbox.selection_clear(0, tk.END)
