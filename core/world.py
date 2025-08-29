
"""
core/world.py - World management and global state
"""

import random
from typing import Dict, Tuple, Optional, List
from core.hex_grid import HexCoordinate
from data.models import Hex, TerrainType
from generation.terrain_generator import TerrainGenerator

class World:
    """
    Manages the entire game world state.
    Coordinates between terrain generation, hex storage, and game systems.
    """
    
    def __init__(self, world_seed: Optional[int] = None):
        self.world_seed = world_seed or random.randint(0, 1000000)
        self.hexes: Dict[Tuple[int, int], Hex] = {}
        self.terrain_generator = TerrainGenerator(self.world_seed)
        
        # Future: Campaign state
        self.campaign_name = "default"
        self.world_timeline = []
        self.global_state = {}
        
    def get_hex(self, coord: HexCoordinate) -> Hex:
        """Get or generate a hex at the given coordinates"""
        key = coord.to_tuple()
        if key not in self.hexes:
            self.generate_hex(coord)
        return self.hexes[key]
    
    def generate_hex(self, coord: HexCoordinate):
        """Generate a new hex using terrain generation rules"""
        # Get neighboring terrain for context
        neighbors = []
        for neighbor_coord in coord.get_neighbors():
            key = neighbor_coord.to_tuple()
            if key in self.hexes:
                neighbors.append(self.hexes[key].terrain)
        
        # Generate terrain
        terrain = self.terrain_generator.generate_terrain(coord, neighbors)
        
        # Create hex
        new_hex = Hex(coord.q, coord.r, terrain)
        self.hexes[coord.to_tuple()] = new_hex
        
        # Future: Generate additional content layers
        # self.generate_inhabitants(new_hex)
        # self.generate_resources(new_hex)
        # self.generate_encounters(new_hex)
        
    def get_hexes_in_range(self, center: HexCoordinate, radius: int) -> List[Hex]:
        """Get all hexes within radius of center"""
        hexes = []
        for q in range(center.q - radius, center.q + radius + 1):
            for r in range(center.r - radius, center.r + radius + 1):
                coord = HexCoordinate(q, r)
                if coord.distance_to(center) <= radius:
                    hexes.append(self.get_hex(coord))
        return hexes
    
    def update_timeline(self, current_date):
        """Process world timeline events (respawns, migrations, etc.)"""
        # Future: Process timeline events
        pass
