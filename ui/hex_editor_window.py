"""
ui/hex_editor_window.py - Hex editor popup window
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional, Callable
from data.models import Hex, TerrainType, SettlementType
from data.hex_editor import HexEditData


class HexEditorWindow:
    """
    Tkinter-based hex editor window for editing hex properties.
    MVP version with basic fields, expandable for images/audio later.
    """
    
    def __init__(self, hex_obj: Hex, on_save: Optional[Callable] = None, 
                 edit_data: Optional[HexEditData] = None):
        """
        Initialize the hex editor window.
        
        Args:
            hex_obj: The hex being edited
            on_save: Callback function when save is clicked
            edit_data: Existing edit data if any
        """
        self.hex_obj = hex_obj
        self.on_save = on_save
        self.edit_data = edit_data or HexEditData(q=hex_obj.q, r=hex_obj.r)
        
        # Create the window
        self.root = tk.Toplevel()
        self.root.title(f"Edit Hex ({hex_obj.q}, {hex_obj.r})")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Make window modal
        self.root.transient()
        self.root.grab_set()
        
        # Track if changes were made
        self.has_changes = False
        
        # Create UI
        self._create_widgets()
        self._load_data()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Center window
        self._center_window()
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title = ttk.Label(main_frame, 
                         text=f"Hex Editor - ({self.hex_obj.q}, {self.hex_obj.r})",
                         font=('TkDefaultFont', 12, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Current hex info (read-only)
        info_frame = ttk.LabelFrame(main_frame, text="Current Hex Info", padding="5")
        info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        info_frame.columnconfigure(1, weight=1)
        
        # Display current terrain
        ttk.Label(info_frame, text="Terrain:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        terrain_text = f"{self.hex_obj.terrain.display_name}"
        self.terrain_label = ttk.Label(info_frame, text=terrain_text)
        self.terrain_label.grid(row=0, column=1, sticky=tk.W)
        
        # Display current settlement if any
        if self.hex_obj.has_settlement:
            ttk.Label(info_frame, text="Settlement:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
            settlement = self.hex_obj.settlement_data
            settlement_text = f"{settlement.name} ({settlement.settlement_type.display_name}, Pop: {settlement.population})"
            ttk.Label(info_frame, text=settlement_text).grid(row=1, column=1, sticky=tk.W)
        
        # Custom Name field
        ttk.Label(main_frame, text="Custom Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar(value=self.edit_data.custom_name)
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=50)
        self.name_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        self.name_var.trace('w', lambda *args: self._mark_changed())
        
        # Description field
        ttk.Label(main_frame, text="Description:").grid(row=3, column=0, sticky=(tk.W, tk.N), pady=5)
        desc_frame = ttk.Frame(main_frame)
        desc_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.desc_text = scrolledtext.ScrolledText(desc_frame, width=60, height=4, wrap=tk.WORD)
        self.desc_text.pack(fill=tk.BOTH, expand=True)
        self.desc_text.bind('<<Modified>>', self._on_text_modified)
        
        # Notes field
        ttk.Label(main_frame, text="Notes:").grid(row=4, column=0, sticky=(tk.W, tk.N), pady=5)
        notes_frame = ttk.Frame(main_frame)
        notes_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, width=60, height=6, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, expand=True)
        self.notes_text.bind('<<Modified>>', self._on_text_modified)
        
        # Override options (collapsed by default for MVP)
        override_frame = ttk.LabelFrame(main_frame, text="Override Options", padding="5")
        override_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Explored checkbox
        self.explored_var = tk.BooleanVar()
        self.explored_check = ttk.Checkbutton(override_frame, text="Mark as Explored", 
                                             variable=self.explored_var,
                                             command=self._mark_changed)
        self.explored_check.grid(row=0, column=0, sticky=tk.W)
        
        # Exploration level
        ttk.Label(override_frame, text="Exploration Level:").grid(row=0, column=1, padx=(20, 5))
        self.exploration_var = tk.IntVar()
        self.exploration_spin = ttk.Spinbox(override_frame, from_=0, to=2, width=10,
                                           textvariable=self.exploration_var,
                                           command=self._mark_changed)
        self.exploration_spin.grid(row=0, column=2)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
        # Save button
        self.save_button = ttk.Button(button_frame, text="Save", command=self._save)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        ttk.Button(button_frame, text="Cancel", command=self._on_close).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(button_frame, text="", foreground="green")
        self.status_label.pack(side=tk.LEFT, padx=20)
    
    def _load_data(self):
        """Load existing edit data into fields"""
        if self.edit_data:
            # Load basic fields
            if self.edit_data.description:
                self.desc_text.insert('1.0', self.edit_data.description)
            if self.edit_data.notes:
                self.notes_text.insert('1.0', self.edit_data.notes)
            
            # Load exploration data
            if self.edit_data.explored is not None:
                self.explored_var.set(self.edit_data.explored)
            else:
                # Use current hex state
                self.explored_var.set(self.hex_obj.discovery_data.explored)
            
            if self.edit_data.exploration_level is not None:
                self.exploration_var.set(self.edit_data.exploration_level)
            else:
                # Use current hex state
                self.exploration_var.set(self.hex_obj.discovery_data.exploration_level)
        else:
            # Load from hex if no edit data
            self.explored_var.set(self.hex_obj.discovery_data.explored)
            self.exploration_var.set(self.hex_obj.discovery_data.exploration_level)
        
        # Reset change tracking
        self.has_changes = False
        self.desc_text.edit_modified(False)
        self.notes_text.edit_modified(False)
    
    def _mark_changed(self):
        """Mark that changes have been made"""
        self.has_changes = True
        self.status_label.config(text="Unsaved changes", foreground="orange")
    
    def _on_text_modified(self, event):
        """Handle text widget modification"""
        if event.widget.edit_modified():
            self._mark_changed()
    
    def _save(self):
        """Save the edited data"""
        # Update edit data from fields
        self.edit_data.custom_name = self.name_var.get().strip()
        self.edit_data.description = self.desc_text.get('1.0', 'end-1c').strip()
        self.edit_data.notes = self.notes_text.get('1.0', 'end-1c').strip()
        
        # Update exploration data
        self.edit_data.explored = self.explored_var.get()
        self.edit_data.exploration_level = self.exploration_var.get()
        
        # Call save callback
        if self.on_save:
            success = self.on_save(self.edit_data)
            if success:
                self.status_label.config(text="Saved!", foreground="green")
                self.has_changes = False
                self.desc_text.edit_modified(False)
                self.notes_text.edit_modified(False)
                # Close after brief delay to show status
                self.root.after(500, self.root.destroy)
            else:
                self.status_label.config(text="Save failed!", foreground="red")
    
    def _on_close(self):
        """Handle window close"""
        if self.has_changes:
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Save before closing?",
                parent=self.root
            )
            if result is True:  # Yes - save and close
                self._save()
            elif result is False:  # No - close without saving
                self.root.destroy()
            # None - cancel, don't close
        else:
            self.root.destroy()