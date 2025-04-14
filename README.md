# methylEZ
"A user-friendly GUI to streamline the preparation of whole-genome bisulfite sequencing (WBGS) and reduced representation bisulfite sequencing (RRBS) workflows. Its hybrid approach consist of generating command-line templates that can be either used directly or modified by the users at their convenience."

Installation Instructions (Linux, macOS, Windows)

Open your terminal (or PowerShell on Windows) and run:

1.Install the package directly from GitHub: 

pip install git+https://github.com/AlejRSosa/methylEZ.git

2. Launch the application:

methylEZ

⚠ Tkinter is required to run MethylEZ! ⚠

If you get `ModuleNotFoundError: No module named 'tkinter'`, install it manually:


🔹 On Ubuntu/Debian: sudo apt install python3-tk
🔹 On Fedora: sudo dnf install python3-tkinter
🔹 On Arch Linux: sudo pacman -S tk
🔹 On Windows/macOS: Reinstall Python with the "tcl/tk" option enabled.

