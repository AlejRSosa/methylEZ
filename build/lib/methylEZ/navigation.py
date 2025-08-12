# Navigation class is a subclass of tk.Frame which acts as a base class for the GUIs
# We originally had them inherit from tk.Frame, but the sub-menu structure was not working
# This class is instantiated and allows the back button to be displayed on any page
# The back button is only shown if a callback function is provided

import tkinter as tk
import tkinter.ttk as ttk

class Navigation(ttk.Frame):
    def __init__(self, master, back_callback=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        # If a back_callback is provided, create a back button.
        if back_callback:
            ttk.Button(self, text="<-- Back to Main menu", command=back_callback).pack(pady=10)