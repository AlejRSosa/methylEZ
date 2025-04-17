import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog, scrolledtext
#import subprocess
from methylEZ.hsmetrics_command_generator import generate_hsmetrics_command
#from methylEZ.hsmetrics_runner import run_picard_hsmetrics - not needed anymore cause we are focusing only on template generation
#from methylEZ.utils import copy_command_to_clipboard, select_directory
import methylEZ
from pathlib import Path
import methylEZ.hsmetrics_parser as hs_parser  #we will later call hs_parser.parse_picard_output()

class HSMetricsGUI(ttk.Frame):
    def __init__(self, parent, controller, output_dir, back_callback=None):
        super().__init__(parent, back_callback=back_callback)
        self.controller = controller
        self.root = controller
        self.output_dir = output_dir

        # GUI sections
        #self.create_file_selection_frame()
        # Remove the output directory input here, cause it's in the left pane.
        self.create_folder_selection_frame()
        self.create_command_generation_section()
        #self.create_real_time_output_section()
        self.create_status_bar()

        # Final button to export the code to .txt
        self.export_button = ttk.Button(self.command_button_frame, text="Export Template Code",
                                        command=self.export_run_code)
        self.export_button.grid(row=0, column=1, padx=5, pady=(0,5), sticky="ew") #changing column and padx to determine where it looks best
        #column=0, padx=5, pady=(0,5), sticky="ew"

    def create_folder_selection_frame(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=10, pady=10)
        label = ttk.Label(frame, text="Input Folder (BAM files):")
        label.pack(side=tk.LEFT, padx=5)
        self.bam_folder = tk.StringVar(value=os.getcwd())
        self.bam_folder_entry = ttk.Entry(frame, textvariable=self.bam_folder, width=50)
        self.bam_folder_entry.pack(side=tk.LEFT, padx=5)
        browse_button = ttk.Button(frame, text="Browse", command=self.select_bam_folder)
        browse_button.pack(side=tk.LEFT, padx=5)

        # we removed a file selection pane, but we still want to keep the target, bait and dictionary file selection
        options_frame = ttk.Frame(self)
        options_frame.pack(fill=tk.X, padx=10, pady=10)

        target_label = ttk.Label(options_frame, text="Target Interval File:")
        target_label.grid(row=0, column=0, padx=5, sticky="w")
        self.target_entry = tk.Entry(options_frame, width=30)
        self.target_entry.grid(row=1, column=0, padx=5, sticky="ew")
        target_button = ttk.Button(options_frame, text="Browse", command=lambda: self.select_file(self.target_entry))
        target_button.grid(row=2, column=0, padx=5, pady=(0,5), sticky="ew")

        bait_label = ttk.Label(options_frame, text="Bait Interval File:")
        bait_label.grid(row=0, column=1, padx=5, sticky="w")
        self.bait_entry = tk.Entry(options_frame, width=30)
        self.bait_entry.grid(row=1, column=1, padx=5, sticky="ew")
        bait_button = ttk.Button(options_frame, text="Browse", command=lambda: self.select_file(self.bait_entry))
        bait_button.grid(row=2, column=1, padx=5, pady=(0,5), sticky="ew")

        dict_label = ttk.Label(options_frame, text="Dictionary File:")
        dict_label.grid(row=0, column=2, padx=5, sticky="w")
        self.dict_entry = tk.Entry(options_frame, width=30)
        self.dict_entry.grid(row=1, column=2, padx=5, sticky="ew")
        dict_button = ttk.Button(options_frame, text="Browse", command=lambda: self.select_file(self.dict_entry))
        dict_button.grid(row=2, column=2, padx=5, pady=(0,5), sticky="ew")

    def select_bam_folder(self):
        folder = filedialog.askdirectory(title="Select BAM files folder")
        if folder:
            self.bam_folder.set(folder)

    """ def create_file_selection_frame(self):
        self.file_frame = ttk.Frame(self)
        self.file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        listbox_container = ttk.Frame(self.file_frame)
        listbox_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.file_frame.rowconfigure(0, weight=1)
        self.file_frame.columnconfigure(0, weight=1)

        lb_frame = ttk.Frame(listbox_container)
        lb_frame.grid(row=0, column=0, sticky="nsew")
        listbox_container.columnconfigure(0, weight=1)
        listbox_container.rowconfigure(0, weight=1)

        self.bam_listbox = tk.Listbox(lb_frame, height=12, selectmode=tk.MULTIPLE)
        self.bam_listbox.grid(row=0, column=0, sticky="nsew")
        lb_frame.rowconfigure(0, weight=1)
        lb_frame.columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(lb_frame, orient="vertical", command=self.bam_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.bam_listbox.config(yscrollcommand=scrollbar.set)

        button_panel = ttk.Frame(listbox_container)
        button_panel.grid(row=0, column=1, sticky="ns", padx=5)
        self.add_bam_button = ttk.Button(button_panel, text="Add BAM Files", command=self.add_bam_files)
        self.add_bam_button.pack(fill='x', pady=(0, 5))
        self.remove_bam_button = ttk.Button(button_panel, text="Remove Selected", command=self.remove_selected_files)
        self.remove_bam_button.pack(fill='x')

        options_frame = ttk.Frame(self.file_frame)
        options_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(2, weight=1)

        target_label = ttk.Label(options_frame, text="Target Interval File:")
        target_label.grid(row=0, column=0, padx=5, sticky="w")
        self.target_entry = tk.Entry(options_frame, width=30)
        self.target_entry.grid(row=1, column=0, padx=5, sticky="ew")
        target_button = ttk.Button(options_frame, text="Browse", command=lambda: self.select_file(self.target_entry))
        target_button.grid(row=2, column=0, padx=5, pady=(0,5), sticky="ew")

        bait_label = ttk.Label(options_frame, text="Bait Interval File:")
        bait_label.grid(row=0, column=1, padx=5, sticky="w")
        self.bait_entry = tk.Entry(options_frame, width=30)
        self.bait_entry.grid(row=1, column=1, padx=5, sticky="ew")
        bait_button = ttk.Button(options_frame, text="Browse", command=lambda: self.select_file(self.bait_entry))
        bait_button.grid(row=2, column=1, padx=5, pady=(0,5), sticky="ew")

        dict_label = ttk.Label(options_frame, text="Dictionary File:")
        dict_label.grid(row=0, column=2, padx=5, sticky="w")
        self.dict_entry = tk.Entry(options_frame, width=30)
        self.dict_entry.grid(row=1, column=2, padx=5, sticky="ew")
        dict_button = ttk.Button(options_frame, text="Browse", command=lambda: self.select_file(self.dict_entry))
        dict_button.grid(row=2, column=2, padx=5, pady=(0,5), sticky="ew")
 """
    """ def remove_selected_files(self):
        selected_indices = self.bam_listbox.curselection()
        for index in reversed(selected_indices):
            self.bam_listbox.delete(index) """

    def create_command_generation_section(self):
        self.command_button_frame = ttk.Frame(self)
        self.command_button_frame.pack(pady=5)

        self.generate_command_button = ttk.Button(self.command_button_frame, text="Generate Command",
                                                  command=lambda: generate_hsmetrics_command(self))
        self.generate_command_button.grid(row=0, column=0, padx=5)
        self.parse_output_button = ttk.Button(self.command_button_frame, text="Parse CollectHsMetrics Output",
                                           command=self.run_parser)
        self.parse_output_button.grid(row=1, column=0, padx=5)
        self.export_parser_button = ttk.Button(self.command_button_frame, text="Export Parser Template",
                                            command=self.export_parse_template)
        self.export_parser_button.grid(row=1, column=1, padx=5)
        #self.run_command_button = ttk.Button(self.command_button_frame, text="Run Picard CollectHsMetrics",
        #                                     command=lambda: run_picard_hsmetrics(self))
        #self.run_command_button.grid(row=0, column=1, padx=5)
        #self.copy_command_button = ttk.Button(self.command_button_frame, text="Copy Command",
        #                                      command=lambda: copy_command_to_clipboard(self))
        #self.copy_command_button.grid(row=0, column=1, padx=5)

        #self.command_text = tk.Text(self.command_button_frame, height=4, width=100)
        #self.command_text.grid(row=1, column=0, columnspan=3, pady=5)
    """ def create_real_time_output_section(self):
        self.output_frame = ttk.Frame(self)
        self.output_frame.pack(pady=5)
        self.output_label = ttk.Label(self.output_frame, text="Real-Time Execution Output:")
        self.output_label.pack()
        self.output_text = scrolledtext.ScrolledText(self.output_frame, height=10, width=120, state=tk.DISABLED)
        self.output_text.pack() """

    def update_status_bar(self, message):
        self.status_bar.config(text=message)

    def create_status_bar(self):
        try:
            self.status_bar = tk.Label(self, text="Ready", bg="#90E0D3", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Helvetica", 20))
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the status bar: {e}")

    def set_status(self, text):
        try:
            self.status_bar.config(text=text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating the status bar: {e}")

    def add_bam_files(self):
        files = filedialog.askopenfilenames(
            title="Select BAM files",
            filetypes=[("BAM files", "*.bam *.cov"), ("All files", "*")]
        )
        for file in files:
            self.bam_listbox.insert(tk.END, file)

    def select_file(self, entry):
        file = filedialog.askopenfilename()
        if file:
            entry.delete(0, tk.END)
            entry.insert(0, file)

    """ def run_picard_hsmetrics(self):
        command = self.command_text.get("1.0", tk.END).strip()
        if not command:
            messagebox.showerror("Error", "No command generated. Please generate it first.")
            return

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "Running Picard CollectHsMetrics...\n")
        self.output_text.config(state=tk.DISABLED)

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, line)
            self.output_text.yview(tk.END)
            self.output_text.config(state=tk.DISABLED)

        process.wait()
        messagebox.showinfo("Completed", "Picard CollectHsMetrics has finished running.")
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "\nProcess completed.\n")
        self.output_text.config(state=tk.DISABLED)
 """
    def export_run_code(self):
        # Get common parameters from the entries:
        output_dir = self.output_dir.get() if hasattr(self, "output_dir") else os.getcwd()
        target_intervals = self.target_entry.get()
        bait_intervals = self.bait_entry.get()
        dict_file = self.dict_entry.get()
        
        # Get the input folder (instead of a list of BAM files)
        bam_folder = self.bam_folder.get()
        if not bam_folder:
            messagebox.showerror("Error", "No input folder specified for BAM files.")
            return

        picard_jar = Path(methylEZ.__file__).resolve().parent / "assets" / "picard.jar"
        ref_genome = "filtered_hg19_ensembl.fa"  # or get from an entry if you allow the user to change it

        # Build the code snippet as a multiline string.
        code_lines = [
            "# Code to run Picard CollectHsMetrics",
            "# Generated by MethylEZ",
            "#!/usr/bin/env python",
            "",
            "import os",
            "import glob",
            "import subprocess",
            "",
            "# Folder for the input BAM files",
            f'bam_folder = r"{bam_folder}"',
            "bam_files = glob.glob(os.path.join(bam_folder, '*.bam'))",
            "",
            "# Output directory",
            f'output_dir = r"{output_dir}"',
            "# If picard.jar is not in the same directory as this script, specify the full path",
            f'picard_jar = r"{picard_jar}"',
            "# Reference genome",
            f'ref_genome = r"{ref_genome}"',
            "# Target and bait intervals",
            f'target_intervals = r"{target_intervals}"',
            f'bait_intervals = r"{bait_intervals}"',
            "# Dictionary file",
            f'dict_file = r"{dict_file}"',
            "",
            "for bam in bam_files:",
            "    base = os.path.basename(bam)",
            "    output_file = os.path.join(output_dir, base.replace('.bam', '_hs_metrics.txt'))",
            "    command = (f'java -jar \"{picard_jar}\" CollectHsMetrics '",
            "               f'-I \"{bam}\" -O \"{output_file}\" '",
            "               f'-R \"{ref_genome}\" '",
            "               f'-TARGET_INTERVALS \"{target_intervals}\" '",
            "               f'-BAIT_INTERVALS \"{bait_intervals}\"')",
            "    subprocess.run(command, shell=True, check=True)",
            "    print(f'Processed: {bam}')",
        ]
        full_code = "\n".join(code_lines)

        # Let the user choose where to save the file:
        filename = filedialog.asksaveasfilename(title="Save Run Code", defaultextension=".py", initialdir=output_dir)
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(full_code)
                messagebox.showinfo("Success", f"Run code exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error writing file: {e}")
        else:
            messagebox.showinfo("Canceled", "No file selected.")
        
    def run_parser(self):    
        directory = filedialog.askdirectory(title="Select Folder containing Picard Output Files")
        if not directory:
            messagebox.showerror("Error", "No folder selected for parsing.")
            return

        # Ask the user where to save the consolidated CSV.
        output_csv = filedialog.asksaveasfilename(title="Save Parsed Output as CSV",
                                                defaultextension=".csv")
        if not output_csv:
            messagebox.showinfo("Canceled", "No output file selected.")
            return

        try:
            hs_parser.parse_picard_output(directory, output_csv)
            messagebox.showinfo("Success", f"Parsed data saved to {output_csv}")
        except Exception as e:
            messagebox.showerror("Error", f"Error during parsing: {e}") 
    
    def export_parser_template(self):
        # Define a template string that calls your parser function.
        template_code = '''#!/usr/bin/env python
    from methylEZ.hsmetrics_parser import parse_picard_output

    # Set these variables accordingly:
    picard_output_directory = r"Path_to_Picard_Output_Folder"
    output_csv = r"Path_where_the_CSV_should_be_saved.csv"

    parse_picard_output(picard_output_directory, output_csv)
    print("Parsed data saved to", output_csv)
    '''
        # Ask the user where to save the file:
        output_dir = self.output_dir.get() if hasattr(self, "output_dir") else os.getcwd()
        filename = filedialog.asksaveasfilename(title="Save Parser Template",
                                                defaultextension=".py",
                                                initialdir=output_dir,
                                                initialfile="parser_template.py")
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(template_code)
                messagebox.showinfo("Success", f"Parser template exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error writing file: {e}")
        else:
            messagebox.showinfo("Canceled", "No file selected.")

    def export_parse_template(self):
        """
        Exports a self-contained Python template script for parsing Picard output files.
        The template contains inline code (no external dependencies on methylEZ) so that
        the user can modify the input folder and output CSV paths as needed.
        """
        template_code = '''#!/usr/bin/env python
    import os
    import glob
    import pandas as pd

    def parse_picard_output(directory, output_csv):
        """
        Parses Picard CollectHsMetrics output files in the specified directory
        and consolidates them into a CSV file.
        
        It looks for files matching the pattern "*_hs_metrics_Ly.txt", extracts the header
        from the first file, and prepends each data line with the sample identifier.
        """
        files = glob.glob(os.path.join(directory, "*_hs_metrics_Ly.txt"))
        if not files:
            print("No Picard output files found in", directory)
            return

        all_lines = []
        header_written = False

        for file in files:
            sample_id = os.path.basename(file).replace("_hs_metrics_Ly.txt", "")
            with open(file, "r") as f:
                lines = f.readlines()
            try:
                start_idx = next(i for i, line in enumerate(lines) if "## METRICS CLASS" in line) + 1
                end_idx = next(i for i, line in enumerate(lines) if "## HISTOGRAM" in line)
                metrics = lines[start_idx:end_idx]
                if not metrics or len(metrics) < 2:
                    print(f"Skipping file {file}: not enough data lines.")
                    continue
                if not header_written:
                    header = "SAMPLE_IDENTIFIER\t" + metrics[0].strip()
                    all_lines.append(header)
                    header_written = True
                for line in metrics[1:]:
                    clean_line = line.strip()
                    if not clean_line or "BAIT_SET" in clean_line:
                        continue
                    all_lines.append(f"{sample_id}\t{clean_line}")
            except StopIteration:
                print(f"Skipping file {file}: Incorrect format.")
                continue

        with open(output_csv, "w") as f:
            f.write("\n".join(all_lines))
        print(f"Parsed data saved to {output_csv}")

    if __name__ == "__main__":
        # MODIFY THE FOLLOWING PATHS BEFORE RUNNING:
        picard_output_dir = r"/path/to/PicardOutputs"
        output_csv = r"/path/to/parsed_output.csv"
        parse_picard_output(picard_output_dir, output_csv)
    '''
        # Where to save the file (ask user input)
        filename = filedialog.asksaveasfilename(title="Save Parsing Template", defaultextension=".py",
                                                initialfile="parse_picard_template.py")
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(template_code)
                messagebox.showinfo("Success", f"Parser template exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error writing file: {e}")
        else:
            messagebox.showinfo("Canceled", "No file selected.")
