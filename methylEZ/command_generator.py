import os
import re
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def generate_samplesheet(self):
    try:
        # Output path checks
        output_dir = (self.output_dir.get() or "").strip()
        samplesheet_name = (self.samplesheet_name.get() or "samplesheet.csv").strip()
        samplesheet_path = os.path.join(output_dir, samplesheet_name)
        if not output_dir:
            messagebox.showerror("Error", "Output directory is not set.")
            return
        os.makedirs(output_dir, exist_ok=True)

        if os.path.exists(samplesheet_path):
            if not messagebox.askyesno("Confirmation", f"Samplesheet {samplesheet_path} already exists. Overwrite?"):
                return

        # ---- helpers focused ONLY on the R1/R2 requirement ----
        # Remove .fastq/.fq with optional compression suffix
        _strip_ext = lambda b: re.sub(r"\.(fastq|fq)(\.(gz|bz2|zst))?$", "", b, flags=re.IGNORECASE)

        # Read detection: case-insensitive; supports separators or plain suffix like SampleR1
        def read_of(stem: str):
            s = stem.lower()
            if re.search(r"(^|[._-])r?1([._-]|$)", s) or re.search(r"r?1$", s):
                return "1"
            if re.search(r"(^|[._-])r?2([._-]|$)", s) or re.search(r"r?2$", s):
                return "2"
            return None  # unknown

        def key_without_read(stem: str) -> str:
            # Remove the specific detected token (R1/R2) once; keep original case
            r = read_of(stem)
            k = stem
            if r:
                pat_boundary = re.compile(rf"(^|[._-])r?{r}(?=([._-]|$))", re.IGNORECASE)
                k2 = pat_boundary.sub(lambda m: m.group(1), k, count=1)
                if k2 == k:
                    # Try suffix without separator
                    k2 = re.sub(rf"(?i)r?{r}$", "", k2, count=1)
                k = k2
            k = re.sub(r"[._-]+$", "", k)
            return k

        # ---- requirement (1): must have files ----
        if not getattr(self, "file_paths", None):
            messagebox.showerror("Error", "No files selected.")
            return

        # ---- build rows: group first, then decide pairing (order-independent) ----
        groups = {}  # sample_key -> list of {path, base, read}
        for file_path in self.file_paths:
            base = os.path.basename(file_path)
            stem = _strip_ext(base)
            key = key_without_read(stem)
            r = read_of(stem)  # "1", "2", or None
            groups.setdefault(key, []).append({"path": file_path, "base": base, "read": r})

        data = []
        for sample_key, items in groups.items():
            # Pick the first R1 and first R2 regardless of order
            r1 = next((it["path"] for it in items if it["read"] == "1"), None)
            r2 = next((it["path"] for it in items if it["read"] == "2"), None)
            
            if r1 and r2:
                # FIXED: Ensure R1 goes to fastq_1 and R2 goes to fastq_2
                data.append([sample_key, r1, r2])  # R1 in fastq_1, R2 in fastq_2
            elif r1:
                data.append([sample_key, r1, ""])  # single-end with R1 only
            elif r2:
                # FIXED: For single R2, put it in fastq_1 column (standard practice)
                data.append([sample_key, r2, ""])  # single-end with R2 in fastq_1
            else:
                # No explicit R1/R2 token; write each as single-end deterministically
                for it in items:
                    data.append([sample_key, it["path"], ""]) 

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
        output_dir = (self.output_dir.get() or "").strip()
        samplesheet_name = (self.samplesheet_name.get() or "samplesheet.csv").strip()
        samplesheet_path = os.path.join(output_dir, samplesheet_name)
        if not os.path.exists(samplesheet_path):
            raise FileNotFoundError(f"Samplesheet not found at {samplesheet_path}. Please generate it first.")

        # Decide --single_end only if ALL rows are single-end
        all_single = False
        try:
            df = pd.read_csv(samplesheet_path)
            if "fastq_2" in df.columns:
                all_single = bool((df["fastq_2"].isna() | (df["fastq_2"].astype(str).str.len() == 0)).all())
        except Exception:
            all_single = False

        def dq(s: str) -> str: return f'"{s}"'

        command = (
            f"nextflow run nf-core/methylseq --input {dq(samplesheet_path)} "
            f"--outdir {dq(output_dir)} --genome {self.genome.get()} "
            f"--aligner {self.aligner.get()} --profile {self.profile.get()}"
        )
        if all_single:
            command += " --single_end"

        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(tk.END, command)
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while generating the command: {e}")