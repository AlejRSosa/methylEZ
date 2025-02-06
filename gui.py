import os
import tkinter as tk
from tkinter import messagebox
from command_generator import generate_samplesheet, generate_command
from utils import copy_command_to_clipboard, select_directory
from file_manager import add_files, clear_selected_files, clear_all_files, move_up, move_down
from navigation import return_to_main #importing the return function to generate a "back to main menu button"

class MethylSeqGUI:
    def __init__(self, root):
        """
        Initializes the MethylEZ GUI application.
        Args:
            root (tk.Tk): The root window of the Tkinter application.
        Attributes:
            root (tk.Tk): The root window of the Tkinter application.
            file_paths (list): List to store selected file paths.
            aligner (tk.StringVar): Variable to store the selected aligner (default is "bismark").
            genome (tk.StringVar): Variable to store the selected genome (default is "GRCh37").
            profile (tk.StringVar): Variable to store the selected profile (default is "docker").
            output_dir (tk.StringVar): Variable to store the output directory (default is the current working directory).
            samplesheet_name (tk.StringVar): Variable to store the name of the samplesheet (default is "samplesheet.csv").
            file_type (dict): Dictionary to store file types.
            sample_names (dict): Dictionary to store sample names.
        Methods:
            create_file_selection_frame(): Creates the file selection section of the GUI.
            create_mark_as_section(): Creates the "Mark As" section of the GUI.
            create_custom_sample_section(): Creates the custom sample section of the GUI.
            create_pipeline_settings_section(): Creates the pipeline settings section of the GUI.
            create_command_generation_section(): Creates the command generation section of the GUI.
            create_status_bar(): Creates the status bar of the GUI.
        """
        self.root = root
        self.root.title("MethylSeq Pipeline GUI")

        # Track shift key press
        self.is_shift_pressed = False
        self.selection_start = None

        # Bind keys
        self.root.bind("<Shift-KeyPress>", self.shift_press)
        self.root.bind("<Shift-KeyRelease>", self.shift_release)

        # Initial window size
        self.root.geometry("1300x850")  # Adjusted to fit everything
        self.back_button=tk.Button(self.root, text="⬅ Back to Main menu", command=lambda:return_to_main(self.root))
        self.back_button.pack(pady=10)
        try:
            # Store selected files and pipeline settings
            self.file_paths = []
            self.aligner = tk.StringVar(value="bismark")
            self.genome = tk.StringVar(value="GRCh37")
            self.profile = tk.StringVar(value="docker")
            self.output_dir = tk.StringVar(value=os.getcwd())
            self.samplesheet_name = tk.StringVar(value="samplesheet.csv")

            # Store file type and sample names
            self.file_type = {}
            self.sample_names = {}

            # Create sections of the GUI
            self.create_file_selection_frame()
            self.create_mark_as_section()
            self.create_custom_sample_section()
            self.create_pipeline_settings_section()
            self.create_command_generation_section()

            # Create status bar
            self.create_status_bar()
            self.file_listbox.bind("<Button-1>", self.single_click_selection)

        except Exception as e:
            messagebox.showerror("Initialization Error", f"An error occurred while initializing the GUI: {e}")

    def shift_press(self, event):
        self.is_shift_pressed = True

    def shift_release(self, event):
        self.is_shift_pressed = False

    def update_status_bar(self, message):
        """Update the status bar with the provided message."""
        self.status_bar.config(text=message)
    
    def create_file_selection_frame(self):
        try:
            self.file_frame = tk.Frame(self.root)
            self.file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.listbox_and_buttons_frame = tk.Frame(self.file_frame)
            self.listbox_and_buttons_frame.pack(fill=tk.BOTH, expand=True)

            # Listbox for file paths
            self.file_listbox = tk.Listbox(self.listbox_and_buttons_frame, height=12, selectmode=tk.MULTIPLE)
            self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

            # Buttons for file actions
            self.button_frame = tk.Frame(self.listbox_and_buttons_frame)
            self.button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

            self.add_file_button = tk.Button(self.button_frame, text="Add FASTQ Files", command=lambda: add_files(self), width=20)
            self.add_file_button.pack(pady=5)
            self.add_file_button.bind("<Enter>", lambda e: self.set_status("Add FASTQ files."))
            self.add_file_button.bind("<Leave>", lambda e: self.set_status(""))

            self.clear_selected_files_button = tk.Button(self.button_frame, text="Clear Selected Files", command=lambda: clear_selected_files(self), width=20)
            self.clear_selected_files_button.pack(pady=5)
            self.clear_selected_files_button.bind("<Enter>", lambda e: self.set_status("Clear selected FASTQ files."))
            self.clear_selected_files_button.bind("<Leave>", lambda e: self.set_status(""))

            self.clear_all_files_button = tk.Button(self.button_frame, text="Clear All Files", command=lambda: clear_all_files(self), width=20)
            self.clear_all_files_button.pack(pady=5)
            self.clear_all_files_button.bind("<Enter>", lambda e: self.set_status("Clear all FASTQ files."))
            self.clear_all_files_button.bind("<Leave>", lambda e: self.set_status(""))

            # Reordering buttons
            self.up_button = tk.Button(self.button_frame, text="Move Up", command=lambda: move_up(self), width=20)
            self.up_button.pack(pady=5)
            self.up_button.bind("<Enter>", lambda e: self.set_status("Move selected file up."))
            self.up_button.bind("<Leave>", lambda e: self.set_status(""))

            self.down_button = tk.Button(self.button_frame, text="Move Down", command=lambda: move_down(self), width=20)
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
        # Determine the index of the nearest item to the click
        index = self.file_listbox.nearest(event.y)
        
        # Get the bounding box of that item. bbox returns (x, y, width, height) if the item is visible.
        bbox = self.file_listbox.bbox(index)
        
        # If there's no bbox or the click's y-coordinate is outside the item's bbox,
        # assume the click was in an empty area.
        if bbox is None or not (bbox[1] <= event.y <= bbox[1] + bbox[3]):
            self.file_listbox.selection_clear(0, tk.END)
            self.selection_start = None
            return "break"
        
        # Check if Shift was held down during the click.
        # event.state is a bitmask. For Shift, we check bit 0x0001.
        if (event.state & 0x0001) and (self.selection_start is not None):
            # Determine the range between the anchor (selection_start) and this index.
            start = min(self.selection_start, index)
            end = max(self.selection_start, index)
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(start, end)
        else:
            # A normal click: clear previous selections and select only the clicked item.
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(index)
            self.selection_start = index  # Set the anchor for future shift-clicks
        
        self.file_listbox.activate(index)
        return "break"

    def create_mark_as_section(self):
        try:
            self.mark_as_frame = tk.Frame(self.root)
            self.mark_as_frame.pack(pady=5)

            self.mark_as_label = tk.Label(self.mark_as_frame, text="Mark as:")
            self.mark_as_label.pack(side=tk.LEFT, padx=5)

            self.mark_menu = tk.StringVar(self.root)
            self.mark_menu.set("Single-end")  
            self.mark_dropdown = tk.OptionMenu(self.mark_as_frame, self.mark_menu, "Single-end", "Paired-end", "Neutral", command=self.apply_mark)
            self.mark_dropdown.pack(side=tk.LEFT, padx=5)

            self.mark_dropdown.bind("<Enter>", lambda e: self.set_status("Mark the selected files as single-end, paired-end, or neutral."))
            self.mark_dropdown.bind("<Leave>", lambda e: self.set_status(""))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the 'Mark as' section: {e}")
    
    def apply_mark(self, mark_choice):
        """Apply a mark (single-end, paired-end, or neutral) to selected files."""
        try:
            # Mapping of user choices to internal states
            mark_map = {"Single-end": "single", "Paired-end": "paired", "Neutral": "neutral"}
            selected_indices = self.file_listbox.curselection()  # Get all selected files

            if not selected_indices:
                # Handle no selection case
                messagebox.showerror("Error", "No files selected to mark.")
                return

            # Iterate through all selected files and apply the mark
            for index in selected_indices:
                file_path = self.file_listbox.get(index)  # Retrieve the file path
                self.file_type[file_path] = mark_map[mark_choice]  # Update internal state

                # Update the file's background color for visual feedback
                if mark_choice == "Single-end":
                    self.file_listbox.itemconfig(index, {'bg': '#A6E1FF'})  # Blue for single-end
                elif mark_choice == "Paired-end":
                    self.file_listbox.itemconfig(index, {'bg': '#FFEE98'})  # Yellow for paired-end
                else:
                    self.file_listbox.itemconfig(index, {'bg': 'white'})  # Default for neutral
        except Exception as e:
            # Show an error message for unexpected exceptions
            messagebox.showerror("Error", f"An error occurred while marking files: {e}")





    def create_custom_sample_section(self):
        try:
            self.sample_name_frame = tk.Frame(self.root)
            self.sample_name_frame.pack(pady=5)

            self.sample_name_label = tk.Label(self.sample_name_frame, text="Enter Custom Sample Name:")
            self.sample_name_label.pack(side=tk.LEFT, padx=5)

            self.sample_name_entry = tk.Entry(self.sample_name_frame)
            self.sample_name_entry.pack(side=tk.LEFT, padx=5)

            self.assign_name_button = tk.Button(self.sample_name_frame, text="Assign Sample Name", command=self.assign_sample_name)
            self.assign_name_button.pack(side=tk.LEFT, padx=5)
            self.assign_name_button.bind("<Enter>", lambda e: self.set_status("Assign a custom sample name to the selected files."))
            self.assign_name_button.bind("<Leave>", lambda e: self.set_status(""))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the custom sample section: {e}")

    def create_pipeline_settings_section(self):
        try:
            self.settings_frame = tk.Frame(self.root)
            self.settings_frame.pack(pady=5)

            self.aligner_label = tk.Label(self.settings_frame, text="Select Aligner:")
            self.aligner_label.pack(side=tk.LEFT, padx=5)

            self.aligner_menu = tk.OptionMenu(self.settings_frame, self.aligner, "bismark", "bismark_hisat", "bwameth")
            self.aligner_menu.pack(side=tk.LEFT, padx=5)
            self.aligner_menu.bind("<Enter>", lambda e: self.set_status("Choose the aligner for the pipeline."))
            self.aligner_menu.bind("<Leave>", lambda e: self.set_status(""))

            self.profile_label = tk.Label(self.settings_frame, text="Select Profile:")
            self.profile_label.pack(side=tk.LEFT, padx=5)

            self.profile_menu = tk.OptionMenu(self.settings_frame, self.profile, "docker", "singularity")
            self.profile_menu.pack(side=tk.LEFT, padx=5)
            self.profile_menu.bind("<Enter>", lambda e: self.set_status("Select the execution profile for the pipeline (Docker/Singularity)."))
            self.profile_menu.bind("<Leave>", lambda e: self.set_status(""))

            # Output Directory Selection (below aligner and profile)
            self.output_dir_frame = tk.Frame(self.root)
            self.output_dir_frame.pack(pady=5)

            self.output_dir_label = tk.Label(self.output_dir_frame, text="Output Directory:")
            self.output_dir_label.pack(side=tk.LEFT, padx=5)

            self.output_dir_entry = tk.Entry(self.output_dir_frame, textvariable=self.output_dir, width=50)
            self.output_dir_entry.pack(side=tk.LEFT, padx=5)
            self.output_dir_entry.bind("<Enter>", lambda e: self.set_status("Enter or browse the directory to save outputs."))
            self.output_dir_entry.bind("<Leave>", lambda e: self.set_status(""))

            self.browse_dir_button = tk.Button(self.output_dir_frame, text="Browse", command=lambda: select_directory(self))
            self.browse_dir_button.pack(side=tk.LEFT, padx=5)
            self.browse_dir_button.bind("<Enter>", lambda e: self.set_status("Browse for the output directory."))
            self.browse_dir_button.bind("<Leave>", lambda e: self.set_status(""))

            # Samplesheet Name (below output directory)
            self.samplesheet_frame = tk.Frame(self.root)
            self.samplesheet_frame.pack(pady=5)

            self.samplesheet_label = tk.Label(self.samplesheet_frame, text="Samplesheet Name:")
            self.samplesheet_label.pack(side=tk.LEFT, padx=5)

            self.samplesheet_entry = tk.Entry(self.samplesheet_frame, textvariable=self.samplesheet_name)
            self.samplesheet_entry.pack(side=tk.LEFT, padx=5)
            self.samplesheet_entry.bind("<Enter>", lambda e: self.set_status("Enter the name for the samplesheet file."))
            self.samplesheet_entry.bind("<Leave>", lambda e: self.set_status(""))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the pipeline settings section: {e}")

    def create_command_generation_section(self):
        try:
            self.command_button_frame = tk.Frame(self.root)
            self.command_button_frame.pack(pady=5)

            self.generate_samplesheet_button = tk.Button(self.command_button_frame, text="Generate Samplesheet", command=lambda: generate_samplesheet(self))
            self.generate_samplesheet_button.pack(side=tk.LEFT, padx=5)
            self.generate_samplesheet_button.bind("<Enter>", lambda e: self.set_status("Generate the samplesheet from the selected files."))
            self.generate_samplesheet_button.bind("<Leave>", lambda e: self.set_status(""))

            self.generate_command_button = tk.Button(self.command_button_frame, text="Generate Command", command=lambda: generate_command(self))
            self.generate_command_button.pack(side=tk.LEFT, padx=5)
            self.generate_command_button.bind("<Enter>", lambda e: self.set_status("Generate the Nextflow command for running the pipeline."))
            self.generate_command_button.bind("<Leave>", lambda e: self.set_status(""))

            self.generate_both_button = tk.Button(self.command_button_frame, text="Generate Both", command=lambda: [generate_samplesheet(self), generate_command(self)])
            self.generate_both_button.pack(side=tk.LEFT, padx=5)
            self.generate_both_button.bind("<Enter>", lambda e: self.set_status("Generate both the samplesheet and the command."))
            self.generate_both_button.bind("<Leave>", lambda e: self.set_status(""))

            # Generated command and copy button
            self.command_text_frame = tk.Frame(self.root)
            self.command_text_frame.pack(pady=5)

            self.command_label = tk.Label(self.command_text_frame, text="Generated Command:")
            self.command_label.pack(pady=5)

            self.command_text = tk.Text(self.command_text_frame, height=4, width=100)
            self.command_text.pack(side=tk.LEFT, padx=5)

            self.copy_command_button = tk.Button(self.command_text_frame, text="Copy Command", command=lambda: copy_command_to_clipboard(self))
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
                raise ValueError("No files selected")             
                messagebox.showerror("Error", "Please select files to assign the sample name to.")
                return

            for index in selected_indices:
                file_path = self.file_listbox.get(index)
                self.sample_names[file_path] = custom_name

            self.sample_name_entry.delete(0, tk.END)  # Clear the entry box after assignment
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while assigning the sample name: {e}")

    def create_status_bar(self):
        try:
        # Create the status bar and make it always visible with larger font size
            self.status_bar = tk.Label(self.root, text="Ready",bg="#90E0D3", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Helvetica", 20))
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the status bar: {e}")
            
    def set_status(self, text):
        try:
            self.status_bar.config(text=text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating the status bar: {e}")
            