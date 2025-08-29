"""
ui/renderer.py - Hex rendering utilities (Updated with Settlement Display)
"""

import pygame
import math
from typing import Tuple
from core.hex_grid import HexCoordinate
from data.models import Hex, SettlementType

class HexRenderer:
    """Handles rendering of hexes to pygame surface"""
    
    def __init__(self, hex_size: int = 35):
        self.hex_size = hex_size
        self.hex_height = hex_size * 2
        self.hex_width = math.sqrt(3) * hex_size
        self.font = None
        self.small_font = None
        self.settlement_font = None
        
        # Settlement display settings
        self.show_settlement_names = True
        self.show_settlement_icons = True
        self.show_population = False
        
    def init_fonts(self):
        """Initialize pygame fonts (must be called after pygame.init())"""
        pygame.font.init()
        self.font = pygame.font.Font(None, 16)
        self.small_font = pygame.font.Font(None, 12)
        self.settlement_font = pygame.font.Font(None, 14)
        
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
    
    def draw_settlement_icon(self, surface: pygame.Surface, center_x: float, 
                           center_y: float, settlement_type: SettlementType):
        """Draw settlement icon/symbol"""
        if not self.show_settlement_icons:
            return
            
        # Settlement size and color based on type
        if settlement_type in [SettlementType.FARMSTEAD, SettlementType.HAMLET]:
            size = 4
            color = (139, 69, 19)  # Brown
        elif settlement_type == SettlementType.VILLAGE:
            size = 6
            color = (160, 82, 45)  # Saddle brown
        elif settlement_type == SettlementType.TOWN:
            size = 8
            color = (105, 105, 105)  # Dim gray
        elif settlement_type == SettlementType.CITY:
            size = 12
            color = (70, 70, 70)  # Dark gray
        elif settlement_type in [SettlementType.LOGGING_CAMP, SettlementType.MINING_CAMP]:
            size = 5
            color = (184, 134, 11)  # Dark goldenrod
        elif settlement_type == SettlementType.MONASTERY:
            size = 6
            color = (75, 0, 130)  # Indigo
        elif settlement_type == SettlementType.WATCHTOWER:
            size = 4
            color = (128, 0, 0)  # Maroon
        else:  # Ruins
            size = 4
            color = (105, 105, 105)  # Dim gray
        
        # Draw settlement icon
        if settlement_type.name.startswith('RUINS'):
            # Draw ruins as broken square
            points = [
                (center_x - size, center_y - size),
                (center_x + size - 2, center_y - size + 1),
                (center_x + size, center_y + size - 2),
                (center_x - size + 1, center_y + size)
            ]
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, (60, 60, 60), points, 1)
        elif settlement_type == SettlementType.WATCHTOWER:
            # Draw tower as triangle
            points = [
                (center_x, center_y - size),
                (center_x - size//2, center_y + size//2),
                (center_x + size//2, center_y + size//2)
            ]
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, (0, 0, 0), points, 1)
        elif settlement_type == SettlementType.MONASTERY:
            # Draw monastery as cross
            pygame.draw.rect(surface, color, 
                           (center_x - size//4, center_y - size, size//2, size*2))
            pygame.draw.rect(surface, color,
                           (center_x - size, center_y - size//4, size*2, size//2))
            pygame.draw.rect(surface, (0, 0, 0),
                           (center_x - size//4, center_y - size, size//2, size*2), 1)
            pygame.draw.rect(surface, (0, 0, 0),
                           (center_x - size, center_y - size//4, size*2, size//2), 1)
        else:
            # Draw regular settlements as squares/rectangles
            if settlement_type == SettlementType.CITY:
                # Draw city as filled rectangle with border
                pygame.draw.rect(surface, color, 
                               (center_x - size, center_y - size, size*2, size*2))
                pygame.draw.rect(surface, (0, 0, 0),
                               (center_x - size, center_y - size, size*2, size*2), 2)
            else:
                # Draw other settlements as filled circles
                pygame.draw.circle(surface, color, (int(center_x), int(center_y)), size)
                pygame.draw.circle(surface, (0, 0, 0), (int(center_x), int(center_y)), size, 1)
    
    def draw_settlement_name(self, surface: pygame.Surface, center_x: float,
                           center_y: float, settlement_name: str, settlement_type: SettlementType):
        """Draw settlement name"""
        if not self.show_settlement_names or not self.settlement_font:
            return
        
        # Position text below the hex
        text_y = center_y + self.hex_size + 5
        
        # Choose text color based on settlement importance
        if settlement_type in [SettlementType.CITY, SettlementType.TOWN]:
            text_color = (255, 255, 255)  # White for important settlements
        elif settlement_type.name.startswith('RUINS'):
            text_color = (128, 128, 128)  # Gray for ruins
        else:
            text_color = (200, 200, 200)  # Light gray for others
        
        # Render text
        text_surface = self.settlement_font.render(settlement_name, True, text_color)
        text_rect = text_surface.get_rect(center=(center_x, text_y))
        
        # Draw background for better readability
        bg_rect = text_rect.copy()
        bg_rect.inflate_ip(4, 2)
        pygame.draw.rect(surface, (0, 0, 0, 128), bg_rect)
        
        surface.blit(text_surface, text_rect)
    
    def draw_hex(self, surface: pygame.Surface, hex_obj: Hex, 
                camera_x: float, camera_y: float, show_coords: bool = True):
        """Draw a single hex with its terrain color, settlements, and optional coordinates"""
        coord = HexCoordinate(hex_obj.q, hex_obj.r)
        pixel_x, pixel_y = self.hex_to_pixel(coord)
        screen_x = pixel_x + camera_x
        screen_y = pixel_y + camera_y
        
        # Draw the hexagon
        border_color = (50, 50, 50)
        if hex_obj.has_settlement:
            border_color = (100, 100, 100)  # Lighter border for settlements
        
        self.draw_hexagon(surface, screen_x, screen_y, hex_obj.terrain.color, border_color)
        
        # Draw settlement if present
        if hex_obj.has_settlement:
            self.draw_settlement_icon(surface, screen_x, screen_y, 
                                    hex_obj.settlement_data.settlement_type)
            
            if self.show_settlement_names:
                self.draw_settlement_name(surface, screen_x, screen_y,
                                        hex_obj.settlement_data.name,
                                        hex_obj.settlement_data.settlement_type)
        
        # Draw coordinates if requested and no settlement name is shown
        if show_coords and self.font and not (hex_obj.has_settlement and self.show_settlement_names):
            text = f"{hex_obj.q},{hex_obj.r}"
            text_surface = self.font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(screen_x, screen_y))
            surface.blit(text_surface, text_rect)
        
        # Draw exploration indicator if explored
        if hex_obj.discovery_data.explored and self.small_font:
            level = hex_obj.discovery_data.exploration_level
            if level > 0:
                indicator = "•" * level
                text_surface = self.small_font.render(indicator, True, (255, 215, 0))  # Gold
                surface.blit(text_surface, (screen_x - 10, screen_y - self.hex_size + 5))
    
    def toggle_settlement_names(self):
        """Toggle display of settlement names"""
        self.show_settlement_names = not self.show_settlement_names
    
    def toggle_settlement_icons(self):
        """Toggle display of settlement icons"""
        self.show_settlement_icons = not self.show_settlement_icons
    
    def toggle_population_display(self):
        """Toggle display of population numbers"""
        self.show_population = not self.show_population