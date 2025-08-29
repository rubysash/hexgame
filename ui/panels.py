"""
ui/panels.py - UI panels for game information display
"""

import pygame
from typing import Optional
from config import Config
from core.hex_grid import HexCoordinate
from data.models import Hex, TerrainType

class UIPanel:
    """Manages UI panels and information display"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.ui_font = pygame.font.Font(None, 24)
        self.tooltip_font = pygame.font.Font(None, 18)
        self.legend_font = pygame.font.Font(None, 16)
        
    def draw(self, viewport_center: HexCoordinate, hex_count: int, 
             mouse_hex: Optional[Hex] = None):
        """Draw all UI elements"""
        self.draw_top_panel(viewport_center, hex_count)
        self.draw_legend()
        if mouse_hex:
            self.draw_tooltip(mouse_hex)
    
    def draw_top_panel(self, viewport_center: HexCoordinate, hex_count: int):
        """Draw top information panel"""
        # Panel background
        panel_rect = pygame.Rect(0, 0, Config.SCREEN_WIDTH, 40)
        pygame.draw.rect(self.screen, Config.UI_PANEL_COLOR, panel_rect)
        pygame.draw.line(self.screen, Config.UI_BORDER_COLOR, 
                         (0, 40), (Config.SCREEN_WIDTH, 40), 2)
        
        # Instructions
        instructions = "Arrow Keys: Move | Shift: Fast | Space: Reset | Ctrl+S: Save | Ctrl+L: Load | ESC: Quit"
        text = self.ui_font.render(instructions, True, Config.TEXT_COLOR)
        self.screen.blit(text, (10, 10))
        
        # Viewport info
        vp_text = f"Viewport: ({viewport_center.q}, {viewport_center.r}) | Hexes: {hex_count}"
        text = self.ui_font.render(vp_text, True, (150, 150, 150))
        self.screen.blit(text, (Config.SCREEN_WIDTH - 350, 10))
    
    def draw_legend(self):
        """Draw terrain type legend"""
        legend_x = Config.SCREEN_WIDTH - 250
        legend_y = Config.SCREEN_HEIGHT - 200
        
        # Background
        pygame.draw.rect(self.screen, Config.UI_PANEL_COLOR,
                        (legend_x - 10, legend_y - 10, 240, 190))
        pygame.draw.rect(self.screen, Config.UI_BORDER_COLOR,
                        (legend_x - 10, legend_y - 10, 240, 190), 2)
        
        # Title
        title = self.ui_font.render("Terrain Types", True, Config.TEXT_COLOR)
        self.screen.blit(title, (legend_x, legend_y - 5))
        
        # Terrain types
        for i, terrain_type in enumerate(TerrainType):
            y_pos = legend_y + 25 + i * 25
            
            # Color sample
            pygame.draw.rect(self.screen, terrain_type.color, 
                           (legend_x, y_pos, 20, 20))
            pygame.draw.rect(self.screen, Config.UI_BORDER_COLOR,
                           (legend_x, y_pos, 20, 20), 1)
            
            # Name and movement cost
            text = f"{terrain_type.display_name}"
            if terrain_type.movement_cost:
                text += f" (Move: {terrain_type.movement_cost})"
            rendered = self.legend_font.render(text, True, (180, 180, 180))
            self.screen.blit(rendered, (legend_x + 30, y_pos + 2))
    
    def draw_tooltip(self, hex_obj: Hex):
        """Draw tooltip for hovered hex"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Prepare tooltip content
        lines = [
            f"Hex ({hex_obj.q}, {hex_obj.r})",
            f"Terrain: {hex_obj.terrain.display_name}",
            hex_obj.terrain.description
        ]
        
        # Add exploration status if explored
        if hex_obj.discovery_data.explored:
            lines.append(f"Exploration Level: {hex_obj.discovery_data.exploration_level}")
        
        # Calculate tooltip size
        max_width = max(self.tooltip_font.size(line)[0] for line in lines)
        tooltip_height = len(lines) * 20 + 10
        
        # Position tooltip
        tooltip_x = mouse_x + 10
        tooltip_y = mouse_y - tooltip_height - 10
        
        # Keep on screen
        if tooltip_x + max_width + 20 > Config.SCREEN_WIDTH:
            tooltip_x = mouse_x - max_width - 30
        if tooltip_y < 50:
            tooltip_y = mouse_y + 10
        
        # Draw background
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, max_width + 20, tooltip_height)
        pygame.draw.rect(self.screen, (10, 10, 10), tooltip_rect)
        pygame.draw.rect(self.screen, (70, 130, 180), tooltip_rect, 2)
        
        # Draw text
        for i, line in enumerate(lines):
            text = self.tooltip_font.render(line, True, Config.TEXT_COLOR)
            self.screen.blit(text, (tooltip_x + 10, tooltip_y + 5 + i * 20))
