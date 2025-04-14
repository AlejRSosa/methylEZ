import os
import profile
import tkinter as tk
import tkinter.ttk as ttk # theme aesthetic widget
from tkinter import messagebox

from click import option
from methylEZ.command_generator import generate_samplesheet, generate_command
from methylEZ.utils import copy_command_to_clipboard, select_directory
from methylEZ.file_manager import add_files, clear_selected_files, clear_all_files, move_up, move_down
from navigation import Navigation

# The section corresponding to the methylseq preparation option inherits from Navigation
# the constructor of Navigation is called to create the back button
# parent is the container where this particular frame is located
# the back_callback call creates the back button 

class MethylSeqGUI(Navigation):
    def __init__(self, parent, controller, back_callback=None):
        # Call Navigation constructor to create the back button (if back_callback is provided)
        super().__init__(parent, back_callback=back_callback)

        # the top level controller is the App class defined in main.py
        # this stores a reference to that class, and with this you can bind events to the main window
        self.controller = controller
        # root refers to the main Tk window, so we are referring to the main window
        self.root = controller  
        
        # Bind keys to the main window 
        self.controller.bind("<Shift-KeyPress>", self.shift_press)
        self.controller.bind("<Shift-KeyRelease>", self.shift_release)
      
        try:
            # Initialize variables and states
            self.file_paths = []
            self.aligner = tk.StringVar(value="bismark")
            self.genome = tk.StringVar(value="GRCh37")
            self.profile = tk.StringVar(value="docker")
            self.output_dir = tk.StringVar(value=os.getcwd())
            self.samplesheet_name = tk.StringVar(value="samplesheet.csv")
            self.file_type = {}
            self.sample_names = {}
            
            # Create GUI sections
            self.create_file_selection_frame()
            self.create_mark_as_section()
            self.create_custom_sample_section()
            self.create_pipeline_settings_section()
            self.create_command_generation_section()
            self.create_status_bar()
        except Exception as e:
            messagebox.showerror("Initialization Error", f"An error occurred while initializing the GUI: {e}")

    def shift_press(self, event):
        self.is_shift_pressed = True

    def shift_release(self, event):
        self.is_shift_pressed = False

    def update_status_bar(self, message):
        """Update the status bar with the description of each button."""
        self.status_bar.config(text=message)
    
    def create_file_selection_frame(self):
        try:
            self.file_frame = ttk.Frame(self)
            self.file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.listbox_and_buttons_frame = ttk.Frame(self.file_frame)
            self.listbox_and_buttons_frame.pack(fill=tk.BOTH, expand=True)

            # Listbox for file paths
            self.file_listbox = tk.Listbox(self.listbox_and_buttons_frame, height=12, selectmode=tk.MULTIPLE)
            self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

            # Buttons for file actions
            self.button_frame = ttk.Frame(self.listbox_and_buttons_frame)
            self.button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

            self.add_file_button = ttk.Button(self.button_frame, text="Add FASTQ Files", command=lambda: add_files(self), width=20)
            self.add_file_button.pack(pady=5)
            self.add_file_button.bind("<Enter>", lambda e: self.set_status("Add FASTQ files."))
            self.add_file_button.bind("<Leave>", lambda e: self.set_status(""))

            self.clear_selected_files_button = ttk.Button(self.button_frame, text="Clear Selected Files", command=lambda: clear_selected_files(self), width=20)
            self.clear_selected_files_button.pack(pady=5)
            self.clear_selected_files_button.bind("<Enter>", lambda e: self.set_status("Clear selected FASTQ files."))
            self.clear_selected_files_button.bind("<Leave>", lambda e: self.set_status(""))

            self.clear_all_files_button = ttk.Button(self.button_frame, text="Clear All Files", command=lambda: clear_all_files(self), width=20)
            self.clear_all_files_button.pack(pady=5)
            self.clear_all_files_button.bind("<Enter>", lambda e: self.set_status("Clear all FASTQ files."))
            self.clear_all_files_button.bind("<Leave>", lambda e: self.set_status(""))

            # Reordering buttons
            self.up_button = ttk.Button(self.button_frame, text="Move Up", command=lambda: move_up(self), width=20)
            self.up_button.pack(pady=5)
            self.up_button.bind("<Enter>", lambda e: self.set_status("Move selected file up."))
            self.up_button.bind("<Leave>", lambda e: self.set_status(""))

            self.down_button = ttk.Button(self.button_frame, text="Move Down", command=lambda: move_down(self), width=20)
            self.down_button.pack(pady=5)
            self.down_button.bind("<Enter>", lambda e: self.set_status("Move selected file down."))
            self.down_button.bind("<Leave>", lambda e: self.set_status(""))

            # Bind mouse events
            self.file_listbox.bind("<Button-1>", self.single_click_selection)
            self.selection_start = None

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the file selection frame: {e}")

    def single_click_selection(self, event):
        """Select one file on a normal click, extend selection with Shift,
        or clear the selection if clicking on empty space."""
        index = self.file_listbox.nearest(event.y)
        bbox = self.file_listbox.bbox(index)
        if bbox is None or not (bbox[1] <= event.y <= bbox[1] + bbox[3]):
            self.file_listbox.selection_clear(0, tk.END)
            self.selection_start = None
            return "break"
        
        if (event.state & 0x0001) and (self.selection_start is not None):
            start = min(self.selection_start, index)
            end = max(self.selection_start, index)
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(start, end)
        else:
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(index)
            self.selection_start = index
        
        self.file_listbox.activate(index)
        return "break"

    def create_mark_as_section(self):
        try:
            self.mark_as_frame = ttk.Frame(self)
            self.mark_as_frame.pack(pady=5)

            self.mark_as_label = ttk.Label(self.mark_as_frame, text="Mark as:")
            self.mark_as_label.pack(side=tk.LEFT, padx=5)

            options = ["Select option", "Single-end", "Paired-end", "Neutral"]
            self.mark_menu = tk.StringVar(self, value=options[0])
            self.mark_dropdown = ttk.OptionMenu(self.mark_as_frame, self.mark_menu, *options, command=self.apply_mark)
            self.mark_dropdown.pack(side=tk.LEFT, padx=5)

            self.mark_dropdown.bind("<Enter>", lambda e: self.set_status("Mark the selected files as single-end, paired-end, or neutral."))
            self.mark_dropdown.bind("<Leave>", lambda e: self.set_status(""))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the 'Mark as' section: {e}")
    
    def apply_mark(self, mark_choice):
        try:
            mark_map = {"Single-end": "single", "Paired-end": "paired", "Neutral": "neutral"}
            selected_indices = self.file_listbox.curselection()

            if not selected_indices:
                messagebox.showerror("Error", "No files selected to mark.")
                return

            for index in selected_indices:
                file_path = self.file_listbox.get(index)
                self.file_type[file_path] = mark_map[mark_choice]
                if mark_choice == "Single-end":
                    self.file_listbox.itemconfig(index, {'bg': '#A6E1FF'})
                elif mark_choice == "Paired-end":
                    self.file_listbox.itemconfig(index, {'bg': '#FFEE98'})
                else:
                    self.file_listbox.itemconfig(index, {'bg': 'white'})
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while marking files: {e}")

    def create_custom_sample_section(self):
        try:
            self.sample_name_frame = ttk.Frame(self)
            self.sample_name_frame.pack(pady=5)

            self.sample_name_label = ttk.Label(self.sample_name_frame, text="Enter Custom Sample Name:")
            self.sample_name_label.pack(side=tk.LEFT, padx=5)

            self.sample_name_entry = tk.Entry(self.sample_name_frame)
            self.sample_name_entry.pack(side=tk.LEFT, padx=5)

            self.assign_name_button = ttk.Button(self.sample_name_frame, text="Assign Sample Name", command=self.assign_sample_name)
            self.assign_name_button.pack(side=tk.LEFT, padx=5)
            self.assign_name_button.bind("<Enter>", lambda e: self.set_status("Assign a custom sample name to the selected files."))
            self.assign_name_button.bind("<Leave>", lambda e: self.set_status(""))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the custom sample section: {e}")

    def create_pipeline_settings_section(self):
        try:
            self.settings_frame = ttk.Frame(self)
            self.settings_frame.pack(pady=5)

            aligners = ["Select aligner","bismark", "bismark_hisat", "bwameth"]
            self.aligner = tk.StringVar(value=aligners[0])
            self.aligner_label = ttk.Label(self.settings_frame, text="Select Aligner:")
            self.aligner_label.pack(side=tk.LEFT, padx=5)

            self.aligner_menu = ttk.OptionMenu(self.settings_frame, self.aligner,*aligners)
            self.aligner_menu.pack(side=tk.LEFT, padx=5)
            self.aligner_menu.bind("<Enter>", lambda e: self.set_status("Choose the aligner for the pipeline."))
            self.aligner_menu.bind("<Leave>", lambda e: self.set_status(""))

            profiles = ["Select profile", "docker", "singularity"]
            self.profile = tk.StringVar(value=profiles[0])
            self.profile_label = ttk.Label(self.settings_frame, text="Select Profile:")
            self.profile_label.pack(side=tk.LEFT, padx=5)

            self.profile_menu = ttk.OptionMenu(self.settings_frame, self.profile, *profiles)
            self.profile_menu.pack(side=tk.LEFT, padx=5)
            self.profile_menu.bind("<Enter>", lambda e: self.set_status("Select the execution profile for the pipeline (Docker/Singularity)."))
            self.profile_menu.bind("<Leave>", lambda e: self.set_status(""))

            # Output Directory Selection
            self.output_dir_frame = ttk.Frame(self)
            self.output_dir_frame.pack(pady=5)

            self.output_dir_label = ttk.Label(self.output_dir_frame, text="Output Directory:")
            self.output_dir_label.pack(side=tk.LEFT, padx=5)

            self.output_dir_entry = tk.Entry(self.output_dir_frame, textvariable=self.output_dir, width=50)
            self.output_dir_entry.pack(side=tk.LEFT, padx=5)
            self.output_dir_entry.bind("<Enter>", lambda e: self.set_status("Enter or browse the directory to save outputs."))
            self.output_dir_entry.bind("<Leave>", lambda e: self.set_status(""))

            self.browse_dir_button = ttk.Button(self.output_dir_frame, text="Browse", command=lambda: select_directory(self))
            self.browse_dir_button.pack(side=tk.LEFT, padx=5)
            self.browse_dir_button.bind("<Enter>", lambda e: self.set_status("Browse for the output directory."))
            self.browse_dir_button.bind("<Leave>", lambda e: self.set_status(""))

            # Samplesheet Name
            self.samplesheet_frame = ttk.Frame(self)
            self.samplesheet_frame.pack(pady=5)

            self.samplesheet_label = ttk.Label(self.samplesheet_frame, text="Samplesheet Name:")
            self.samplesheet_label.pack(side=tk.LEFT, padx=5)

            self.samplesheet_entry = tk.Entry(self.samplesheet_frame, textvariable=self.samplesheet_name)
            self.samplesheet_entry.pack(side=tk.LEFT, padx=5)
            self.samplesheet_entry.bind("<Enter>", lambda e: self.set_status("Enter the name for the samplesheet file."))
            self.samplesheet_entry.bind("<Leave>", lambda e: self.set_status(""))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the pipeline settings section: {e}")

    def create_command_generation_section(self):
        try:
            self.command_button_frame = ttk.Frame(self)
            self.command_button_frame.pack(pady=5)

            self.generate_samplesheet_button = ttk.Button(self.command_button_frame, text="Generate Samplesheet", command=lambda: generate_samplesheet(self))
            self.generate_samplesheet_button.pack(side=tk.LEFT, padx=5)
            self.generate_samplesheet_button.bind("<Enter>", lambda e: self.set_status("Generate the samplesheet from the selected files."))
            self.generate_samplesheet_button.bind("<Leave>", lambda e: self.set_status(""))

            self.generate_command_button = ttk.Button(self.command_button_frame, text="Generate Command", command=lambda: generate_command(self))
            self.generate_command_button.pack(side=tk.LEFT, padx=5)
            self.generate_command_button.bind("<Enter>", lambda e: self.set_status("Generate the Nextflow command for running the pipeline."))
            self.generate_command_button.bind("<Leave>", lambda e: self.set_status(""))

            self.generate_both_button = ttk.Button(self.command_button_frame, text="Generate Both", command=lambda: [generate_samplesheet(self), generate_command(self)])
            self.generate_both_button.pack(side=tk.LEFT, padx=5)
            self.generate_both_button.bind("<Enter>", lambda e: self.set_status("Generate both the samplesheet and the command."))
            self.generate_both_button.bind("<Leave>", lambda e: self.set_status(""))

            # Generated command and copy button
            self.command_text_frame = ttk.Frame(self)
            self.command_text_frame.pack(pady=5)

            self.command_label = ttk.Label(self.command_text_frame, text="Generated Command:")
            self.command_label.pack(pady=5)

            self.command_text = tk.Text(self.command_text_frame, height=4, width=100)
            self.command_text.pack(side=tk.LEFT, padx=5)

            self.copy_command_button = ttk.Button(self.command_text_frame, text="Copy Command", command=lambda: copy_command_to_clipboard(self))
            self.copy_command_button.pack(side=tk.LEFT, padx=5)
            self.copy_command_button.bind("<Enter>", lambda e: self.set_status("Copy the generated Nextflow command to the clipboard."))
            self.copy_command_button.bind("<Leave>", lambda e: self.set_status(""))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the command generation section: {e}")

    def assign_sample_name(self):
        try:
            selected_indices = self.file_listbox.curselection()
            custom_name = self.sample_name_entry.get()
            if not custom_name:
                messagebox.showerror("Error", "Please enter a sample name.")
                return

            if not selected_indices:
                messagebox.showerror("Error", "Please select files to assign the sample name to.")
                return

            for index in selected_indices:
                file_path = self.file_listbox.get(index)
                self.sample_names[file_path] = custom_name

            self.sample_name_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while assigning the sample name: {e}")

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
