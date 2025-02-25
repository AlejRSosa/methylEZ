'''
MethylEZ - A GUI for methylation sequencing workflow
Author: Alejandra Rodriguez-Sosa
Date: 06-02-2025

'''
import tkinter as tk
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

from methylEZ.gui import MethylSeqGUI  # Your existing GUI
#from methylEZ.hsmetrics_gui import HSMetricsGUI  # New GUI for CollectHsMetrics (to be implemented)
#from methylEZ.dmr_gui import DMRGUI  # New GUI for downstream analysis (to be implemented)
from methylEZ.navigation import return_to_main

class MainMenuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MethylEZ - Main Menu")
        self.root.geometry("400x300")  # Adjust window size

        tk.Label(self.root, text="Welcome to MethylEZ", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text="Select a workflow to continue:", font=("Arial", 16)).pack(pady=5)

        # Buttons for different workflows
        tk.Button(self.root, text="🧬 Methylseq Preparation", command=self.launch_methylseq, width=30).pack(pady=5)
        #tk.Button(self.root, text="📊 Collect HsMetrics", command=self.launch_hsmetrics, width=30).pack(pady=5)
        #tk.Button(self.root, text="🔬 Downstream DMR Analysis", command=self.launch_dmr, width=30).pack(pady=5)

        tk.Button(self.root, text="❌ Exit", command=root.quit, width=30).pack(pady=20)

    def launch_methylseq(self):
        """Launch the existing MethylSeq preparation GUI."""
        self.root.destroy()  # Close main menu
        root = tk.Tk()
        app = MethylSeqGUI(root)
        root.mainloop()

"""     def launch_hsmetrics(self):
        self.root.destroy()
        root = tk.Tk()
        app = HSMetricsGUI(root)  # Assuming this is a separate Tkinter-based GUI
        root.mainloop()

    def launch_dmr(self):
        self.root.destroy()
        root = tk.Tk()
        app = DMRGUI(root)  # Assuming this is a separate Tkinter-based GUI
        root.mainloop() """

def launch_submenu(sub_gui_class):
    """Launch any sub-GUI with a back-to-main-menu button."""
    root = tk.Tk()
    app = sub_gui_class(root)  

    # Add "Back to Main Menu" button
    tk.Button(root, text="⬅ Back to Main Menu", command=lambda: return_to_main(root)).pack(pady=10)

    root.mainloop()

def start_gui():
    """Launch the main GUI."""
    root = tk.Tk()
    app = MainMenuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenuGUI(root)
    root.mainloop()
