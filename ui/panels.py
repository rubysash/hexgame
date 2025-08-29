"""
ui/panels.py - UI panels for game information display (Updated with Settlement Info)
"""

import pygame
from typing import Optional, Dict, List
from config import Config
from core.hex_grid import HexCoordinate
from data.models import Hex, TerrainType, SettlementType

class UIPanel:
    """Manages UI panels and information display"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.ui_font = pygame.font.Font(None, 24)
        self.tooltip_font = pygame.font.Font(None, 18)
        self.legend_font = pygame.font.Font(None, 16)
        self.settlement_font = pygame.font.Font(None, 14)
        
        # Panel visibility toggles
        self.show_legend = True
        self.show_settlement_panel = True
        self.show_statistics = False
        
    def draw(self, viewport_center: HexCoordinate, hex_count: int, 
             mouse_hex: Optional[Hex] = None, world_stats: Optional[Dict] = None):
        """Draw all UI elements"""
        self.draw_top_panel(viewport_center, hex_count)
        
        if self.show_legend:
            self.draw_legend()
            
        if self.show_settlement_panel and world_stats:
            self.draw_settlement_summary(world_stats)
            
        if self.show_statistics and world_stats:
            self.draw_world_statistics(world_stats)
            
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
        instructions = "Arrow Keys: Move | Shift: Fast | Space: Reset | Ctrl+S: Save | Ctrl+L: Load | N: Toggle Names | ESC: Quit"
        text = self.ui_font.render(instructions, True, Config.TEXT_COLOR)
        self.screen.blit(text, (10, 10))
        
        # Viewport info
        vp_text = f"Viewport: ({viewport_center.q}, {viewport_center.r}) | Hexes: {hex_count}"
        text = self.ui_font.render(vp_text, True, (150, 150, 150))
        self.screen.blit(text, (Config.SCREEN_WIDTH - 350, 10))
    
    def draw_legend(self):
        """Draw terrain type legend"""
        legend_x = Config.SCREEN_WIDTH - 250
        legend_y = Config.SCREEN_HEIGHT - 300
        
        # Background
        pygame.draw.rect(self.screen, Config.UI_PANEL_COLOR,
                        (legend_x - 10, legend_y - 10, 240, 290))
        pygame.draw.rect(self.screen, Config.UI_BORDER_COLOR,
                        (legend_x - 10, legend_y - 10, 240, 290), 2)
        
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
        
        # Settlement legend
        settlement_y = legend_y + 200
        title = self.ui_font.render("Settlements", True, Config.TEXT_COLOR)
        self.screen.blit(title, (legend_x, settlement_y))
        
        # Key settlement types
        key_settlements = [
            (SettlementType.FARMSTEAD, "◦", "Farmstead/Hamlet"),
            (SettlementType.VILLAGE, "●", "Village"),
            (SettlementType.TOWN, "■", "Town"),
            (SettlementType.CITY, "▣", "City"),
            (SettlementType.RUINS_VILLAGE, "◇", "Ruins"),
        ]
        
        for i, (settlement_type, symbol, name) in enumerate(key_settlements):
            y_pos = settlement_y + 25 + i * 18
            
            # Symbol
            symbol_text = self.legend_font.render(symbol, True, (200, 200, 200))
            self.screen.blit(symbol_text, (legend_x, y_pos))
            
            # Name
            name_text = self.legend_font.render(name, True, (180, 180, 180))
            self.screen.blit(name_text, (legend_x + 20, y_pos))
    
    def draw_settlement_summary(self, world_stats: Dict):
        """Draw settlement summary panel"""
        panel_x = 10
        panel_y = 60
        panel_width = 280
        panel_height = 200
        
        # Background
        pygame.draw.rect(self.screen, Config.UI_PANEL_COLOR,
                        (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, Config.UI_BORDER_COLOR,
                        (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Title
        title = self.ui_font.render("Settlement Summary", True, Config.TEXT_COLOR)
        self.screen.blit(title, (panel_x + 10, panel_y + 10))
        
        y_offset = 40
        
        # Total settlements and population
        total_settlements = world_stats.get('total_settlements', 0)
        total_population = world_stats.get('total_population', 0)
        
        text = self.settlement_font.render(f"Total Settlements: {total_settlements}", True, (200, 200, 200))
        self.screen.blit(text, (panel_x + 10, panel_y + y_offset))
        y_offset += 18
        
        text = self.settlement_font.render(f"Total Population: {total_population:,}", True, (200, 200, 200))
        self.screen.blit(text, (panel_x + 10, panel_y + y_offset))
        y_offset += 25
        
        # Largest city
        largest_city = world_stats.get('largest_city')
        if largest_city:
            text = self.settlement_font.render(f"Largest City: {largest_city}", True, (220, 220, 100))
            self.screen.blit(text, (panel_x + 10, panel_y + y_offset))
            y_offset += 20
        
        # Settlement breakdown
        settlements_by_type = world_stats.get('settlements_by_type', {})
        if settlements_by_type:
            text = self.settlement_font.render("By Type:", True, (180, 180, 180))
            self.screen.blit(text, (panel_x + 10, panel_y + y_offset))
            y_offset += 18
            
            # Sort by count, descending
            sorted_settlements = sorted(settlements_by_type.items(), 
                                      key=lambda x: x[1], reverse=True)
            
            for settlement_type, count in sorted_settlements[:6]:  # Show top 6
                if count > 0:
                    # Clean up settlement type name for display
                    display_name = settlement_type.replace('_', ' ').title()
                    if display_name.startswith('Ruins '):
                        display_name = display_name.replace('Ruins ', 'Ruins: ')
                    
                    text = self.settlement_font.render(f"  {display_name}: {count}", 
                                                     True, (160, 160, 160))
                    self.screen.blit(text, (panel_x + 20, panel_y + y_offset))
                    y_offset += 16
    
    def draw_world_statistics(self, world_stats: Dict):
        """Draw detailed world statistics panel"""
        panel_x = 10
        panel_y = 280
        panel_width = 280
        panel_height = 150
        
        # Background
        pygame.draw.rect(self.screen, Config.UI_PANEL_COLOR,
                        (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, Config.UI_BORDER_COLOR,
                        (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Title
        title = self.ui_font.render("World Statistics", True, Config.TEXT_COLOR)
        self.screen.blit(title, (panel_x + 10, panel_y + 10))
        
        y_offset = 40
        
        # Total hexes
        total_hexes = world_stats.get('total_hexes', 0)
        text = self.settlement_font.render(f"Total Hexes Explored: {total_hexes}", True, (200, 200, 200))
        self.screen.blit(text, (panel_x + 10, panel_y + y_offset))
        y_offset += 20
        
        # Terrain distribution
        terrain_dist = world_stats.get('terrain_distribution', {})
        if terrain_dist:
            text = self.settlement_font.render("Terrain Distribution:", True, (180, 180, 180))
            self.screen.blit(text, (panel_x + 10, panel_y + y_offset))
            y_offset += 18
            
            # Sort by count, descending
            sorted_terrain = sorted(terrain_dist.items(), key=lambda x: x[1], reverse=True)
            
            for terrain_type, count in sorted_terrain[:4]:  # Show top 4
                percentage = (count / total_hexes * 100) if total_hexes > 0 else 0
                display_name = terrain_type.replace('_', ' ').title()
                text = self.settlement_font.render(f"  {display_name}: {count} ({percentage:.1f}%)", 
                                                 True, (160, 160, 160))
                self.screen.blit(text, (panel_x + 20, panel_y + y_offset))
                y_offset += 16
    
    def draw_tooltip(self, hex_obj: Hex):
        """Draw tooltip for hovered hex"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Prepare tooltip content
        lines = [
            f"Hex ({hex_obj.q}, {hex_obj.r})",
            f"Terrain: {hex_obj.terrain.display_name}",
        ]
        
        # Add settlement info if present
        if hex_obj.has_settlement:
            settlement = hex_obj.settlement_data
            lines.extend([
                "",  # Blank line
                f"Settlement: {settlement.name}",
                f"Type: {settlement.settlement_type.display_name}",
                f"Population: {settlement.population:,}" if settlement.population > 0 else "Population: Abandoned",
                f"Prosperity: {'★' * settlement.prosperity_level}",
            ])
            
            # Add special features
            if settlement.special_features:
                lines.append("Features:")
                for feature in settlement.special_features[:3]:  # Limit to 3
                    feature_display = feature.replace('_', ' ').title()
                    lines.append(f"  • {feature_display}")
            
            # Add trade goods
            if settlement.trade_goods:
                goods_text = ", ".join(settlement.trade_goods[:3])  # Limit to 3
                lines.append(f"Trade: {goods_text}")
        else:
            lines.append(hex_obj.terrain.description)
        
        # Add exploration status if explored
        if hex_obj.discovery_data.explored:
            lines.append(f"Exploration Level: {hex_obj.discovery_data.exploration_level}")
        
        # Calculate tooltip size
        max_width = max(self.tooltip_font.size(line)[0] for line in lines if line)
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
        pygame.draw.rect(self.screen, (10, 10, 10, 240), tooltip_rect)
        pygame.draw.rect(self.screen, (70, 130, 180), tooltip_rect, 2)
        
        # Draw text
        for i, line in enumerate(lines):
            if line:  # Skip empty lines for spacing
                color = Config.TEXT_COLOR
                if "Settlement:" in line:
                    color = (255, 215, 0)  # Gold for settlement name
                elif line.startswith("  •"):
                    color = (180, 180, 180)  # Gray for features
                
                text = self.tooltip_font.render(line, True, color)
                self.screen.blit(text, (tooltip_x + 10, tooltip_y + 5 + i * 20))
    
    def toggle_legend(self):
        """Toggle legend visibility"""
        self.show_legend = not self.show_legend
    
    def toggle_settlement_panel(self):
        """Toggle settlement panel visibility"""
        self.show_settlement_panel = not self.show_settlement_panel
    
    def toggle_statistics(self):
        """Toggle statistics panel visibility"""
        self.show_statistics = not self.show_statistics