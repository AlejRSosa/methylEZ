'''
MethylEZ - A GUI for methylation sequencing workflow
Author: Alejandra Rodriguez-Sosa
Date: 06-02-2025

'''
# Using the container approach, we hold all GUI pages for each of the options in the main menu.
# Each page is instantiated just once, stored in a dictionary and the user navigates them thansks to 
# tkraise() method, avoiding duplicate widget and loss of efficiency by generation / destroying widgets dynamically.

import tkinter as tk
#from matplotlib import scale
try:
    import tkinter as tk
except ImportError:
    print("\nError: Tkinter is not installed!\n")
    print("Please install Tkinter manually:\n")
    print("🔹 On Ubuntu/Debian: sudo apt install python3-tk")
    print("🔹 On Fedora: sudo dnf install python3-tkinter")
    print("🔹 On Arch Linux: sudo pacman -S tk")
    print("🔹 On Windows/macOS: Reinstall Python with the 'tcl/tk' option enabled.")
    exit(1)
from tkinter import ttk # import aesthetic ttk module for buttons, labels, etc.
from ttkthemes import ThemedStyle  # import ttkthemes for more aesthetic stuff (I tried to make it look pretty, don't judge me)
# Import all GUI classes
from methylEZ.gui import MethylSeqGUI  # methylseq preparation
#from hsmetrics_gui import HSMetricsGUI  # CollectHsMetrics 
from methylEZ.hsmetrics_main_gui import MainPicardGUI  # CollectHsMetrics GUI
#from methylEZ.dmr_gui import DMRGUI  # New GUI for downstream analysis (to be implemented)

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent)
        self.controller=controller
        self.back_callback = back_callback

        #self.logo = tk.PhotoImage(file=r"C:\Users\aroso\Documents\GitHub\methylEZ\methylEZ\METHYLEZ_LOGO3.png").subsample(2,2)
        #logo_label = ttk.Label(self, image=self.logo)
        #logo_label.pack(pady=10)

        #ttk.Label(self, text="Welcome to MethylEZ", font=("Arial", 20)).pack(pady=10)
        ttk.Label(self, text="Select an option to continue:", font=("Arial", 16)).pack(pady=5)
        ttk.Button(self, text="🧬 Methylseq Preparation",
                  command=lambda: controller.show_frame(MethylSeqGUI), width=30).pack(pady=5)
        ttk.Button(self, text="📈 Collect HsMetrics",
                  command=lambda: controller.show_frame(MainPicardGUI), width=30).pack(pady=5)
        ttk.Button(self, text="🖥️Downstream Analysis",
                  command=lambda: controller.show_frame(DMRAnalysisGUI), width=30).pack(pady=5)
        ttk.Button(self,text="📊 Visualization",
                   command=lambda: controller.show_frame(VisualizationGUI),width=30).pack(pady=5)
        ttk.Button(self, text="❌ Exit", command=controller.destroy, width=30).pack(pady=20)


class DMRAnalysisGUI(ttk.Frame):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.back_callback = back_callback
        ttk.Label(self, text="DMR Analysis", font=("Arial", 18)).pack(pady=10)
        ttk.Button(self, text="⬅ Back to Main Menu",
                  command=lambda: controller.show_frame(MainMenu), width=30).pack(pady=10)

class VisualizationGUI(ttk.Frame):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.back_callback = back_callback
        ttk.Label(self, text="Visualization", font=("Arial", 18)).pack(pady=10)
        ttk.Button(self, text="⬅ Back to Main Menu",
                  command=lambda: controller.show_frame(MainMenu), width=30).pack(pady=10)

# The main application class or App is the main window which has one container (tk.Frame) that holds all pages.
# MainMenu, MethlySeqGUI, HSMetricsGUI, and DMRAnalysisGUI are pages that will be children of the container.
# By instantiating all pages once and storing them in a dictionary, we avoid generating a new instance when the user
# navigates, avoiding dynamic generation and destruction of widgets.

# Using tkraise() we just bring the frame of choice to the front.

# The dictionary storage allows managing the pages. Each state is maintained when the user switches and 
# prevents duplication of widget instances (which was happening before).

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(True, True)
        self.title("MethylEZ")
        # Set the style of the GUI 
        style = ThemedStyle(self)
        #print(style.theme_names())
        style.set_theme('radiance') #equilux is a dark theme, radiance is the favourite for now, aquativo is blue and not bad
        # Set a default window geometry
        # self.geometry("800x600")
        # Create a container that will hold all frames (layout managers)
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Instantiate all pages once and store them in a dictionary.
        self.frames = {}
        for F in (MainMenu, MethylSeqGUI, MainPicardGUI, DMRAnalysisGUI, VisualizationGUI):
            frame = F(container, self, back_callback=lambda: self.show_frame(MainMenu))

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            # For pages that support navigation (like MethylSeqGUI), pass a back_callback.
            #if F == MethylSeqGUI:
            #    frame = F(container, self, back_callback=lambda: self.show_frame(MainMenu))
            #else:
            #    frame = F(container, self)
            #self.frames[F] = frame
            # Place all frames in the same location; the one on top will be visible.
            #frame.grid(row=0, column=0, sticky="nsew")
        
        self.update_idletasks()  # Update the window to get the correct size
        self.geometry("")
        self.show_frame(MainMenu)
    
    # this method is in charge of taking the selected frame to the front, without destroying
    # and recreating the others
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        # Adjust geometry based on the frame - to be checked
        #if frame_class != MainMenu:
         #   self.geometry("1300x1000")
        #else:
         #   self.geometry("800x700")
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
