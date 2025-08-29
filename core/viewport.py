"""
core/viewport.py - Viewport and memory management
"""

from typing import List, Set, Tuple
from core.hex_grid import HexCoordinate
from core.world import World
from data.models import Hex

class Viewport:
    """
    Manages the visible area of the world and memory optimization.
    Implements lazy loading and unloading strategies.
    """
    
    def __init__(self, world: World, radius: int = 15, buffer: int = 20):
        self.world = world
        self.radius = radius  # Viewport radius
        self.buffer_radius = buffer  # Buffer zone for smooth scrolling
        self.center = HexCoordinate(0, 0)
        self.loaded_coords: Set[Tuple[int, int]] = set()
        
    def update(self, new_center: HexCoordinate):
        """Update viewport center and load/unload hexes as needed"""
        self.center = new_center
        
        # Load hexes in buffer radius
        new_loaded = set()
        for q in range(new_center.q - self.buffer_radius, 
                      new_center.q + self.buffer_radius + 1):
            for r in range(new_center.r - self.buffer_radius,
                          new_center.r + self.buffer_radius + 1):
                coord = HexCoordinate(q, r)
                if coord.distance_to(new_center) <= self.buffer_radius:
                    self.world.get_hex(coord)  # Ensure hex is generated
                    new_loaded.add(coord.to_tuple())
        
        self.loaded_coords = new_loaded
        
        # Future: Unload distant hexes if memory becomes an issue
        
    def get_visible_hexes(self) -> List[Hex]:
        """Get list of hexes currently visible in viewport"""
        return self.world.get_hexes_in_range(self.center, self.radius)
    
    def is_hex_visible(self, coord: HexCoordinate) -> bool:
        """Check if a hex is within the visible viewport"""
        return coord.distance_to(self.center) <= self.radius
