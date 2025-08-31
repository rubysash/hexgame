"""
data/hex_editor.py - Hex editing data management
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path

@dataclass
class HexEditData:
    """
    Stores user-edited data for a hex.
    This data overrides procedurally generated content.
    """
    # Core identification
    q: int
    r: int
    
    # Basic editable fields (MVP)
    custom_name: str = ""
    description: str = ""
    notes: str = ""
    
    # Override flags
    override_terrain: bool = False
    override_settlement: bool = False
    
    # Terrain override (if override_terrain is True)
    terrain_type: Optional[str] = None
    
    # Settlement override (if override_settlement is True) 
    settlement_name: Optional[str] = None
    settlement_type: Optional[str] = None
    settlement_population: Optional[int] = None
    
    # Discovery/exploration overrides
    explored: Optional[bool] = None
    exploration_level: Optional[int] = None
    
    # Media references (for future expansion)
    image_files: list = field(default_factory=list)
    audio_file: Optional[str] = None
    
    # Metadata
    last_edited: Optional[str] = None
    version: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HexEditData':
        """Create from dictionary"""
        return cls(**data)
    
    def has_overrides(self) -> bool:
        """Check if this edit data has any meaningful overrides"""
        return bool(
            self.custom_name or 
            self.description or 
            self.notes or 
            self.override_terrain or 
            self.override_settlement or
            self.explored is not None
        )


class HexEditorManager:
    """
    Manages loading, saving, and caching of hex edit data.
    """
    
    def __init__(self, world_seed: int, save_dir: str = "saves/edits"):
        self.world_seed = world_seed
        self.save_dir = Path(save_dir) / str(world_seed)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache loaded edit data
        self._cache: Dict[tuple, HexEditData] = {}
        
    def get_hex_filename(self, q: int, r: int) -> str:
        """
        Generate filename for hex edit data.
        Format: seed_qXXX_rYYY.json where XXX/YYY are signed coordinates
        """
        # Use simple signed format for readability
        return f"{self.world_seed}_{q:+04d}_{r:+04d}.json"
    
    def get_hex_path(self, q: int, r: int) -> Path:
        """Get full path for hex edit file"""
        return self.save_dir / self.get_hex_filename(q, r)
    
    def load_hex_edit(self, q: int, r: int) -> Optional[HexEditData]:
        """Load edit data for a hex, returns None if no edit exists"""
        # Check cache first
        key = (q, r)
        if key in self._cache:
            return self._cache[key]
        
        # Try to load from file
        file_path = self.get_hex_path(q, r)
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                edit_data = HexEditData.from_dict(data)
                self._cache[key] = edit_data
                return edit_data
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error loading hex edit at ({q}, {r}): {e}")
            return None
    
    def save_hex_edit(self, edit_data: HexEditData) -> bool:
        """Save edit data for a hex"""
        if not edit_data.has_overrides():
            # Don't save empty edits, remove file if it exists
            file_path = self.get_hex_path(edit_data.q, edit_data.r)
            if file_path.exists():
                file_path.unlink()
                # Remove from cache
                key = (edit_data.q, edit_data.r)
                self._cache.pop(key, None)
            return True
        
        # Save to file
        file_path = self.get_hex_path(edit_data.q, edit_data.r)
        try:
            # Add timestamp
            from datetime import datetime
            edit_data.last_edited = datetime.now().isoformat()
            
            with open(file_path, 'w') as f:
                json.dump(edit_data.to_dict(), f, indent=2)
            
            # Update cache
            key = (edit_data.q, edit_data.r)
            self._cache[key] = edit_data
            return True
            
        except OSError as e:
            print(f"Error saving hex edit at ({edit_data.q}, {edit_data.r}): {e}")
            return False
    
    def has_edit(self, q: int, r: int) -> bool:
        """Check if a hex has edit data without loading it fully"""
        if (q, r) in self._cache:
            return True
        return self.get_hex_path(q, r).exists()
    
    def list_all_edits(self) -> list:
        """List all hexes with edit data"""
        edits = []
        for file_path in self.save_dir.glob("*.json"):
            try:
                # Parse filename to get coordinates
                parts = file_path.stem.split('_')
                if len(parts) == 3:
                    q = int(parts[1])
                    r = int(parts[2])
                    edits.append((q, r))
            except ValueError:
                continue
        return edits
    
    def clear_cache(self):
        """Clear the cache (useful when switching worlds)"""
        self._cache.clear()
    
    def delete_hex_edit(self, q: int, r: int) -> bool:
        """Delete edit data for a hex"""
        file_path = self.get_hex_path(q, r)
        if file_path.exists():
            try:
                file_path.unlink()
                # Remove from cache
                key = (q, r)
                self._cache.pop(key, None)
                return True
            except OSError:
                return False
        return True