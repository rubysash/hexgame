"""
ui/renderer.py - Hex rendering utilities (Updated with Settlement Display)
"""

import pygame
import math
from typing import Tuple
from core.hex_grid import HexCoordinate
from data.models import Hex, SettlementType
from generation.config_data import SETTLEMENT_SYMBOLS, SETTLEMENT_COLORS

# Add this to your main game initialization for debugging
def debug_fonts(self):
    """Debug helper to see what's available"""
    print("=== FONT DEBUG INFO ===")
    
    # List all available system fonts
    available_fonts = pygame.font.get_fonts()
    print(f"System has {len(available_fonts)} fonts available")
    
    # Look for common Unicode fonts
    unicode_fonts = ['dejavu', 'noto', 'arial', 'liberation', 'segoe']
    found_unicode_fonts = []
    
    for font_family in unicode_fonts:
        matches = [f for f in available_fonts if font_family in f.lower()]
        if matches:
            found_unicode_fonts.extend(matches)
            print(f"Found {font_family} variants: {matches}")
    
    if not found_unicode_fonts:
        print("⚠ No common Unicode fonts found")
        print("Consider installing: DejaVu Sans, Noto Sans, or Liberation Sans")
    
    print("=" * 23)

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
        self.show_settlement_names = False  # Disabled by default - use tooltips instead
        self.show_settlement_icons = True
        self.show_population = False
        
    def init_fonts(self):
        """Initialize pygame fonts with Unicode support and comprehensive symbol testing"""
        pygame.font.init()
        
        # Import here to avoid circular imports
        from generation.config_data import SETTLEMENT_SYMBOLS
        
        # Try to load fonts with good Unicode support
        unicode_fonts = [
            'DejaVu Sans',      # Good Unicode coverage
            'Arial Unicode MS', # Windows
            'Noto Sans',        # Google Noto fonts
            'Liberation Sans',  # Linux
            'Segoe UI Symbol',  # Windows symbols
            'Apple Symbols',    # macOS
            'Arial',            # Fallback
        ]
        
        # Test all settlement symbols with each font
        self.unicode_font = None
        best_font_name = None
        best_success_count = 0
        
        for font_name in unicode_fonts:
            try:
                test_font = pygame.font.SysFont(font_name, 14)
                if test_font is None:
                    print(f"Font '{font_name}' not found on system")
                    continue
                    
                successful_symbols = []
                failed_symbols = []
                
                # Test each settlement symbol
                for settlement_type, symbol in SETTLEMENT_SYMBOLS.items():
                    try:
                        test_surface = test_font.render(symbol, True, (255, 255, 255))
                        if test_surface.get_width() > 0:
                            successful_symbols.append((settlement_type.name, symbol))
                        else:
                            failed_symbols.append((settlement_type.name, symbol))
                    except Exception as e:
                        failed_symbols.append((settlement_type.name, symbol, str(e)))
                
                success_count = len(successful_symbols)
                total_count = len(SETTLEMENT_SYMBOLS)
                
                print(f"Font '{font_name}': {success_count}/{total_count} symbols rendered successfully")
                
                # Log failed symbols for this font
                if failed_symbols:
                    print(f"  Failed symbols for '{font_name}':")
                    for failure in failed_symbols:
                        if len(failure) == 3:  # Has error message
                            settlement_name, symbol, error = failure
                            print(f"    {settlement_name}: '{symbol}' (Error: {error})")
                        else:
                            settlement_name, symbol = failure
                            print(f"    {settlement_name}: '{symbol}' (Width = 0, likely not supported)")
                
                # Keep track of the best font so far
                if success_count > best_success_count:
                    best_success_count = success_count
                    best_font_name = font_name
                    self.unicode_font = test_font
                    
                # If we found a font that renders all symbols, use it
                if success_count == total_count:
                    print(f"✓ Perfect match found: '{font_name}' renders all settlement symbols!")
                    break
                    
            except Exception as e:
                print(f"Error testing font '{font_name}': {e}")
                continue
        
        # Final font selection and reporting
        if self.unicode_font:
            print(f"\n✓ Selected font: '{best_font_name}' ({best_success_count}/{len(SETTLEMENT_SYMBOLS)} symbols)")
            if best_success_count < len(SETTLEMENT_SYMBOLS):
                print(f"⚠ Warning: {len(SETTLEMENT_SYMBOLS) - best_success_count} symbols may not display correctly")
                print("  Consider using ASCII fallback symbols or installing better Unicode fonts")
        else:
            print("\n✗ No suitable Unicode font found!")
            print("  All settlement symbols will use ASCII fallbacks")
            print("  Consider installing 'DejaVu Sans' or 'Noto Sans' fonts for better symbol support")
        
        # Set up standard fonts
        self.font = pygame.font.Font(None, 12)
        self.small_font = pygame.font.Font(None, 12) 
        self.settlement_font = self.unicode_font if self.unicode_font else pygame.font.Font(None, 14)
        
        # Test the final selected font one more time for user feedback
        if self.unicode_font:
            print("\nFinal symbol test with selected font:")
            for settlement_type, symbol in SETTLEMENT_SYMBOLS.items():
                try:
                    test_surface = self.unicode_font.render(symbol, True, (255, 255, 255))
                    status = "✓" if test_surface.get_width() > 0 else "✗"
                    print(f"  {status} {settlement_type.name}: '{symbol}'")
                except Exception as e:
                    print(f"  ✗ {settlement_type.name}: '{symbol}' (Error: {e})")

    def get_font_info(self):
        """Get information about available fonts (debugging helper)"""
        available_fonts = pygame.font.get_fonts()
        print(f"\nAvailable system fonts ({len(available_fonts)}):")
        for font in sorted(available_fonts)[:20]:  # Show first 20
            print(f"  {font}")
        if len(available_fonts) > 20:
            print(f"  ... and {len(available_fonts) - 20} more")
        
        return available_fonts

    def draw_settlement_icon(self, surface: pygame.Surface, center_x: float, 
                        center_y: float, settlement_type: SettlementType, population: int = 0):
        """Draw settlement icon using Unicode or ASCII fallback"""
        if not self.show_settlement_icons:
            return
        
        # Get symbol and color from config
        symbol = SETTLEMENT_SYMBOLS.get(settlement_type, "?")
        symbol_color = SETTLEMENT_COLORS.get(settlement_type, (200, 200, 200))
        
        # Size scaling
        base_size = 12
        if settlement_type == SettlementType.CITY:
            font_size = min(20, base_size + population // 500)
        elif settlement_type == SettlementType.TOWN:
            font_size = min(18, base_size + population // 200)
        elif settlement_type == SettlementType.VILLAGE:
            font_size = min(16, base_size + population // 100)
        elif settlement_type in [SettlementType.HAMLET, SettlementType.FARMSTEAD]:
            font_size = max(10, base_size + population // 20)
        elif settlement_type.name.startswith('RUINS'):
            font_size = 11
        else:
            font_size = 14
        
        # Choose font based on symbol complexity
        if self.unicode_font and len(symbol.encode('utf-8')) > 1:
            # Use Unicode font for complex symbols
            try:
                icon_font = pygame.font.SysFont(self.unicode_font.get_fonts()[0], font_size)
            except:
                icon_font = self.unicode_font
        else:
            # Use default font for simple ASCII
            try:
                icon_font = pygame.font.Font(None, font_size)
            except:
                icon_font = self.settlement_font or self.font
        
        # Move icon slightly above center
        icon_y = center_y - 8
        
        # Test if symbol renders properly
        try:
            text_surface = icon_font.render(symbol, True, symbol_color)
            if text_surface.get_width() == 0:
                # Symbol didn't render, use fallback
                fallback_symbol = "*" if settlement_type != SettlementType.FARMSTEAD else "o"
                text_surface = icon_font.render(fallback_symbol, True, symbol_color)
        except:
            # Fallback for any rendering error
            fallback_symbol = "*"
            text_surface = self.font.render(fallback_symbol, True, symbol_color)
        
        text_rect = text_surface.get_rect(center=(int(center_x), int(icon_y)))
        
        # Add subtle background for better visibility
        bg_rect = text_rect.copy()
        bg_rect.inflate_ip(2, 1)
        pygame.draw.rect(surface, (0, 0, 0, 80), bg_rect)
        
        # Draw the symbol
        surface.blit(text_surface, text_rect)
        
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
                camera_x: float, camera_y: float, show_coords: bool = True,
                has_edit: bool = False):
        """Draw a single hex with its terrain color, settlements, and optional coordinates"""
        coord = HexCoordinate(hex_obj.q, hex_obj.r)
        pixel_x, pixel_y = self.hex_to_pixel(coord)
        screen_x = pixel_x + camera_x
        screen_y = pixel_y + camera_y
        
        # Draw the hexagon
        border_color = (50, 50, 50)
        if has_edit:
            border_color = (100, 200, 100)  # Green border for edited hexes
        elif hex_obj.has_settlement:
            border_color = (100, 100, 100)  # Lighter border for settlements
        
        self.draw_hexagon(surface, screen_x, screen_y, hex_obj.terrain.color, border_color)
        
        # Draw edit indicator if hex has been edited
        if has_edit:
            # Draw a small "E" in the top-left corner
            if self.small_font:
                edit_indicator = self.small_font.render("E", True, (100, 255, 100))
                surface.blit(edit_indicator, (screen_x - self.hex_size + 5, screen_y - self.hex_size + 5))
        
        # Draw settlement if present
        if hex_obj.has_settlement:
            self.draw_settlement_icon(surface, screen_x, screen_y, 
                                    hex_obj.settlement_data.settlement_type)
        
        # Draw coordinates below center
        if show_coords and self.font:
            text = f"{hex_obj.q},{hex_obj.r}"
            text_surface = self.font.render(text, True, (0, 0, 0))
            text_y = screen_y + 10
            text_rect = text_surface.get_rect(center=(screen_x, text_y))
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