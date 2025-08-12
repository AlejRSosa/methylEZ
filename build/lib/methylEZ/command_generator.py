import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def generate_samplesheet(self):
    try:
        samplesheet_path = os.path.join(self.output_dir.get(), self.samplesheet_name.get())
        if os.path.exists(samplesheet_path):
            if not messagebox.askyesno("Confirmation", f"Samplesheet {samplesheet_path} already exists. Overwrite?"):
                return

        data = []
        paired_buffer = []

        for file_path in self.file_paths:
            sample_name = self.sample_names.get(file_path, os.path.basename(file_path).rsplit('.', 2)[0])
            if self.file_type.get(file_path) == "single":
                data.append([sample_name, file_path, ""])
            elif self.file_type.get(file_path) == "paired":
                paired_buffer.append(file_path)
                if len(paired_buffer) == 2:
                    data.append([sample_name, paired_buffer[0], paired_buffer[1]])
                    paired_buffer = []

        if not data:
            messagebox.showerror("Error", "No files selected or marked.")
            return

        samplesheet = pd.DataFrame(data, columns=["sample", "fastq_1", "fastq_2"])
        try:
            samplesheet.to_csv(samplesheet_path, index=False)
        except IOError as e:
            messagebox.showerror("File Error", f"Failed to save the samplesheet: {e}")
            return

        messagebox.showinfo("Success", f"Samplesheet saved at {samplesheet_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while generating the samplesheet: {e}")

def generate_command(self):
    try:
        samplesheet_path = os.path.join(self.output_dir.get(), self.samplesheet_name.get())
        if not os.path.exists(samplesheet_path):
            raise FileNotFoundError(f"Samplesheet not found at {samplesheet_path}. Please generate it first.")

        command = (f"nextflow run nf-core/methylseq --input {samplesheet_path} "
                   f"--outdir {self.output_dir.get()} --genome {self.genome.get()} "
                   f"--aligner {self.aligner.get()} --profile {self.profile.get()}")

        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(tk.END, command)
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while generating the command: {e}")
