import os
import glob
import tkinter as tk
from tkinter import messagebox

# Variables (preset, but can be changed by user)

DEFAULT_REF_GENOME = "filtered_hg19_ensembl.fa"
DEFAULT_PICARD_JAR = os.path.join(os.getcwd(), "lib", "picard.jar")
# get current working directory and joins it with the lib directory name and file name
# using the right path separator according to operating system (Win \, Linux or Mac /)

def clean_output_filename(bam_file):
    """ Generates a cleaner output filename stripping known suffixes, might not work with all """
    base = os.path.basename(bam_file)
    suffixes = [".sorted.bam", ".deduplicated.bismark.cov.gz", ".cov.gz", ".bam", ".cov"]
    for suf in suffixes:
        if base.endswith(suf):
            base = base[:-len(suf)]
            break
    return base + "_hs_metrics.txt"

def generate_hsmetrics_command(self):
    """Generates the Picard CollectHsMetrics command based on user inputs."""
    #bam_files = [self.bam_listbox.get(idx) for idx in range(self.bam_listbox.size())]
    bam_folder = self.bam_folder.get()
    bam_files= glob.glob(os.path.join(bam_folder, "*.bam"))
    if not bam_files:
        messagebox.showerror("Error", "No BAM files selected.")
        return

    output_dir = self.output_dir.get()
    target_intervals = self.target_entry.get()
    bait_intervals = self.bait_entry.get()

    if not target_intervals or not bait_intervals:
        messagebox.showerror("Error", "Target and Bait interval files must be selected.")
        return

    ref_genome = DEFAULT_REF_GENOME
    picard_jar = DEFAULT_PICARD_JAR

    command_lines = []
    for bam in bam_files:
        output_file = os.path.join(output_dir, clean_output_filename(bam))
        command = (
            f"java -jar \"{picard_jar}\" CollectHsMetrics "
            f"-I \"{bam}\" -O \"{output_file}\" "
            f"-R \"{ref_genome}\" "
            f"-TARGET_INTERVALS \"{target_intervals}\" "
            f"-BAIT_INTERVALS \"{bait_intervals}\""
        )
        command_lines.append(command)

    full_command = "\n".join(command_lines)
    self.command_text.delete(1.0, tk.END)
    self.command_text.insert(tk.END, full_command)
