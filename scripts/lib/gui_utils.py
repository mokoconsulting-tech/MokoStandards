#!/usr/bin/env python3
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# (./LICENSE).
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Library
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/lib/gui_utils.py
# VERSION: 01.00.00
# BRIEF: Cross-platform GUI utilities for MokoStandards scripts
# PATH: /scripts/lib/gui_utils.py
# NOTE: Provides optional GUI for scripts with graceful CLI fallback

"""
GUI Utilities for MokoStandards Scripts

Provides cross-platform GUI capabilities with:
- Automatic CLI fallback when GUI not available
- File/directory selection dialogs
- Progress indicators
- Confirmation dialogs
- Input forms
- Result displays
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass

# Try to import GUI libraries (optional)
GUI_AVAILABLE = False
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    GUI_AVAILABLE = True
except ImportError:
    tk = None
    ttk = None
    filedialog = None
    messagebox = None
    scrolledtext = None


# ============================================================
# GUI Detection and Mode Selection
# ============================================================

def is_gui_available() -> bool:
    """Check if GUI is available on this system"""
    if not GUI_AVAILABLE:
        return False
    
    # Check if display is available (Linux/Mac)
    if sys.platform != 'win32':
        display = sys.platform.startswith('darwin') or 'DISPLAY' in sys.environ
        if not display:
            return False
    
    try:
        # Test if we can create a window
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception:
        return False


def should_use_gui(force_gui: bool = False, force_cli: bool = False) -> bool:
    """
    Determine if GUI should be used
    
    Args:
        force_gui: Force GUI mode (will error if not available)
        force_cli: Force CLI mode even if GUI available
        
    Returns:
        True if GUI should be used
    """
    if force_cli:
        return False
    if force_gui:
        if not is_gui_available():
            raise RuntimeError("GUI mode requested but GUI not available")
        return True
    
    # Auto-detect: use GUI if available and no pipe/redirect
    return is_gui_available() and sys.stdout.isatty()


# ============================================================
# Dialog Functions
# ============================================================

def select_file(
    title: str = "Select File",
    filetypes: Optional[List[tuple]] = None,
    initialdir: Optional[str] = None,
    use_gui: bool = True
) -> Optional[Path]:
    """
    Select a file using GUI or CLI prompt
    
    Args:
        title: Dialog title
        filetypes: List of (description, pattern) tuples
        initialdir: Initial directory
        use_gui: Use GUI if available
        
    Returns:
        Selected file path or None
    """
    if use_gui and is_gui_available():
        root = tk.Tk()
        root.withdraw()
        
        filename = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes or [("All files", "*.*")],
            initialdir=initialdir
        )
        
        root.destroy()
        return Path(filename) if filename else None
    else:
        # CLI fallback
        print(f"\n{title}")
        if initialdir:
            print(f"Starting directory: {initialdir}")
        filepath = input("Enter file path (or press Enter to cancel): ").strip()
        return Path(filepath) if filepath else None


def select_directory(
    title: str = "Select Directory",
    initialdir: Optional[str] = None,
    use_gui: bool = True
) -> Optional[Path]:
    """
    Select a directory using GUI or CLI prompt
    
    Args:
        title: Dialog title
        initialdir: Initial directory
        use_gui: Use GUI if available
        
    Returns:
        Selected directory path or None
    """
    if use_gui and is_gui_available():
        root = tk.Tk()
        root.withdraw()
        
        dirname = filedialog.askdirectory(
            title=title,
            initialdir=initialdir
        )
        
        root.destroy()
        return Path(dirname) if dirname else None
    else:
        # CLI fallback
        print(f"\n{title}")
        if initialdir:
            print(f"Starting directory: {initialdir}")
        dirpath = input("Enter directory path (or press Enter to cancel): ").strip()
        return Path(dirpath) if dirpath else None


def confirm(
    message: str,
    title: str = "Confirm",
    use_gui: bool = True
) -> bool:
    """
    Show confirmation dialog
    
    Args:
        message: Confirmation message
        title: Dialog title
        use_gui: Use GUI if available
        
    Returns:
        True if confirmed, False otherwise
    """
    if use_gui and is_gui_available():
        root = tk.Tk()
        root.withdraw()
        
        result = messagebox.askyesno(title, message)
        
        root.destroy()
        return result
    else:
        # CLI fallback
        print(f"\n{title}")
        print(message)
        response = input("Continue? (y/N): ").strip().lower()
        return response in ('y', 'yes')


def show_info(
    message: str,
    title: str = "Information",
    use_gui: bool = True
):
    """Show information message"""
    if use_gui and is_gui_available():
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title, message)
        root.destroy()
    else:
        print(f"\nℹ️  {title}")
        print(message)


def show_error(
    message: str,
    title: str = "Error",
    use_gui: bool = True
):
    """Show error message"""
    if use_gui and is_gui_available():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    else:
        print(f"\n❌ {title}", file=sys.stderr)
        print(message, file=sys.stderr)


def show_warning(
    message: str,
    title: str = "Warning",
    use_gui: bool = True
):
    """Show warning message"""
    if use_gui and is_gui_available():
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(title, message)
        root.destroy()
    else:
        print(f"\n⚠️  {title}")
        print(message)


# ============================================================
# Input Forms
# ============================================================

@dataclass
class FormField:
    """Form field definition"""
    name: str
    label: str
    field_type: str = "text"  # text, password, number, choice
    default: str = ""
    required: bool = True
    choices: Optional[List[str]] = None


class SimpleForm:
    """Simple input form with GUI or CLI fallback"""
    
    def __init__(self, title: str, fields: List[FormField], use_gui: bool = True):
        self.title = title
        self.fields = fields
        self.use_gui = use_gui and is_gui_available()
        self.values: Dict[str, str] = {}
    
    def show(self) -> Optional[Dict[str, str]]:
        """Show form and return values"""
        if self.use_gui:
            return self._show_gui()
        else:
            return self._show_cli()
    
    def _show_gui(self) -> Optional[Dict[str, str]]:
        """Show GUI form"""
        root = tk.Tk()
        root.title(self.title)
        root.geometry("500x400")
        
        # Create form fields
        entries = {}
        row = 0
        
        for field in self.fields:
            # Label
            label = ttk.Label(root, text=field.label + ("*" if field.required else ""))
            label.grid(row=row, column=0, sticky="w", padx=10, pady=5)
            
            # Input widget
            if field.field_type == "choice" and field.choices:
                widget = ttk.Combobox(root, values=field.choices, width=40)
                if field.default:
                    widget.set(field.default)
            elif field.field_type == "password":
                widget = ttk.Entry(root, show="*", width=40)
            else:
                widget = ttk.Entry(root, width=40)
                if field.default:
                    widget.insert(0, field.default)
            
            widget.grid(row=row, column=1, padx=10, pady=5)
            entries[field.name] = widget
            row += 1
        
        # Buttons
        button_frame = ttk.Frame(root)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        result = {"submitted": False}
        
        def on_submit():
            # Validate and collect values
            for field in self.fields:
                value = entries[field.name].get().strip()
                if field.required and not value:
                    messagebox.showerror("Error", f"{field.label} is required")
                    return
                self.values[field.name] = value
            result["submitted"] = True
            root.quit()
        
        def on_cancel():
            root.quit()
        
        submit_btn = ttk.Button(button_frame, text="Submit", command=on_submit)
        submit_btn.pack(side="left", padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=on_cancel)
        cancel_btn.pack(side="left", padx=5)
        
        root.mainloop()
        root.destroy()
        
        return self.values if result["submitted"] else None
    
    def _show_cli(self) -> Optional[Dict[str, str]]:
        """Show CLI form"""
        print(f"\n{self.title}")
        print("=" * len(self.title))
        
        for field in self.fields:
            while True:
                prompt = f"{field.label}"
                if field.default:
                    prompt += f" [{field.default}]"
                if field.required:
                    prompt += " *"
                prompt += ": "
                
                if field.field_type == "choice" and field.choices:
                    print(f"Choices: {', '.join(field.choices)}")
                
                value = input(prompt).strip()
                
                if not value and field.default:
                    value = field.default
                
                if field.required and not value:
                    print("❌ This field is required")
                    continue
                
                self.values[field.name] = value
                break
        
        # Confirm submission
        print("\nValues entered:")
        for name, value in self.values.items():
            field = next(f for f in self.fields if f.name == name)
            if field.field_type == "password":
                print(f"  {field.label}: ******")
            else:
                print(f"  {field.label}: {value}")
        
        if not confirm("Submit these values?", use_gui=False):
            return None
        
        return self.values


# ============================================================
# Progress Indicator
# ============================================================

class ProgressWindow:
    """Progress indicator with GUI or CLI fallback"""
    
    def __init__(self, title: str = "Processing", use_gui: bool = True):
        self.title = title
        self.use_gui = use_gui and is_gui_available()
        self.root = None
        self.progress_var = None
        self.status_label = None
        
        if self.use_gui:
            self._create_gui()
    
    def _create_gui(self):
        """Create GUI progress window"""
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry("400x150")
        
        # Status label
        self.status_label = ttk.Label(self.root, text="Starting...", font=("Arial", 10))
        self.status_label.pack(pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            self.root,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=350
        )
        progress_bar.pack(pady=10)
        
        # Cancel button (optional)
        cancel_btn = ttk.Button(self.root, text="Cancel", command=self.root.quit)
        cancel_btn.pack(pady=10)
        
        self.root.update()
    
    def update(self, percent: float, status: str = ""):
        """Update progress"""
        if self.use_gui and self.root:
            self.progress_var.set(percent)
            if status:
                self.status_label.config(text=status)
            self.root.update()
        else:
            # CLI fallback
            bar_length = 50
            filled = int(bar_length * percent / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"\r{status} [{bar}] {percent:.1f}%", end="", flush=True)
    
    def close(self):
        """Close progress window"""
        if self.use_gui and self.root:
            self.root.destroy()
        else:
            print()  # New line after progress bar


# ============================================================
# Example Usage
# ============================================================

if __name__ == "__main__":
    import time
    
    print(f"GUI Available: {is_gui_available()}")
    print(f"Should use GUI: {should_use_gui()}")
    
    # Test file selection
    if confirm("Test file selection?"):
        file_path = select_file(title="Select a Python file",
                               filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if file_path:
            print(f"Selected: {file_path}")
    
    # Test form
    if confirm("Test input form?"):
        form = SimpleForm(
            title="Configuration",
            fields=[
                FormField("name", "Name", default="test"),
                FormField("email", "Email", required=True),
                FormField("role", "Role", field_type="choice",
                         choices=["Developer", "Admin", "User"], default="Developer")
            ]
        )
        values = form.show()
        if values:
            print(f"Form values: {values}")
    
    # Test progress
    if confirm("Test progress indicator?"):
        with ProgressWindow("Processing Files") as progress:
            for i in range(101):
                progress.update(i, f"Processing item {i}/100")
                time.sleep(0.05)
