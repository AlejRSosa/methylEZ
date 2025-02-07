import tkinter as tk

def return_to_main(current_window):
    """Destroy the current window and go back to the Main Menu."""
    from methylEZ.main import MainMenuGUI  # Import inside function to avoid circular dependency

    # Destroy the current window but keep the main Tk instance running
    if current_window:
        current_window.destroy()

    # Instead of creating a new Tk instance, reuse the existing one
    new_root = tk.Tk()  # Ensure a single Tk instance
    app = MainMenuGUI(new_root)
    new_root.mainloop()  # Start the mainloop again
