# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:01:29 2024

@author: maxim
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import function_smoothing as fs

# Function: Calculate and set the window to be centered
def center_window(window):
    window.update_idletasks()    # Update window size and layout
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width/2) - (width/0.4))
    y = int((screen_height/2) - (height/0.5))
    window.geometry(f'+{x}+{y}')
    
class DataSmoothingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BD Outline Smoothing")

        # Create frames
        self.left_frame = tk.Frame(self.root, padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.right_frame = tk.Frame(self.root, padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Input data area
        tk.Label(self.left_frame, text="Data (Tab-separated TXT format):").grid(row=0, column=0, columnspan=2, sticky='w')
        self.data_text = tk.Text(self.left_frame, width=50, height=40)
        self.data_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(self.left_frame, text="Fraction:").grid(row=2, column=0, sticky='w')
        self.frac_entry = tk.Entry(self.left_frame)
        self.frac_entry.insert(0, '0.05')  # Default value
        self.frac_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(self.left_frame, text="Output File Name:").grid(row=3, column=0, sticky='w')
        self.output_filename_entry = tk.Entry(self.left_frame)
        self.output_filename_entry.insert(0, 'smoothed_data')  # Default value
        self.output_filename_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(self.left_frame, text="Output File Address:").grid(row=4, column=0, sticky='w')
        self.output_address_entry = tk.Entry(self.left_frame)
        self.output_address_entry.insert(0, '.')
        self.output_address_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        self.browse_button = tk.Button(self.left_frame, text="...", command=self.browse_folder)
        self.browse_button.grid(row=4, column=2, padx=5, pady=5)

        # Button to execute program
        self.execute_button = tk.Button(self.left_frame, text="Execute", command=self.execute_program, width=20, height=2)
        self.execute_button.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Last row: Message
        self.message_label = tk.Label(self.left_frame, text="", fg="green")
        self.message_label.grid(row=6, column=0, columnspan=3, pady=10)

        # Create matplotlib figures
        self.fig1, self.ax1 = plt.subplots(figsize=(5, 4))
        self.fig2, self.ax2 = plt.subplots(figsize=(5, 4))

        # Create canvas for the figures
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.right_frame)
        self.canvas1_widget = self.canvas1.get_tk_widget()
        self.canvas1_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.right_frame)
        self.canvas2_widget = self.canvas2.get_tk_widget()
        self.canvas2_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_address_entry.delete(0, tk.END)
            self.output_address_entry.insert(0, folder_selected)

    def execute_program(self):
        try:
            # Read data from text box
            data_str = self.data_text.get("1.0", tk.END).strip()
            data_lines = data_str.splitlines()
            data = np.array([line.split('\t') for line in data_lines], dtype=float)

            # Read frac
            frac = float(self.frac_entry.get().strip())

            # Read output file name and address
            output_filename = self.output_filename_entry.get().strip()
            output_address = self.output_address_entry.get().strip()

            # Apply the smoothing function
            original_data, smoothed_data, polar_data, smoothed_polar_data = fs.smoothing(data, frac)
            
            smoothed_polar_data = smoothed_polar_data[
                (smoothed_polar_data[:, 0] >= -180) & 
                (smoothed_polar_data[:, 0] <= 180)]

            # Plot Cartesian data
            self.ax1.clear()
            self.ax1.plot(original_data[:, 0], original_data[:, 1], label='Original Data', color='blue', linestyle='-', linewidth=3, alpha=0.7)
            self.ax1.plot(smoothed_data[:, 0], smoothed_data[:, 1], label='Smoothed Data', color='red', linestyle='-', linewidth=3, alpha=0.7)
            self.ax1.set_title('Comparison of Original and Smoothed Data')
            self.ax1.set_xlabel('X Values')
            self.ax1.set_ylabel('Y Values')
            self.ax1.legend()

            # Plot polar data
            self.ax2.clear()
            self.ax2.plot(polar_data[:, 0], polar_data[:, 1], label='Original Polar Data', color='blue', linestyle='-', linewidth=3, alpha=0.7)
            self.ax2.plot(smoothed_polar_data[:, 0], smoothed_polar_data[:, 1], label='Smoothed Polar Data', color='red', linestyle='-', linewidth=3, alpha=0.7)
            self.ax2.set_title('Comparison of Original and Smoothed Polar Data')
            self.ax2.set_xlabel('θ (Degrees)')
            self.ax2.set_ylabel('Radius')
            self.ax2.legend()

            # Draw on canvas
            self.canvas1.draw()
            self.canvas2.draw()

            # Save smoothed data
            np.savetxt(f"{output_address}/{output_filename}.txt", smoothed_data, delimiter='\t', comments='')

            # messagebox.showinfo("Success", f'Data processed and saved successfully to {output_address}/{output_filename}.txt')
            self.message_label.config(text=f'Data processed and saved successfully at:\n {output_address}/{output_filename}.txt')
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    # Ensure the window is centered
    center_window(root)
    app = DataSmoothingApp(root)
    root.mainloop()
