# Defines a DMRAnalysisGUI(ttk.Frame) class
# that creates a GUI for DMR analysis using tkinter and ttk

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from methylEZ.dmr_template_generator import export_methylkit_template


class DMRAnalysisGUI(ttk.Frame):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.back_callback = back_callback

        # Initialize configuration variables
        self.base_dir = tk.StringVar()
        self.genome_assembly = tk.StringVar(value="hg19")
        self.bedfile_path = tk.StringVar()
        self.min_coverage = tk.IntVar(value=10)
        self.max_coverage_percentile = tk.DoubleVar(value=99.9)
        self.sd_cutoff = tk.DoubleVar(value=2.0)
        self.tile_win_size = tk.IntVar(value=500)
        self.tile_step_size = tk.IntVar(value=300)
        self.sample_group_recode = tk.StringVar(value='c("Group1"=0, "Group2"=1)')
        self.group_column = tk.StringVar(value="Sample_Group")
        self.file_column = tk.StringVar(value="file_name")
        self.id_column = tk.StringVar(value="Sample_ID")
        self.output_dir = tk.StringVar(value=os.getcwd())

        self._build_widgets()

    def _build_widgets(self):
        # Directory Selection
        dir_frame = ttk.LabelFrame(self, text="Project & Output Directories")
        dir_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(dir_frame, text="Base Directory:").grid(row=0, column=0, sticky="w")
        ttk.Entry(dir_frame, textvariable=self.base_dir, width=60).grid(row=0, column=1, padx=5)
        ttk.Button(dir_frame, text="Browse", command=self._select_base_dir).grid(row=0, column=2)

        ttk.Label(dir_frame, text="Output Directory:").grid(row=1, column=0, sticky="w")
        ttk.Entry(dir_frame, textvariable=self.output_dir, width=60).grid(row=1, column=1, padx=5)
        ttk.Button(dir_frame, text="Browse", command=self._select_output_dir).grid(row=1, column=2)

        # Configurable Settings Frame
        config_frame = ttk.LabelFrame(self, text="DMR Settings")
        config_frame.pack(fill="x", padx=10, pady=5)

        row = 0
        for label, var in [
            ("Genome Assembly:", self.genome_assembly),
            ("BED File Path:", self.bedfile_path),
            ("Min Coverage:", self.min_coverage),
            ("Max Coverage Percentile:", self.max_coverage_percentile),
            ("SD Cutoff:", self.sd_cutoff),
            ("Tile Window Size:", self.tile_win_size),
            ("Tile Step Size:", self.tile_step_size),
            ("Sample Group Recode (R syntax):", self.sample_group_recode),
            ("Group Column:", self.group_column),
            ("File Column:", self.file_column),
            ("ID Column:", self.id_column),
        ]:
            ttk.Label(config_frame, text=label).grid(row=row, column=0, sticky="w")
            ttk.Entry(config_frame, textvariable=var, width=60).grid(row=row, column=1, padx=5, pady=2)
            row += 1

        # Export Button
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Export R Template", command=self.export_template).pack(side="left")

        if self.back_callback:
            ttk.Button(button_frame, text="Back to Main Menu", command=self.back_callback).pack(side="right")

    def _select_base_dir(self):
        directory = filedialog.askdirectory(title="Select Base Directory")
        if directory:
            self.base_dir.set(directory)

    def _select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)

    def export_template(self):
        config = {
            'base_dir': self.base_dir.get(),
            'bedfile_path': self.bedfile_path.get(),
            'genome_assembly': self.genome_assembly.get(),
            'min_coverage': self.min_coverage.get(),
            'max_coverage_percentile': self.max_coverage_percentile.get(),
            'sd_cutoff': self.sd_cutoff.get(),
            'tile_win_size': self.tile_win_size.get(),
            'tile_step_size': self.tile_step_size.get(),
            'sample_group_recode': self.sample_group_recode.get(),
            'group_column': self.group_column.get(),
            'file_column': self.file_column.get(),
            'id_column': self.id_column.get()
        }
        export_methylkit_template(config)
