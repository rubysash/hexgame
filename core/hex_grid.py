"""
core/hex_grid.py - Hexagonal grid mathematics and coordinate system
"""

import math
from typing import Tuple, List

class HexCoordinate:
    """
    Represents a hexagonal coordinate using axial coordinates (q, r).
    Includes conversion methods and hex math operations.
    """
    
    def __init__(self, q: int, r: int):
        self.q = q
        self.r = r
        self.s = -q - r  # Cubic coordinate for distance calculations
        
    def __eq__(self, other):
        return self.q == other.q and self.r == other.r
    
    def __hash__(self):
        return hash((self.q, self.r))
    
    def __str__(self):
        return f"Hex({self.q}, {self.r})"
    
    def to_tuple(self) -> Tuple[int, int]:
        """Return coordinates as tuple"""
        return (self.q, self.r)
    
    def get_neighbors(self) -> List['HexCoordinate']:
        """Return list of 6 adjacent hex coordinates"""
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        return [HexCoordinate(self.q + dq, self.r + dr) for dq, dr in directions]
    
    def distance_to(self, other: 'HexCoordinate') -> int:
        """Calculate hex distance to another coordinate"""
        return (abs(self.q - other.q) + abs(self.r - other.r) + 
                abs(self.s - other.s)) // 2
    
    def to_pixel(self, hex_size: float) -> Tuple[float, float]:
        """Convert hex coordinate to pixel position"""
        x = hex_size * (3/2 * self.q)
        y = hex_size * (math.sqrt(3) * (self.r + self.q/2))
        return x, y
    
    @staticmethod
    def from_pixel(x: float, y: float, hex_size: float) -> 'HexCoordinate':
        """Convert pixel position to hex coordinate"""
        q = (2/3 * x) / hex_size
        r = (-1/3 * x + math.sqrt(3)/3 * y) / hex_size
        return HexCoordinate.axial_round(q, r)
    
    @staticmethod
    def axial_round(q: float, r: float) -> 'HexCoordinate':
        """Round fractional axial coordinates to nearest hex"""
        s = -q - r
        rq = round(q)
        rr = round(r)
        rs = round(s)
        
        q_diff = abs(rq - q)
        r_diff = abs(rr - r)
        s_diff = abs(rs - s)
        
        if q_diff > r_diff and q_diff > s_diff:
            rq = -rr - rs
        elif r_diff > s_diff:
            rr = -rq - rs
            
        return HexCoordinate(rq, rr)
