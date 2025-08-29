
"""
ui/renderer.py - Hex rendering utilities
"""

import pygame
import math
from typing import Tuple
from core.hex_grid import HexCoordinate
from data.models import Hex

class HexRenderer:
    """Handles rendering of hexes to pygame surface"""
    
    def __init__(self, hex_size: int = 35):
        self.hex_size = hex_size
        self.hex_height = hex_size * 2
        self.hex_width = math.sqrt(3) * hex_size
        self.font = None
        self.small_font = None
        
    def init_fonts(self):
        """Initialize pygame fonts (must be called after pygame.init())"""
        pygame.font.init()
        self.font = pygame.font.Font(None, 16)
        self.small_font = pygame.font.Font(None, 12)
        
    def hex_to_pixel(self, coord: HexCoordinate) -> Tuple[float, float]:
        """Convert hex coordinates to pixel coordinates"""
        return coord.to_pixel(self.hex_size)
    
    def pixel_to_hex(self, x: float, y: float) -> HexCoordinate:
        """Convert pixel coordinates to hex coordinates"""
        return HexCoordinate.from_pixel(x, y, self.hex_size)
    
    def draw_hexagon(self, surface: pygame.Surface, center_x: float, 
                    center_y: float, color: Tuple[int, int, int], 
                    border_color: Tuple[int, int, int] = (50, 50, 50)):
        """Draw a hexagon at the given center position"""
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            x = center_x + self.hex_size * math.cos(angle)
            y = center_y + self.hex_size * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, border_color, points, 2)
        
    def draw_hex(self, surface: pygame.Surface, hex_obj: Hex, 
                camera_x: float, camera_y: float, show_coords: bool = True):
        """Draw a single hex with its terrain color and optional coordinates"""
        coord = HexCoordinate(hex_obj.q, hex_obj.r)
        pixel_x, pixel_y = self.hex_to_pixel(coord)
        screen_x = pixel_x + camera_x
        screen_y = pixel_y + camera_y
        
        # Draw the hexagon
        self.draw_hexagon(surface, screen_x, screen_y, hex_obj.terrain.color)
        
        # Draw coordinates if requested
        if show_coords and self.font:
            text = f"{hex_obj.q},{hex_obj.r}"
            text_surface = self.font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(screen_x, screen_y))
            surface.blit(text_surface, text_rect)
        
        # Future: Draw additional layers (inhabitants, resources, etc.)
        if hex_obj.discovery_data.explored and self.small_font:
            # Draw exploration indicator
            pass
