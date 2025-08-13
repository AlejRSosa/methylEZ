import os 
import tkinter as tk
from tkinter import messagebox
import pandas as pd

# The code below was at the top level and caused an indentation error.
# If you need to validate the samplesheet, move this logic inside a function after 'data' is defined.
# For now, it is removed to fix the syntax error.


def generate_samplesheet(self):
    try:
        output_dir = self.output_dir.get()
        if not output_dir or not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Please select a valid output directory.")
            return

        samplesheet_path = os.path.join(output_dir, self.samplesheet_name.get())        
        if os.path.exists(samplesheet_path):
            if not messagebox.askyesno("Confirmation", f"Samplesheet {samplesheet_path} already exists. Overwrite?"):
                return

        data = []

        # Group paired files by sample name first
        paired_files = {}
        for file_path in self.file_paths:
            basename = os.path.basename(file_path)
            sample_name = self.sample_names.get(file_path, basename.split('.')[0])

            if self.file_type.get(file_path) == "single":
                data.append([sample_name, file_path, ""])
            elif self.file_type.get(file_path) == "paired":
                if sample_name not in paired_files:
                    paired_files[sample_name] = []
                paired_files[sample_name].append(file_path)

        # Validate required parameters
        required_params = {
            'genome': self.genome.get(),
            'aligner': self.aligner.get(),
            'profile': self.profile.get(),
            'output_dir': self.output_dir.get()
        }
        
        for param_name, param_value in required_params.items():
            if not param_value or param_value.strip() == "":
                raise ValueError(f"Required parameter '{param_name}' is empty")
        
        command = (
            f"nextflow run nf-core/methylseq \\\n"
            f"  --input {samplesheet_path} \\\n"
            f"  --outdir {self.output_dir.get()} \\\n"
            f"  --genome {self.genome.get()} \\\n"
            f"  --aligner {self.aligner.get()} \\\n"
            f"  --profile {self.profile.get()}"
        )
        for sample_name, files in paired_files.items():
            if len(files) == 2:
                data.append([sample_name, files[0], files[1]])
            else:
                messagebox.showwarning(
                    "Warning",
                    f"Sample {sample_name} has {len(files)} paired files, expected 2"
                )

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
