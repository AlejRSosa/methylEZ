import os
import tkinter as tk
from tkinter import ttk
from .hsmetrics_gui import HSMetricsGUI
from .hsmetrics_preparation import PicardPreparationFrame
from .navigation import Navigation

class MainPicardGUI(Navigation):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent, back_callback=back_callback)
        self.controller = controller
        self.root=controller

        # Adding an output directory shared state between two panels
        self.output_dir = tk.StringVar(value=os.getcwd())
             
        # Create a horizontal container for the two sections.
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left pane with a border.
        left_frame = ttk.Frame(main_container, borderwidth=2, relief="groove")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        prep_frame = PicardPreparationFrame(left_frame, controller, self.output_dir)
        prep_frame.pack(fill=tk.BOTH, expand=True)
        
        # Separator between the two panes.
        #separator = ttk.Separator(main_container, orient=tk.VERTICAL)
        #separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Right pane with a border.
        right_frame = ttk.Frame(main_container, borderwidth=2, relief="groove")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        hsmetrics_frame = HSMetricsGUI(right_frame, controller, self.output_dir)
        hsmetrics_frame.pack(fill=tk.BOTH, expand=True)




