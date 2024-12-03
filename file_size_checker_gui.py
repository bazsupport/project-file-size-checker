import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import sys

class FileSizeCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Project File Size Checker")
        self.root.geometry("900x700")  # Larger default size
        
        # Add proper window close handling
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        style = ttk.Style()
        style.configure('Main.TFrame', padding=10)  # Reduced padding
        style.configure('Settings.TLabelframe', padding=10)  # Reduced padding
        style.configure('Results.TLabel', font=('Arial', 10, 'bold'))
        
        # Configure root grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, style='Main.TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # Reduced padding
        
        # Configure main frame grid
        for i in range(7):  # Adjust based on number of rows
            main_frame.grid_rowconfigure(i, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Create centered content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(content_frame, text="Project File Size Checker", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))  # Reduced padding
        
        # Folder selection
        self.folder_path = tk.StringVar()
        folder_frame = ttk.Frame(content_frame)
        folder_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 8))  # Reduced padding
        folder_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(folder_frame, text="Folder:", font=('Arial', 10)).grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path)
        self.folder_entry.grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=(5, 0))
        
        # Size limit input
        size_frame = ttk.Frame(content_frame)
        size_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=8)  # Reduced padding
        size_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(size_frame, text="Size Limit (MB):", font=('Arial', 10)).grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.size_limit = tk.StringVar(value="50")
        size_entry = ttk.Entry(size_frame, textvariable=self.size_limit, width=10)
        size_entry.grid(row=0, column=1, sticky="w")
        
        # Checkbox settings
        settings_frame = ttk.LabelFrame(content_frame, text="Search Settings", style='Settings.TLabelframe')
        settings_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)  # Reduced padding
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_columnconfigure(1, weight=1)
        
        self.include_git = tk.BooleanVar(value=False)
        self.include_godot = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(settings_frame, text="Include .git folder", 
                       variable=self.include_git).grid(row=0, column=0, sticky="w", padx=20, pady=5)
        ttk.Checkbutton(settings_frame, text="Include .godot folder", 
                       variable=self.include_godot).grid(row=0, column=1, sticky="w", padx=20, pady=5)
        
        # Add custom folder exclusions section
        exclude_frame = ttk.LabelFrame(settings_frame, text="Custom Folder Exclusions")
        exclude_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(8, 4))  # Reduced padding
        exclude_frame.grid_columnconfigure(0, weight=1)
        
        # Add help text
        help_text = "Enter folder names to exclude (one per line).\nThese folders will be skipped during scanning."
        ttk.Label(exclude_frame, text=help_text, font=('Arial', 9)).grid(row=0, column=0, sticky="w", padx=5, pady=(5,0))
        
        # Create text widget for exclusions with scrollbar
        self.exclude_text = tk.Text(exclude_frame, wrap=tk.WORD, height=3, width=40, font=('Consolas', 10))  # Reduced height
        exclude_scrollbar = ttk.Scrollbar(exclude_frame, orient=tk.VERTICAL, command=self.exclude_text.yview)
        self.exclude_text.configure(yscrollcommand=exclude_scrollbar.set)
        
        self.exclude_text.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        exclude_scrollbar.grid(row=1, column=1, sticky="ns", pady=5)
        
        # Scan button
        scan_button = tk.Button(content_frame, text="Scan Files", 
                       command=self.scan_files,
                       font=('Arial', 10, 'bold'),
                       bg='#0066cc',
                       fg='white',
                       activebackground='#005299',
                       activeforeground='white')
        scan_button.grid(row=4, column=0, columnspan=3, pady=10)  # Reduced padding
        
        # Results area
        results_label = ttk.Label(content_frame, text="Files exceeding size limit:", 
                                style='Results.TLabel', anchor="w")
        results_label.grid(row=5, column=0, columnspan=3, sticky="w", pady=(8, 4))  # Reduced padding
        
        # Create frame for results with scrollbar
        results_frame = ttk.Frame(content_frame)
        results_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=(0, 8))  # Reduced padding
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)
        
        # Configure text widget with custom font and colors
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=18,  # Increased height
                                  font=('Consolas', 10), bg='#ffffff')
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Grid the text widget and scrollbar
        self.results_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Tag configuration for clickable links
        self.results_text.tag_configure("link", foreground="#0066cc", underline=1)
        self.results_text.tag_bind("link", "<Button-1>", self.open_file_location)
        self.results_text.tag_bind("link", "<Enter>", lambda e: self.results_text.configure(cursor="hand2"))
        self.results_text.tag_bind("link", "<Leave>", lambda e: self.results_text.configure(cursor=""))

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def scan_files(self):
        folder_path = self.folder_path.get()
        try:
            size_limit = float(self.size_limit.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for size limit")
            return

        if not folder_path:
            messagebox.showerror("Error", "Please select a folder")
            return

        self.results_text.delete(1.0, tk.END)
        large_files = self.find_large_files(folder_path, size_limit)

        if not large_files:
            self.results_text.insert(tk.END, f"\nNo files found exceeding {size_limit} MB\n")
        else:
            self.results_text.insert(tk.END, f"\nFound {len(large_files)} files exceeding {size_limit} MB:\n\n")
            for file_path, size in large_files:
                self.results_text.insert(tk.END, f"Size: {size:.2f} MB\n")
                self.results_text.insert(tk.END, f"Path: ")
                # Insert the path as a clickable link
                link_start = self.results_text.index("end-1c")
                self.results_text.insert(tk.END, file_path + "\n\n")
                link_end = self.results_text.index("end-2c")
                self.results_text.tag_add("link", link_start, link_end)

    def find_large_files(self, folder_path, size_limit_mb):
        size_limit_bytes = size_limit_mb * 1024 * 1024
        large_files = []

        # Get custom exclusions
        custom_exclusions = [folder.strip() for folder in self.exclude_text.get("1.0", tk.END).splitlines() if folder.strip()]

        try:
            for root, dirs, files in os.walk(folder_path):
                # Skip .git folder if not included
                if '.git' in dirs and not self.include_git.get():
                    dirs.remove('.git')
                
                # Skip .godot folder if not included
                if '.godot' in dirs and not self.include_godot.get():
                    dirs.remove('.godot')
                
                # Skip custom excluded folders
                for exclude_folder in custom_exclusions:
                    if exclude_folder in dirs:
                        dirs.remove(exclude_folder)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        if file_size > size_limit_bytes:
                            size_mb = file_size / (1024 * 1024)
                            large_files.append((file_path, size_mb))
                    except OSError:
                        continue
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        return large_files

    def open_file_location(self, event):
        # Get the clicked line
        index = self.results_text.index(f"@{event.x},{event.y}")
        line_start = self.results_text.index(f"{index} linestart")
        line_end = self.results_text.index(f"{index} lineend")
        line = self.results_text.get(line_start, line_end)
        
        # Extract the file path
        if line.startswith("Path: "):
            file_path = line[6:]  # Remove "Path: " prefix
            # Open file explorer and select the file
            try:
                subprocess.run(['explorer', '/select,', os.path.normpath(file_path)])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file location: {str(e)}")

    def on_closing(self):
        """Handle window close event"""
        self.root.destroy()
        sys.exit(0)  # Ensure the Python process terminates

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSizeCheckerGUI(root)
    root.mainloop()
