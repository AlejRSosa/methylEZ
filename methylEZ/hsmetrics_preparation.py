#we need biopython (pip install biopython) and samtools (https://www.htslib.org/download/)
#we need to install picard tools (https://broadinstitute.github.io/picard/)
import os
import subprocess
from Bio import SeqIO
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# helper functions

def sort_key(record):
        order = {str(i): i for i in range(1, 23)}
        order['X'] = 23
        order['Y'] = 24
        order['MT'] = 25
        chrom = record.id.split(' ')[0]
        return (order.get(chrom, 26), chrom)
    
def sort_fasta_file(input_fasta, output_fasta):
    # Read sequences into a list
    records = list(SeqIO.parse(input_fasta, "fasta"))
    # Sort records based on custom key
    records.sort(key=sort_key)
    # Write sorted records to a new fasta file
    SeqIO.write(records, output_fasta, "fasta")

class PicardPreparationFrame(ttk.Frame):
    def __init__(self, parent, controller,output_dir, back_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.back_callback=back_callback
        self.output_dir=output_dir

        row = 0
        
        # (1) Output Directory Section
        out_frame = ttk.Frame(self)
        out_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=5, padx=5)
        out_label = ttk.Label(out_frame, text="Output Directory:")
        out_label.grid(row=0, column=0, sticky="w")
        self.out_entry = ttk.Entry(out_frame, width=50)
        self.out_entry.grid(row=0, column=1, sticky="ew")
        out_button = ttk.Button(out_frame, text="Browse", command=self.select_output_dir)
        out_button.grid(row=0, column=2, sticky="e", padx=5)
        row += 1
        
        # (2) Reference FASTA Section
        ref_frame = ttk.LabelFrame(self, text="Reference FASTA Preparation")
        ref_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=5, padx=5)
        ref_label = ttk.Label(ref_frame, text="Reference FASTA:")
        ref_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.fasta_entry = ttk.Entry(ref_frame, width=50)
        self.fasta_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        fasta_button = ttk.Button(ref_frame, text="Browse", command=self.select_fasta)
        fasta_button.grid(row=0, column=2, padx=5, pady=2)
        sort_button = ttk.Button(ref_frame, text="Sort FASTA", command=self.sort_fasta)
        sort_button.grid(row=1, column=0, padx=5, pady=2)
        index_button = ttk.Button(ref_frame, text="Index FASTA", command=self.index_fasta)
        index_button.grid(row=1, column=1, padx=5, pady=2)
        dict_button = ttk.Button(ref_frame, text="Create Sequence Dictionary", command=self.create_dict)
        dict_button.grid(row=1, column=2, padx=5, pady=2)
        #Export command for FASTA section only
        export_fasta_button = ttk.Button(ref_frame, text="Export FASTA Commands", command=self.export_fasta_commands)
        export_fasta_button.grid(row=2, column=0, columnspan=3, pady=2)
        row += 1
        
        # (3) BAM File Section
        bam_frame = ttk.LabelFrame(self, text="BAM File Preparation")
        bam_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=5, padx=5)
        bam_label = ttk.Label(bam_frame, text="BAM File:")
        bam_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.bam_entry = ttk.Entry(bam_frame, width=50)
        self.bam_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        bam_button = ttk.Button(bam_frame, text="Browse", command=self.select_bam)
        bam_button.grid(row=0, column=2, padx=5, pady=2)
        bam_sort_button = ttk.Button(bam_frame, text="Sort BAM", command=self.sort_bam)
        bam_sort_button.grid(row=1, column=0, padx=5, pady=2)
        bam_index_button = ttk.Button(bam_frame, text="Index BAM", command=self.index_bam)
        bam_index_button.grid(row=1, column=1, padx=5, pady=2)
        #Export command for BAM section only
        export_bam_button = ttk.Button(bam_frame, text="Export BAM Commands", command=self.export_bam_commands)
        export_bam_button.grid(row=2, column=0, columnspan=3, pady=2)
        row += 1
        
        # (4) BED File Section
        bed_frame = ttk.LabelFrame(self, text="BED File Preparation")
        bed_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=5, padx=5)
        bed_label = ttk.Label(bed_frame, text="BED File:")
        bed_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.bed_entry = ttk.Entry(bed_frame, width=50)
        self.bed_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        bed_button = ttk.Button(bed_frame, text="Browse", command=self.select_bed)
        bed_button.grid(row=0, column=2, padx=5, pady=2)
        interval_button = ttk.Button(bed_frame, text="Generate Interval List", command=self.generate_interval_list)
        interval_button.grid(row=3, column=0, columnspan=3, pady=2)
        dict_label = ttk.Label(bed_frame, text="Sequence Dictionary:")
        dict_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.dict_entry = ttk.Entry(bed_frame, width=50)
        self.dict_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        dict_button = ttk.Button(bed_frame, text="Browse", command=self.select_dict)
        dict_button.grid(row=2, column=2, padx=5, pady=2)
        #Export command for BED section only
        export_bed_button = ttk.Button(bed_frame, text="Export BED Commands", command=self.export_bed_commands)
        export_bed_button.grid(row=3, column=0, columnspan=3, pady=2)
        row += 1
        
        # (5) Export Preparation Commands
        export_button = ttk.Button(self, text="Export Preparation Commands", command=self.export_preparation_commands)
        export_button.grid(row=row, column=0, columnspan=3, pady=5)
        row += 1

        # Widget for status messages - unsure if needed 
        self.log_text = tk.Text(self, height=8, width=70, state="disabled")
        self.log_text.grid(row=row, column=0, columnspan=3, pady=5, padx=5)
    
    # Output Directory methods
    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.out_entry.delete(0, tk.END)
            self.out_entry.insert(0, directory)
    
    # Reference FASTA methods
    def select_fasta(self):
        file = filedialog.askopenfilename(title="Select Reference FASTA",
                                          filetypes=[("FASTA files", "*.fa *.fasta")])
        if file:
            self.fasta_entry.delete(0, tk.END)
            self.fasta_entry.insert(0, file)

    # sorting, indexing and creating functions 
    def sort_fasta(self):
        fasta = self.fasta_entry.get()
        if not fasta:
            messagebox.showerror("Error", "Please select a FASTA file.")
            return
        sorted_fasta = os.path.join(os.path.dirname(fasta), "sorted_" + os.path.basename(fasta))
        self.log("Sorting FASTA...")
        try:
            sort_fasta_file(fasta, sorted_fasta)
            self.log(f"Sorted FASTA saved as: {sorted_fasta}")
            self.fasta_entry.delete(0, tk.END)
            self.fasta_entry.insert(0, sorted_fasta)
        except Exception as e:
            self.log("Error sorting FASTA: " + str(e))

    
    def index_fasta(self):
        fasta = self.fasta_entry.get()
        if not fasta:
            messagebox.showerror("Error", "Please select (or generate) a sorted FASTA file.")
            return
        fasta=os.path.normpath(fasta)
        cmd = f'samtools faidx "{fasta}"'
        self.log("Indexing FASTA with samtools faidx...")
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.log("FASTA indexing completed.")
        except subprocess.CalledProcessError as e:
            self.log("Error indexing FASTA: " + str(e))
    
    def create_dict(self):
        fasta = self.fasta_entry.get()
        if not fasta:
            messagebox.showerror("Error", "Please select (or generate) a sorted FASTA file.")
            return
        dict_file = os.path.splitext(fasta)[0] + ".dict"
        picard_jar_path = os.path.join(os.getcwd(), "lib", "picard.jar")
        cmd = f'java -jar "{picard_jar_path}" CreateSequenceDictionary R="{fasta}" O="{dict_file}"'
        self.log("Creating sequence dictionary...")
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.log("Sequence dictionary created: " + dict_file)
        except subprocess.CalledProcessError as e:
            self.log("Error creating sequence dictionary: " + str(e))
    
    # BAM methods
    def select_bam(self):
        file = filedialog.askopenfilename(title="Select BAM file",
                                          filetypes=[("BAM files", "*.bam")])
        if file:
            self.bam_entry.delete(0, tk.END)
            self.bam_entry.insert(0, file)
    
    def sort_bam(self):
        bam = self.bam_entry.get()
        if not bam:
            messagebox.showerror("Error", "Please select a BAM file.")
            return
        sorted_bam = os.path.join(os.path.dirname(bam), "sorted_" + os.path.basename(bam))
        cmd = f'samtools sort "{bam}" -o "{sorted_bam}"'
        self.log("Sorting BAM...")
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.log("Sorted BAM saved as: " + sorted_bam)
            self.bam_entry.delete(0, tk.END)
            self.bam_entry.insert(0, sorted_bam)
        except subprocess.CalledProcessError as e:
            self.log("Error sorting BAM: " + str(e))
    
    def index_bam(self):
        bam = self.bam_entry.get()
        if not bam:
            messagebox.showerror("Error", "Please select (or generate) a sorted BAM file.")
            return
        cmd = f'samtools index "{bam}"'
        self.log("Indexing BAM with samtools index...")
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.log("BAM indexing completed.")
        except subprocess.CalledProcessError as e:
            self.log("Error indexing BAM: " + str(e))
    
    # BED methods
    def select_bed(self):
        file = filedialog.askopenfilename(title="Select BED file",
                                          filetypes=[("BED files", "*.bed")])
        if file:
            self.bed_entry.delete(0, tk.END)
            self.bed_entry.insert(0, file)
    
    def select_dict(self):
        file = filedialog.askopenfilename(title="Select Sequence Dictionary",
                                          filetypes=[("Dictionary files", "*.dict")])
        if file:
            self.dict_entry.delete(0, tk.END)
            self.dict_entry.insert(0, file)

    #TO BE MODIFIED!!
    def generate_interval_list(self):
        bed = self.bed_entry.get()
        output_dir = self.out_entry.get()
        dict_file = self.dict_entry.get()  # Reference sequence dictionary
        if not bed or not output_dir:
            messagebox.showerror("Error", "Please select a BED file and an output directory.")
            return
        output_file = os.path.join(output_dir, os.path.basename(bed).replace(".bed", ".interval_list"))
        # HERE YOU MUST REPLACE 'cp' command with the actual method!!!
        picard_jar_path = os.path.join(os.getcwd(), "lib", "picard.jar")
        cmd = f'java -jar "{picard_jar_path}" BedToIntervalList -I "{bed}" -O "{output_file}" -SD "{dict_file}"'
        self.log("Generating interval list from BED file...")
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.log("Interval list created: " + output_file)
        except subprocess.CalledProcessError as e:
            self.log("Error generating interval list: " + str(e))
    
    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)


    def export_fasta_commands(self):
            fasta = self.fasta_entry.get()
            if not fasta:
                messagebox.showerror("Error", "No FASTA file selected.")
                return
            sorted_fasta = os.path.join(os.path.dirname(fasta), "sorted_" + os.path.basename(fasta))
            picard_jar_path = os.path.join(os.getcwd(), "lib", "picard.jar")
            dict_file = os.path.splitext(sorted_fasta)[0] + ".dict"
            
            code = f'''#!/usr/bin/env python
    from Bio import SeqIO

    def sort_key(record):
        order = {{str(i): i for i in range(1, 23)}}
        order['X'] = 23
        order['Y'] = 24
        order['MT'] = 25
        chrom = record.id.split(' ')[0]
        return (order.get(chrom, 26), chrom)

    def sort_fasta_file(input_fasta, output_fasta):
        records = list(SeqIO.parse(input_fasta, "fasta"))
        records.sort(key=sort_key)
        SeqIO.write(records, output_fasta, "fasta")

    if __name__ == "__main__":
        input_fasta = r"{fasta}"
        output_fasta = r"{sorted_fasta}"
        sort_fasta_file(input_fasta, output_fasta)
        print("Sorted FASTA saved as", output_fasta)
    '''
            # Add a separator and further commands
            sep = "\n\n# --------------------\n\n"
            code += sep + f'samtools faidx "{sorted_fasta}"'
            code += sep + f'java -jar "{picard_jar_path}" CreateSequenceDictionary R="{sorted_fasta}" O="{dict_file}"'
            
            filename = filedialog.asksaveasfilename(
                title="Save FASTA Commands",
                defaultextension=".txt",
                initialdir=self.out_entry.get(),
                initialfile="fasta_commands.txt"
            )
            if filename:
                try:
                    with open(filename, "w") as f:
                        f.write(code)
                    messagebox.showinfo("Success", f"FASTA commands exported to:\n{filename}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error writing file: {e}")
            else:
                messagebox.showinfo("Canceled", "No file selected.")

    def export_bam_commands(self):
            bam = self.bam_entry.get()
            if not bam:
                messagebox.showerror("Error", "No BAM file selected.")
                return
            sorted_bam = os.path.join(os.path.dirname(bam), "sorted_" + os.path.basename(bam))
            code = f'''# Commands for BAM file preparation
    samtools sort "{bam}" -o "{sorted_bam}"
    samtools index "{sorted_bam}"
    '''
            filename = filedialog.asksaveasfilename(
                title="Save BAM Commands",
                defaultextension=".txt",
                initialdir=self.out_entry.get(),
                initialfile="bam_commands.txt"
            )
            if filename:
                try:
                    with open(filename, "w") as f:
                        f.write(code)
                    messagebox.showinfo("Success", f"BAM commands exported to:\n{filename}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error writing file: {e}")
            else:
                messagebox.showinfo("Canceled", "No file selected.")


    def export_bed_commands(self):
            bed = self.bed_entry.get()
            output_dir = self.out_entry.get()
            if not bed or not output_dir:
                messagebox.showerror("Error", "Please select a BED file and an output directory.")
                return
            output_interval = os.path.join(output_dir, os.path.basename(bed).replace(".bed", ".interval_list"))
            code = f'''# Command for generating interval list from BED file
    cp "{bed}" "{output_interval}"
    '''
            filename = filedialog.asksaveasfilename(
                title="Save BED Commands",
                defaultextension=".txt",
                initialdir=output_dir,
                initialfile="bed_commands.txt"
            )
            if filename:
                try:
                    with open(filename, "w") as f:
                        f.write(code)
                    messagebox.showinfo("Success", f"BED commands exported to:\n{filename}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error writing file: {e}")
            else:
                messagebox.showinfo("Canceled", "No file selected.")

    def export_preparation_commands(self):
        # As the hybrid approach of this GUI is to provide a 
        # template that the user can modify, this method allows the user to 
        # export a .txt with the commands that should be used in cmd
        output_dir = self.out_entry.get() if hasattr(self, "out_entry") else os.getcwd()
        fasta = self.fasta_entry.get()
        bam = self.bam_entry.get()
        bed = self.bed_entry.get()

        # if user provides a value
        commands = []
        if fasta:
            sorted_fasta = os.path.join(os.path.dirname(fasta), "sorted_" + os.path.basename(fasta))
            prep_code = f'''#!/usr/bin/env python
        from Bio import SeqIO

        def sort_key(record):
            order = {{str(i): i for i in range(1, 23)}}
            order['X'] = 23
            order['Y'] = 24
            order['MT'] = 25
            chrom = record.id.split(' ')[0]
            return (order.get(chrom, 26), chrom)

        def sort_fasta_file(input_fasta, output_fasta):
            records = list(SeqIO.parse(input_fasta, "fasta"))
            records.sort(key=sort_key)
            SeqIO.write(records, output_fasta, "fasta")

        if __name__ == "__main__":
            input_fasta = r"{fasta}"
            output_fasta = r"{sorted_fasta}"
            sort_fasta_file(input_fasta, output_fasta)
            print("Sorted FASTA saved as", output_fasta)
        '''
            commands.append(prep_code)
            commands.append(f'samtools faidx "{sorted_fasta}"')
            picard_jar_path = os.path.join(os.getcwd(), "lib", "picard.jar")
            dict_file = os.path.splitext(sorted_fasta)[0] + ".dict"
            commands.append(f'java -jar "{picard_jar_path}" CreateSequenceDictionary R="{sorted_fasta}" O="{dict_file}"')
        if bam:
            sorted_bam = os.path.join(os.path.dirname(bam), "sorted_" + os.path.basename(bam))
            commands.append(f'samtools sort "{bam}" -o "{sorted_bam}"')
            commands.append(f'samtools index "{sorted_bam}"')
        if bed:
            output_interval = os.path.join(output_dir, os.path.basename(bed).replace(".bed", ".interval_list"))
            # Here we assume a simple copy; replace with your actual command if needed.
            commands.append(f'cp "{bed}" "{output_interval}"')

        # Join the commands with newlines
        full_commands = "\n".join(commands)
        
        # Define a separator with an empty line and a comment
        separator = "\n\n# --------------------\n\n"
        full_commands = separator.join(commands)

        # Let the user choose where to save the file, with a default filename:
        filename = filedialog.asksaveasfilename(
            title="Save Preparation Commands",
            defaultextension=".txt",
            initialdir=output_dir,
            initialfile="preparation_commands.txt"
        )

        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(full_commands)
                messagebox.showinfo("Success", f"Preparation commands exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error writing file: {e}")
        else:
            messagebox.showinfo("Canceled", "No file selected.")