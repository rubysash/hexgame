"""
ui/hex_editor_window.py - Fixed Hex editor popup window
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional, Callable
from data.models import Hex, TerrainType, SettlementType
from data.hex_editor import HexEditData


class HexEditorWindow:
    """
    Tkinter-based hex editor window for editing hex properties.
    Fixed version with proper window lifecycle management.
    """
    
    def __init__(self, hex_obj: Hex, on_save: Optional[Callable] = None, 
                 edit_data: Optional[HexEditData] = None, parent=None):
        """
        Initialize the hex editor window.
        
        Args:
            hex_obj: The hex being edited
            on_save: Callback function when save is clicked
            edit_data: Existing edit data if any
            parent: Parent window (optional)
        """
        self.hex_obj = hex_obj
        self.on_save = on_save
        self.edit_data = edit_data or HexEditData(q=hex_obj.q, r=hex_obj.r)
        self.npc_frames = []

        # Create root window if none exists
        if parent is None:
            try:
                # Try to get existing root
                parent = tk._default_root
                if parent is None:
                    # Create a hidden root window
                    self.hidden_root = tk.Tk()
                    self.hidden_root.withdraw()
                    parent = self.hidden_root
                else:
                    self.hidden_root = None
            except:
                self.hidden_root = tk.Tk()
                self.hidden_root.withdraw()
                parent = self.hidden_root
        else:
            self.hidden_root = None
        
        # Create the window as a Toplevel
        self.root = tk.Toplevel(parent)
        self.root.title(f"Edit Hex ({hex_obj.q}, {hex_obj.r})")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Make window stay on top but not modal
        self.root.lift()
        self.root.focus_force()
        
        # Track if changes were made
        self.has_changes = False
        
        # Create UI
        self._create_widgets()
        self._load_data()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Center window
        self._center_window()
        
        # Track if window is closing to prevent multiple close attempts
        self._closing = False
        
        # Start the event loop processing
        self._process_events()
    
    def _process_events(self):
        """Process Tkinter events to prevent freezing"""
        if not self._closing and self.root.winfo_exists():
            try:
                self.root.update_idletasks()
                self.root.after(50, self._process_events)  # Schedule next update
            except tk.TclError:
                # Window was destroyed
                pass
    
    def _center_window(self):
        """Center the window on screen"""
        try:
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f'{width}x{height}+{x}+{y}')
        except tk.TclError:
            pass  # Window already destroyed
    
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
        desc_frame.rowconfigure(0, weight=1)
        desc_frame.columnconfigure(0, weight=1)
        
        self.desc_text = scrolledtext.ScrolledText(desc_frame, width=60, height=4, wrap=tk.WORD)
        self.desc_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.desc_text.bind('<KeyRelease>', lambda e: self._mark_changed())
        self.desc_text.bind('<Button-1>', lambda e: self._mark_changed())
        
        # Notes field
        ttk.Label(main_frame, text="Notes:").grid(row=4, column=0, sticky=(tk.W, tk.N), pady=5)
        notes_frame = ttk.Frame(main_frame)
        notes_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        notes_frame.rowconfigure(0, weight=1)
        notes_frame.columnconfigure(0, weight=1)
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, width=60, height=6, wrap=tk.WORD)
        self.notes_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.notes_text.bind('<KeyRelease>', lambda e: self._mark_changed())
        self.notes_text.bind('<Button-1>', lambda e: self._mark_changed())
        
        # Override options
        override_frame = ttk.LabelFrame(main_frame, text="Override Options", padding="5")
        override_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # NPCs section
        npc_frame = ttk.LabelFrame(main_frame, text="Notable NPCs", padding="5")
        npc_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        npc_frame.columnconfigure(0, weight=1)
        
        # NPC container with scrollbar
        canvas = tk.Canvas(npc_frame, height=150)
        scrollbar = ttk.Scrollbar(npc_frame, orient="vertical", command=canvas.yview)
        self.npc_container = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas_frame = canvas.create_window((0, 0), window=self.npc_container, anchor="nw")
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Add NPC button
        ttk.Button(npc_frame, text="Add NPC", command=self._add_npc).grid(row=1, column=0, pady=5)
        
        # Update button frame row from 6 to 7
        #button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))

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
        button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))
        
        # Save button
        self.save_button = ttk.Button(button_frame, text="Save", command=self._save)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        ttk.Button(button_frame, text="Cancel", command=self._on_close).pack(side=tk.LEFT, padx=5)
        
        # Clear All button
        ttk.Button(button_frame, text="Clear All", command=self._clear_all).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(button_frame, text="", foreground="green")
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Configure grid weights for main frame
        main_frame.rowconfigure(3, weight=1)  # Description area
        main_frame.rowconfigure(4, weight=2)  # Notes area (bigger)
    
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
            
            # ADD THIS NEW CODE HERE - Load NPCs
            if self.edit_data.notable_npcs:
                for npc_data in self.edit_data.notable_npcs:
                    self._add_npc(npc_data)
        else:
            # Load from hex if no edit data
            self.explored_var.set(self.hex_obj.discovery_data.explored)
            self.exploration_var.set(self.hex_obj.discovery_data.exploration_level)
        
        # Reset change tracking after loading
        self.has_changes = False
        self._update_status()
    
    def _update_status(self):
        """Update status label"""
        if not self.has_changes:
            self.status_label.config(text="No changes", foreground="gray")
    
    def _mark_changed(self):
        """Mark that changes have been made"""
        self.has_changes = True
        self.status_label.config(text="Unsaved changes", foreground="orange")

    def _add_npc(self, npc_data=None):
        """Add a new NPC input frame"""
        frame = ttk.Frame(self.npc_container, relief=tk.RIDGE, borderwidth=1)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create input fields
        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        frame.name_var = tk.StringVar(value=npc_data.get('name', '') if npc_data else '')
        ttk.Entry(frame, textvariable=frame.name_var, width=25).grid(row=0, column=1, padx=5)
        
        ttk.Label(frame, text="Role:").grid(row=0, column=2, sticky=tk.W)
        frame.role_var = tk.StringVar(value=npc_data.get('role', '') if npc_data else '')
        ttk.Entry(frame, textvariable=frame.role_var, width=25).grid(row=0, column=3, padx=5)
        
        ttk.Label(frame, text="Personality:").grid(row=1, column=0, sticky=tk.W)
        frame.personality_var = tk.StringVar(value=npc_data.get('personality', '') if npc_data else '')
        ttk.Entry(frame, textvariable=frame.personality_var, width=58).grid(row=1, column=1, columnspan=3, padx=5)
        
        ttk.Label(frame, text="Goals:").grid(row=2, column=0, sticky=tk.W)
        frame.goals_var = tk.StringVar(value=npc_data.get('goals', '') if npc_data else '')
        ttk.Entry(frame, textvariable=frame.goals_var, width=58).grid(row=2, column=1, columnspan=3, padx=5)
        
        # Delete button
        ttk.Button(frame, text="Remove", command=lambda: self._remove_npc(frame)).grid(row=0, column=4, padx=5)
        
        # Track changes
        frame.name_var.trace('w', lambda *args: self._mark_changed())
        frame.role_var.trace('w', lambda *args: self._mark_changed())
        frame.personality_var.trace('w', lambda *args: self._mark_changed())
        frame.goals_var.trace('w', lambda *args: self._mark_changed())
        
        self.npc_frames.append(frame)
        self._mark_changed()
    
    def _remove_npc(self, frame):
        """Remove an NPC frame"""
        self.npc_frames.remove(frame)
        frame.destroy()
        self._mark_changed()

    def _clear_all(self):
        """Clear all fields"""
        result = messagebox.askyesno(
            "Clear All",
            "Clear all custom data for this hex?",
            parent=self.root
        )
        if result:
            self.name_var.set("")
            self.desc_text.delete('1.0', tk.END)
            self.notes_text.delete('1.0', tk.END)
            self.explored_var.set(self.hex_obj.discovery_data.explored)
            self.exploration_var.set(self.hex_obj.discovery_data.exploration_level)
            self._mark_changed()
    
    def _save(self):
        """Save the edited data"""
        try:
            # Update edit data from fields
            self.edit_data.custom_name = self.name_var.get().strip()
            self.edit_data.description = self.desc_text.get('1.0', 'end-1c').strip()
            self.edit_data.notes = self.notes_text.get('1.0', 'end-1c').strip()
            
            # Update exploration data
            self.edit_data.explored = self.explored_var.get()
            self.edit_data.exploration_level = self.exploration_var.get()

            # Save NPCs
            self.edit_data.notable_npcs = []
            for frame in self.npc_frames:
                npc_data = {
                    'name': frame.name_var.get().strip(),
                    'role': frame.role_var.get().strip(),
                    'personality': frame.personality_var.get().strip(),
                    'goals': frame.goals_var.get().strip()
                }
                if npc_data['name']:  # Only save if name exists
                    self.edit_data.notable_npcs.append(npc_data)

            # Call save callback
            if self.on_save:
                success = self.on_save(self.edit_data)
                if success:
                    self.status_label.config(text="Saved!", foreground="green")
                    self.has_changes = False
                    # Close after brief delay to show status
                    self.root.after(800, self._close_window)
                else:
                    self.status_label.config(text="Save failed!", foreground="red")
            else:
                self.status_label.config(text="No save callback", foreground="red")
                
        except Exception as e:
            print(f"Error saving hex edit: {e}")
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
    
    def _close_window(self):
        """Safely close the window"""
        if self._closing:
            return
            
        self._closing = True
        try:
            # Clean up hidden root if we created it
            if self.hidden_root:
                self.hidden_root.quit()
                self.hidden_root.destroy()
            
            # Destroy the editor window
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            print(f"Error closing editor window: {e}")
    
    def _on_close(self):
        """Handle window close with unsaved changes check"""
        if self._closing:
            return  # Already closing, don't do anything
            
        if self.has_changes:
            try:
                result = messagebox.askyesnocancel(
                    "Unsaved Changes",
                    "You have unsaved changes. Save before closing?",
                    parent=self.root
                )
                if result is True:  # Yes - save and close
                    self._save()
                    # _save will close the window after delay
                    return
                elif result is False:  # No - close without saving
                    self._close_window()
                # None - cancel, don't close
            except Exception as e:
                print(f"Error in close dialog: {e}")
                self._close_window()
        else:
            self._close_window()