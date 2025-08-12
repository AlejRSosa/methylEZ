##UPDATE: april 2025 - removed the functionality of hsmetrics_runner altogether from the hsmetrics_gui to focus on template generation

import subprocess
import tkinter as tk
from tkinter import messagebox

def run_picard_hsmetrics(self):
    """Executes Picard CollectHsMetrics and captures real-time output."""
    command = self.command_text.get("1.0", tk.END).strip()
    if not command:
        messagebox.showerror("Error", "No command generated. Please generate it first.")
        return

    commands= command.splitlines()

    self.output_text.config(state=tk.NORMAL)
    self.output_text.delete(1.0, tk.END)
    self.output_text.insert(tk.END, "Running Picard CollectHsMetrics...\n")
    self.output_text.config(state=tk.DISABLED)

    # Now we loop over each command
    for cmd in commands:
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"\nRunning: {cmd}\n")
        self.output_text.config(state=tk.DISABLED)
        
        # Run the current command, merge stderr into stdout to avoid blocking if stderr fills
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding="utf-8",
            errors="replace",
        )

        # Stream output line-by-line (stdout can be Optional for type checkers)
        if process.stdout:
            for line in process.stdout:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, line)
                self.output_text.yview(tk.END)
                self.output_text.config(state=tk.DISABLED)

        process.wait()
        if process.returncode != 0:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"\nCommand exited with code {process.returncode}\n")
            self.output_text.config(state=tk.DISABLED)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "\n Completed \n")
        self.output_text.config(state=tk.DISABLED)

    messagebox.showinfo("Completed", "Picard CollectHsMetrics has finished running.")
    self.output_text.config(state=tk.NORMAL)
    self.output_text.insert(tk.END, "\nProcess finalised.\n")
    self.output_text.config(state=tk.DISABLED)