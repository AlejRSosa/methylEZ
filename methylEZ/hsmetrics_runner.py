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
        
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, line)
            self.output_text.yview(tk.END)
            self.output_text.config(state=tk.DISABLED)

        process.wait()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "\n Completed \n")
        self.output_text.config(state=tk.DISABLED)

    messagebox.showinfo("Completed", "Picard CollectHsMetrics has finished running.")
    self.output_text.config(state=tk.NORMAL)
    self.output_text.insert(tk.END, "\nProcess finalised.\n")
    self.output_text.config(state=tk.DISABLED)