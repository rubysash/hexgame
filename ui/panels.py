"""
ui/panels.py - UI panels for game information display (Updated with Settlement Info)
"""

import pygame
from typing import Optional, Dict, List
from config import Config
from core.hex_grid import HexCoordinate
from data.models import Hex, TerrainType, SettlementType
from generation.config_data import SETTLEMENT_SYMBOLS, SETTLEMENT_COLORS

class UIPanel:
    """Manages UI panels and information display"""
    
    def __init__(self, screen: pygame.Surface, renderer=None):
        self.screen = screen
        self.renderer = renderer  # Reference to renderer for shared fonts
        
        # Initialize standard fonts
        self.ui_font = pygame.font.Font(None, 24)
        self.tooltip_font = pygame.font.Font(None, 18)
        self.legend_font = pygame.font.Font(None, 16)
        self.settlement_font = pygame.font.Font(None, 14)
        
        # Panel visibility toggles
        self.show_legend = True
        self.show_settlement_panel = True
        self.show_statistics = False
        
    def set_renderer(self, renderer):
        """Set renderer reference after initialization for shared font access"""
        self.renderer = renderer
        
    def get_unicode_font(self):
        """Get the Unicode-capable font from renderer, with fallback"""
        if self.renderer and hasattr(self.renderer, 'unicode_font') and self.renderer.unicode_font:
            return self.renderer.unicode_font
        return self.legend_font  # Fallback to default font
        
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
        instructions = "Arrows: Move | +/-: Zoom | 0: Reset Zoom | Space: Reset | N: Names | ESC: Quit"
        text = self.ui_font.render(instructions, True, Config.TEXT_COLOR)
        self.screen.blit(text, (10, 10))
        
        # Viewport info
        vp_text = f"Viewport: ({viewport_center.q}, {viewport_center.r}) | Hexes: {hex_count}"
        text = self.ui_font.render(vp_text, True, (150, 150, 150))
        self.screen.blit(text, (Config.SCREEN_WIDTH - 350, 10))
    
    def draw_legend(self):
        """Draw terrain type legend with proper Unicode font support"""
        legend_x = Config.SCREEN_WIDTH - 210
        legend_y = Config.SCREEN_HEIGHT - 450
        
        # Background
        pygame.draw.rect(self.screen, Config.UI_PANEL_COLOR,
                        (legend_x - 10, legend_y - 10, 200, 440))
        pygame.draw.rect(self.screen, Config.UI_BORDER_COLOR,
                        (legend_x - 10, legend_y - 10, 200, 440), 2)
        
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
        
        # Get Unicode font for settlement symbols
        unicode_font = self.get_unicode_font()
        
        # Settlement types
        settlement_types = [
            (SettlementType.FARMSTEAD, "Farmstead"),
            (SettlementType.HAMLET, "Hamlet"), 
            (SettlementType.VILLAGE, "Village"),
            (SettlementType.TOWN, "Town"),
            (SettlementType.CITY, "City"),
            (SettlementType.LOGGING_CAMP, "Logging Camp"),
            (SettlementType.MINING_CAMP, "Mining Camp"),
            (SettlementType.MONASTERY, "Monastery"),
            (SettlementType.WATCHTOWER, "Watchtower"),
            (SettlementType.RUINS_VILLAGE, "Village Ruins"),
            (SettlementType.RUINS_KEEP, "Keep Ruins"),
            (SettlementType.ANCIENT_RUINS, "Ancient Ruins"),
        ]
        
        for i, (settlement_type, name) in enumerate(settlement_types):
            y_pos = settlement_y + 25 + i * 15
            
            # Get symbol and color from config
            symbol = SETTLEMENT_SYMBOLS.get(settlement_type, "?")
            symbol_color = SETTLEMENT_COLORS.get(settlement_type, (200, 200, 200))
            
            # Try to render symbol with Unicode font, fall back if needed
            try:
                symbol_text = unicode_font.render(symbol, True, symbol_color)
                if symbol_text.get_width() == 0:
                    # Symbol didn't render, use ASCII fallback
                    fallback_symbol = "*" if settlement_type != SettlementType.FARMSTEAD else "o"
                    symbol_text = unicode_font.render(fallback_symbol, True, symbol_color) 
            except Exception:
                # Any error, use simple fallback
                fallback_symbol = "*"
                symbol_text = unicode_font.render(fallback_symbol, True, symbol_color) 
            
            self.screen.blit(symbol_text, (legend_x, y_pos))
            
            # Name
            name_text = self.legend_font.render(name, True, (180, 180, 180))
            self.screen.blit(name_text, (legend_x + 20, y_pos))

    def draw_settlement_summary(self, world_stats: Dict):
        """Draw settlement summary panel with top 3 largest settlements"""
        panel_x = 10
        panel_y = 60
        panel_width = 320  # Increased width to accommodate longer settlement info
        panel_height = 240  # Increased height for top 3 settlements
        
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
        
        # Top 3 largest settlements
        largest_settlements = world_stats.get('largest_settlements', [])
        if largest_settlements:
            text = self.settlement_font.render("Largest Settlements:", True, (220, 220, 100))
            self.screen.blit(text, (panel_x + 10, panel_y + y_offset))
            y_offset += 20
            
            for i, settlement_info in enumerate(largest_settlements):
                if i >= 3:  # Only show top 3
                    break
                    
                name = settlement_info['name']
                population = settlement_info['population']
                coordinates = settlement_info['coordinates']
                
                # Format the line as: "1. Settlement Name  x,y  (population)"
                settlement_line = f"{i + 1}. {name}  {coordinates[0]},{coordinates[1]}  ({population:,})"
                
                # Use smaller font and lighter color for settlement entries
                text = self.settlement_font.render(settlement_line, True, (180, 180, 180))
                self.screen.blit(text, (panel_x + 15, panel_y + y_offset))
                y_offset += 16
        
        y_offset += 10  # Add some spacing
        
        # Settlement breakdown by type
        settlements_by_type = world_stats.get('settlements_by_type', {})
        if settlements_by_type:
            text = self.settlement_font.render("By Type:", True, (180, 180, 180))
            self.screen.blit(text, (panel_x + 10, panel_y + y_offset))
            y_offset += 18
            
            # Sort by count, descending
            sorted_settlements = sorted(settlements_by_type.items(), 
                                      key=lambda x: x[1], reverse=True)
            
            for settlement_type, count in sorted_settlements[:5]:  # Show top 5 (reduced from 6 to fit)
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
        panel_y = 320  # Adjusted to account for taller settlement panel
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
        
        # Check for edit data
        has_edit = hasattr(hex_obj, 'edit_data') and hex_obj.edit_data
        
        # Add custom name if present
        if has_edit and hex_obj.edit_data.custom_name:
            lines.insert(0, hex_obj.edit_data.custom_name)  # Add at top
            lines[1] = f"Location: ({hex_obj.q}, {hex_obj.r})"  # Change label
        
        # Add custom description if present
        if has_edit and hex_obj.edit_data.description:
            lines.append("")  # Blank line
            # Split long descriptions into multiple lines
            desc_lines = hex_obj.edit_data.description.split('\n')
            for line in desc_lines[:3]:  # Limit to 3 lines
                if len(line) > 50:
                    line = line[:47] + "..."
                lines.append(line)
        
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
        elif not (has_edit and hex_obj.edit_data.description):
            # Only show terrain description if no custom description
            lines.append(hex_obj.terrain.description)
        
        # Add notes if present (abbreviated)
        if has_edit and hex_obj.edit_data.notes:
            lines.append("")  # Blank line
            notes = hex_obj.edit_data.notes
            if len(notes) > 60:
                notes = notes[:57] + "..."
            lines.append(f"Notes: {notes}")
        
        # Add exploration status if explored
        if hex_obj.discovery_data.explored:
            lines.append(f"Exploration Level: {hex_obj.discovery_data.exploration_level}")
        
        # Add edit indicator
        if has_edit:
            lines.append("")  # Blank line
            lines.append("[EDITED - Right-click to modify]")
        else:
            lines.append("")
            lines.append("[Right-click to edit]")
        
        # Calculate tooltip size
        max_width = max(self.tooltip_font.size(line)[0] for line in lines if line)
        tooltip_width = max_width + 20
        tooltip_height = len(lines) * 20 + 10
        
        # Position tooltip (default: right and above mouse)
        tooltip_x = mouse_x + 15
        tooltip_y = mouse_y - tooltip_height - 15
        
        # Keep tooltip on screen - adjust horizontal position
        if tooltip_x + tooltip_width > Config.SCREEN_WIDTH:
            tooltip_x = mouse_x - tooltip_width - 15  # Move to left side of mouse
        if tooltip_x < 0:
            tooltip_x = 5  # Minimum margin from left edge
        
        # Keep tooltip on screen - adjust vertical position
        if tooltip_y < 45:  # Account for top UI panel
            tooltip_y = mouse_y + 15  # Move below mouse
        if tooltip_y + tooltip_height > Config.SCREEN_HEIGHT:
            tooltip_y = Config.SCREEN_HEIGHT - tooltip_height - 5  # Move up from bottom
        
        # Draw background
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
        pygame.draw.rect(self.screen, (10, 10, 10, 240), tooltip_rect)
        
        # Different border color for edited hexes
        border_color = (100, 200, 100) if has_edit else (70, 130, 180)
        pygame.draw.rect(self.screen, border_color, tooltip_rect, 2)
        
        # Draw text
        for i, line in enumerate(lines):
            if line:  # Skip empty lines for spacing
                color = Config.TEXT_COLOR
                if has_edit and i == 0 and hex_obj.edit_data.custom_name:
                    color = (100, 255, 100)  # Green for custom name
                elif "Settlement:" in line:
                    color = (255, 215, 0)  # Gold for settlement name
                elif line.startswith("  •"):
                    color = (180, 180, 180)  # Gray for features
                elif "[" in line and "]" in line:
                    color = (150, 150, 150)  # Gray for instructions
                
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