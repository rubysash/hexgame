"""
core/world.py - World management and global state (Updated with Settlements)
"""

import random
from typing import Dict, Tuple, Optional, List
from core.hex_grid import HexCoordinate
from data.models import Hex, TerrainType
from data.hex_editor import HexEditorManager, HexEditData
from generation.terrain_generator import TerrainGenerator
from generation.settlement_generator import SettlementGenerator


class World:
    """
    Manages the entire game world state.
    Coordinates between terrain generation, settlement generation, hex storage, 
    edit data, and game systems.
    """
    
    def __init__(self, world_seed: Optional[int] = None):
        self.world_seed = world_seed or random.randint(0, 1000000)
        self.hexes: Dict[Tuple[int, int], Hex] = {}
        self.terrain_generator = TerrainGenerator(self.world_seed)
        self.settlement_generator = SettlementGenerator(self.world_seed)
        
        # Edit data manager
        self.editor_manager = HexEditorManager(self.world_seed)
        
        # Settlement tracking
        self.settlements_by_type: Dict[str, List[Hex]] = {}
        self.named_settlements: Dict[str, Hex] = {}
        
        # Future: Campaign state
        self.campaign_name = "default"
        self.world_timeline = []
        self.global_state = {}
        
    def get_hex(self, coord: HexCoordinate) -> Hex:
        """Get or generate a hex at the given coordinates"""
        key = coord.to_tuple()
        if key not in self.hexes:
            self.generate_hex(coord)
        
        hex_obj = self.hexes[key]
        
        # Apply edit data if it exists
        self._apply_edit_data(hex_obj)
        
        return hex_obj
    
    def _apply_edit_data(self, hex_obj: Hex):
        """Apply edit data overrides to a hex"""
        edit_data = self.editor_manager.load_hex_edit(hex_obj.q, hex_obj.r)
        if not edit_data:
            return
        
        # Store reference to edit data in hex (for UI display)
        hex_obj.edit_data = edit_data
        
        # Apply exploration overrides
        if edit_data.explored is not None:
            hex_obj.discovery_data.explored = edit_data.explored
        if edit_data.exploration_level is not None:
            hex_obj.discovery_data.exploration_level = edit_data.exploration_level
        
        # Apply terrain override (future expansion)
        if edit_data.override_terrain and edit_data.terrain_type:
            try:
                hex_obj.terrain_data.primary = TerrainType[edit_data.terrain_type]
            except KeyError:
                pass  # Invalid terrain type, ignore
        
        # Apply settlement override (future expansion)
        if edit_data.override_settlement and edit_data.settlement_name:
            if hex_obj.settlement_data:
                hex_obj.settlement_data.name = edit_data.settlement_name
    
    def save_hex_edit(self, edit_data: HexEditData) -> bool:
        """Save edit data for a hex"""
        success = self.editor_manager.save_hex_edit(edit_data)
        
        if success:
            # Refresh the hex to apply changes
            key = (edit_data.q, edit_data.r)
            if key in self.hexes:
                self._apply_edit_data(self.hexes[key])
        
        return success
    
    def has_hex_edit(self, coord: HexCoordinate) -> bool:
        """Check if a hex has edit data"""
        return self.editor_manager.has_edit(coord.q, coord.r)
    
    def get_hex_edit(self, coord: HexCoordinate) -> Optional[HexEditData]:
        """Get edit data for a hex"""
        return self.editor_manager.load_hex_edit(coord.q, coord.r)
    
    def generate_hex(self, coord: HexCoordinate):
        """Generate a new hex using terrain generation rules"""
        # Get neighboring terrain for context
        neighbor_terrains = []
        for neighbor_coord in coord.get_neighbors():
            key = neighbor_coord.to_tuple()
            if key in self.hexes:
                neighbor_terrains.append(self.hexes[key].terrain)
        
        # Generate terrain
        terrain = self.terrain_generator.generate_terrain(coord, neighbor_terrains)
        
        # Create hex
        new_hex = Hex(coord.q, coord.r, terrain)
        self.hexes[coord.to_tuple()] = new_hex
        
        # Generate settlement if appropriate
        settlement = self.settlement_generator.generate_settlement(
            coord, terrain, neighbor_terrains
        )
        
        if settlement:
            new_hex.settlement_data = settlement
            self._track_settlement(new_hex)
        
        # Apply edit data if it exists (for already edited hexes being regenerated)
        self._apply_edit_data(new_hex)
        
    def _track_settlement(self, hex_obj: Hex):
        """Track settlement for easy lookup"""
        if not hex_obj.settlement_data:
            return
            
        settlement = hex_obj.settlement_data
        settlement_type = settlement.settlement_type.name
        
        # Track by type
        if settlement_type not in self.settlements_by_type:
            self.settlements_by_type[settlement_type] = []
        self.settlements_by_type[settlement_type].append(hex_obj)
        
        # Track by name (ensure unique names)
        base_name = settlement.name
        name = base_name
        counter = 1
        while name in self.named_settlements:
            counter += 1
            name = f"{base_name} {counter}"
        
        settlement.name = name
        self.named_settlements[name] = hex_obj
    
    def get_hexes_in_range(self, center: HexCoordinate, radius: int) -> List[Hex]:
        """Get all hexes within radius of center"""
        hexes = []
        for q in range(center.q - radius, center.q + radius + 1):
            for r in range(center.r - radius, center.r + radius + 1):
                coord = HexCoordinate(q, r)
                if coord.distance_to(center) <= radius:
                    hexes.append(self.get_hex(coord))
        return hexes
    
    def get_settlements_in_range(self, center: HexCoordinate, radius: int) -> List[Hex]:
        """Get all settlements within radius of center"""
        hexes = self.get_hexes_in_range(center, radius)
        return [hex_obj for hex_obj in hexes if hex_obj.has_settlement]
    
    def find_nearest_settlement(self, coord: HexCoordinate, max_radius: int = 20) -> Optional[Hex]:
        """Find the nearest settlement to a coordinate"""
        for radius in range(1, max_radius + 1):
            settlements = self.get_settlements_in_range(coord, radius)
            if settlements:
                # Return the closest one
                return min(settlements, 
                          key=lambda h: HexCoordinate(h.q, h.r).distance_to(coord))
        return None
    
    def get_settlement_by_name(self, name: str) -> Optional[Hex]:
        """Get settlement hex by name"""
        return self.named_settlements.get(name)
    
    def get_settlements_by_type(self, settlement_type: str) -> List[Hex]:
        """Get all settlements of a specific type"""
        return self.settlements_by_type.get(settlement_type, [])
    
    def get_edited_hexes(self) -> List[Tuple[int, int]]:
        """Get list of all hexes with edit data"""
        return self.editor_manager.list_all_edits()
    
    def get_world_statistics(self) -> Dict:
        """Get statistics about the generated world"""
        stats = {
            'total_hexes': len(self.hexes),
            'total_settlements': len(self.named_settlements),
            'settlements_by_type': {k: len(v) for k, v in self.settlements_by_type.items()},
            'terrain_distribution': {},
            'largest_city': None,
            'largest_city_xy': None,
            'largest_settlements': [],
            'total_population': 0,
            'edited_hexes': len(self.get_edited_hexes())  # Track edited hexes
        }
        
        # Calculate terrain distribution and find largest settlements
        terrain_counts = {}
        total_pop = 0
        all_settlements = []
        
        for hex_obj in self.hexes.values():
            terrain_name = hex_obj.terrain.name
            terrain_counts[terrain_name] = terrain_counts.get(terrain_name, 0) + 1
            
            if hex_obj.has_settlement:
                pop = hex_obj.settlement_data.population
                total_pop += pop
                
                # Collect all settlements with their data for sorting
                all_settlements.append({
                    'name': hex_obj.settlement_data.name,
                    'population': pop,
                    'coordinates': (hex_obj.q, hex_obj.r)
                })
        
        # Sort settlements by population (descending) and take top 3
        all_settlements.sort(key=lambda s: s['population'], reverse=True)
        stats['largest_settlements'] = all_settlements[:3]
        
        # Keep backward compatibility - largest_city is still the biggest settlement
        if all_settlements:
            largest = all_settlements[0]
            stats['largest_city'] = largest['name']
            stats['largest_city_xy'] = largest['coordinates']
        
        stats['terrain_distribution'] = terrain_counts
        stats['total_population'] = total_pop
        
        return stats
    
    def update_timeline(self, current_date):
        """Process world timeline events (respawns, migrations, etc.)"""
        # Future: Process timeline events
        # - Settlement growth/decline
        # - Trade route development
        # - Seasonal changes
        # - Political changes
        pass