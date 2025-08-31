"""
ui/game_window.py - Main pygame window and game loop (Updated with Settlement Features)
"""

import random
import pygame
import threading
from typing import Optional
import tkinter as tk
from tkinter import filedialog, messagebox

from config import Config
from core.hex_grid import HexCoordinate
from core.world import World
from core.viewport import Viewport
from ui.renderer import HexRenderer
from ui.panels import UIPanel
from ui.hex_editor_window import HexEditorWindow
from data.persistence import WorldPersistence
from data.hex_editor import HexEditData


def get_world_seed():
    """Import helper function"""
    from config import get_world_seed as _get_world_seed
    return _get_world_seed()


class HexGridGame:
    """Main game class managing the pygame window and game loop"""
    
    def __init__(self, world_seed: Optional[int] = None):
        pygame.init()
        Config.ensure_directories()
        
        # Use provided seed or get from config system
        if world_seed is None:
            world_seed = get_world_seed()
        
        # Setup display with seed in title if configured
        title = "Hex Explorer - Infinite World with Settlements"
        if Config.SHOW_SEED_IN_TITLE:
            title += f" (Seed: {world_seed})"
            
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game components with seed
        self.world = World(world_seed)
        self.viewport = Viewport(self.world, Config.VIEWPORT_RADIUS, Config.BUFFER_RADIUS)
        self.renderer = HexRenderer(Config.HEX_SIZE)
        self.renderer.init_fonts()
        
        # Store seed for display/saving
        self.world_seed = world_seed
        
        # UI components
        self.ui_panel = UIPanel(self.screen)
        self.camera_x = Config.SCREEN_WIDTH // 2
        self.camera_y = Config.SCREEN_HEIGHT // 2
        self.current_center = HexCoordinate(0, 0)
        self.mouse_hex = None
        self.mouse_pos = (0, 0)
        self.persistence = WorldPersistence()
        self.viewport.update(HexCoordinate(0, 0))
        
        # Editor window reference
        self.editor_window = None
        
        print(f"Hex Explorer initialized with seed: {world_seed}")
        print("Controls:")
        print("  Arrow Keys: Move camera")
        print("  Shift + Arrow: Fast movement")
        print("  Right-Click: Edit hex")
        print("  E (on hover): Edit hex")
        print("  Space: Reset to origin")
        print("  G: Print world statistics")
        print("  Ctrl+S: Save world")
        print("  Ctrl+L: Load world")
        print("  ESC: Quit")
        
    def handle_events(self):
        """Handle pygame events and input"""
        keys = pygame.key.get_pressed()
        
        # Determine camera speed
        speed = Config.CAMERA_SPEED
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            speed = Config.CAMERA_SPEED_FAST
        
        # Camera movement
        if keys[pygame.K_LEFT]:
            self.camera_x += speed
        if keys[pygame.K_RIGHT]:
            self.camera_x -= speed
        if keys[pygame.K_UP]:
            self.camera_y += speed
        if keys[pygame.K_DOWN]:
            self.camera_y -= speed
        
        # Update viewport center
        center_world_x = Config.SCREEN_WIDTH // 2 - self.camera_x
        center_world_y = Config.SCREEN_HEIGHT // 2 - self.camera_y
        new_center = self.renderer.pixel_to_hex(center_world_x, center_world_y)
        
        if new_center != self.current_center:
            self.current_center = new_center
            self.viewport.update(new_center)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                self.update_mouse_hex(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
                
    def handle_mouse_click(self, event):
        """Handle mouse click events"""
        if event.button == 3:  # Right click
            self.open_hex_editor()
        elif event.button == 1:  # Left click (future: play media)
            if self.mouse_hex:
                self.play_hex_media()
    
    def open_hex_editor(self):
        """Open the hex editor for the currently hovered hex"""
        if not self.mouse_hex:
            return
        
        # Don't open multiple editors
        if self.editor_window is not None:
            return
        
        # Get existing edit data if any
        coord = HexCoordinate(self.mouse_hex.q, self.mouse_hex.r)
        edit_data = self.world.get_hex_edit(coord)
        
        # Create editor window
        def on_save(data: HexEditData) -> bool:
            success = self.world.save_hex_edit(data)
            if success:
                print(f"Saved edit data for hex ({data.q}, {data.r})")
                # Refresh the hex to show changes
                self.viewport.update(self.current_center)
            return success
        
        def open_editor():
            """Open editor in a thread-safe way"""
            try:
                # Initialize Tk if needed
                root = tk.Tk()
                root.withdraw()  # Hide the root window
                
                # Create editor
                self.editor_window = HexEditorWindow(
                    self.mouse_hex,
                    on_save=on_save,
                    edit_data=edit_data
                )
                
                # Run the editor
                self.editor_window.root.mainloop()
                
            except Exception as e:
                print(f"Error opening editor: {e}")
            finally:
                self.editor_window = None
        
        # Run editor in separate thread to avoid blocking pygame
        editor_thread = threading.Thread(target=open_editor, daemon=True)
        editor_thread.start()
    
    def play_hex_media(self):
        """Play media associated with hex (future feature)"""
        if not self.mouse_hex:
            return
        
        # Check if hex has edit data with media
        coord = HexCoordinate(self.mouse_hex.q, self.mouse_hex.r)
        edit_data = self.world.get_hex_edit(coord)
        
        if edit_data and (edit_data.image_files or edit_data.audio_file):
            print(f"Playing media for hex ({self.mouse_hex.q}, {self.mouse_hex.r})")
            # Future: Implement media playback
        else:
            print(f"No media for hex ({self.mouse_hex.q}, {self.mouse_hex.r})")
    
    def handle_keydown(self, event):
        """Handle keyboard events"""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_SPACE:
            # Reset to origin
            self.camera_x = Config.SCREEN_WIDTH // 2
            self.camera_y = Config.SCREEN_HEIGHT // 2
            self.current_center = HexCoordinate(0, 0)
            self.viewport.update(HexCoordinate(0, 0))
        elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.save_world()
        elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.load_world()
        elif event.key == pygame.K_e:
            # Edit hex under mouse
            self.open_hex_editor()
        elif event.key == pygame.K_n:
            # Toggle settlement names
            self.renderer.toggle_settlement_names()
            print(f"Settlement names: {'ON' if self.renderer.show_settlement_names else 'OFF'}")
        elif event.key == pygame.K_i:
            # Toggle settlement icons
            self.renderer.toggle_settlement_icons()
            print(f"Settlement icons: {'ON' if self.renderer.show_settlement_icons else 'OFF'}")
        elif event.key == pygame.K_l and not (pygame.key.get_mods() & pygame.KMOD_CTRL):
            # Toggle legend (only if not Ctrl+L)
            self.ui_panel.toggle_legend()
            print(f"Legend: {'ON' if self.ui_panel.show_legend else 'OFF'}")
        elif event.key == pygame.K_p:
            # Toggle settlement panel
            self.ui_panel.toggle_settlement_panel()
            print(f"Settlement panel: {'ON' if self.ui_panel.show_settlement_panel else 'OFF'}")
        elif event.key == pygame.K_t:
            # Toggle statistics
            self.ui_panel.toggle_statistics()
            print(f"Statistics: {'ON' if self.ui_panel.show_statistics else 'OFF'}")
        elif event.key == pygame.K_g:
            # Generate settlement statistics and print to console
            self.print_world_statistics()
            
    def update_mouse_hex(self, mouse_pos):
        """Update which hex the mouse is hovering over"""
        mx, my = mouse_pos
        world_x = mx - self.camera_x
        world_y = my - self.camera_y
        
        coord = self.renderer.pixel_to_hex(world_x, world_y)
        key = coord.to_tuple()
        
        if key in self.world.hexes:
            self.mouse_hex = self.world.hexes[key]
        else:
            self.mouse_hex = None
    
    def print_world_statistics(self):
        """Print detailed world statistics to console"""
        stats = self.world.get_world_statistics()
        
        print("\n" + "="*50)
        print("WORLD STATISTICS")
        print("="*50)
        print(f"Total Hexes Generated: {stats['total_hexes']}")
        print(f"Total Settlements: {stats['total_settlements']}")
        print(f"Total Population: {stats['total_population']:,}")
        print(f"Edited Hexes: {stats.get('edited_hexes', 0)}")
        
        if stats['largest_city']:
            print(f"Largest City: {stats['largest_city']}")
        
        print(f"\nWorld Seed: {self.world.world_seed}")
        
        print("\nTERRAIN DISTRIBUTION:")
        for terrain, count in sorted(stats['terrain_distribution'].items(), 
                                   key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_hexes'] * 100) if stats['total_hexes'] > 0 else 0
            print(f"  {terrain}: {count} hexes ({percentage:.1f}%)")
        
        print("\nSETTLEMENT TYPES:")
        for settlement_type, count in sorted(stats['settlements_by_type'].items(), 
                                           key=lambda x: x[1], reverse=True):
            if count > 0:
                display_name = settlement_type.replace('_', ' ').title()
                print(f"  {display_name}: {count}")
        
        # Find some notable settlements
        cities = self.world.get_settlements_by_type('CITY')
        towns = self.world.get_settlements_by_type('TOWN')
        
        if cities:
            print(f"\nCITIES ({len(cities)}):")
            for city_hex in cities[:5]:  # Show first 5
                settlement = city_hex.settlement_data
                print(f"  {settlement.name} - Pop: {settlement.population:,} at ({city_hex.q}, {city_hex.r})")
        
        if towns:
            print(f"\nLARGE TOWNS ({len(towns)}):")
            # Sort by population
            sorted_towns = sorted(towns, key=lambda h: h.settlement_data.population, reverse=True)
            for town_hex in sorted_towns[:5]:  # Show top 5 by population
                settlement = town_hex.settlement_data
                print(f"  {settlement.name} - Pop: {settlement.population:,} at ({town_hex.q}, {town_hex.r})")
        
        # Show edited hexes
        edited_hexes = self.world.get_edited_hexes()
        if edited_hexes:
            print(f"\nEDITED HEXES ({len(edited_hexes)}):")
            for q, r in edited_hexes[:10]:  # Show first 10
                print(f"  ({q}, {r})")
        
        print("="*50)
    
    def save_world(self):
        """Save world with file dialog"""
        def save_thread():
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir=Config.SAVE_DIR
            )
            if filename:
                try:
                    self.persistence.save_world(self.world, self.viewport, filename)
                    stats = self.world.get_world_statistics()
                    print(f"World saved to {filename}")
                    print(f"Saved {stats['total_hexes']} hexes with {stats['total_settlements']} settlements")
                    print(f"Edited hexes: {stats.get('edited_hexes', 0)}")
                except Exception as e:
                    messagebox.showerror("Save Error", f"Failed to save world: {e}")
        
        threading.Thread(target=save_thread, daemon=True).start()
    
    def load_world(self):
        """Load world with file dialog"""
        def load_thread():
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir=Config.SAVE_DIR
            )
            if filename:
                try:
                    self.world, viewport_center = self.persistence.load_world(filename)
                    self.viewport = Viewport(self.world, Config.VIEWPORT_RADIUS, Config.BUFFER_RADIUS)
                    self.viewport.update(viewport_center)
                    
                    # Reset camera to loaded position
                    px, py = self.renderer.hex_to_pixel(viewport_center)
                    self.camera_x = Config.SCREEN_WIDTH // 2 - px
                    self.camera_y = Config.SCREEN_HEIGHT // 2 - py
                    self.current_center = viewport_center
                    
                    stats = self.world.get_world_statistics()
                    print(f"World loaded from {filename}")
                    print(f"Loaded {stats['total_hexes']} hexes with {stats['total_settlements']} settlements")
                    print(f"Edited hexes: {stats.get('edited_hexes', 0)}")
                    
                except Exception as e:
                    messagebox.showerror("Load Error", f"Failed to load world: {e}")
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def draw(self):
        """Main draw method"""
        # Clear screen
        self.screen.fill(Config.BACKGROUND_COLOR)
        
        # Draw visible hexes
        visible_hexes = self.viewport.get_visible_hexes()
        for hex_obj in visible_hexes:
            # Check if hex has edit data for special rendering
            has_edit = hasattr(hex_obj, 'edit_data') and hex_obj.edit_data
            self.renderer.draw_hex(self.screen, hex_obj, self.camera_x, self.camera_y, 
                                  show_coords=True, has_edit=has_edit)
        
        # Get world statistics for UI
        world_stats = self.world.get_world_statistics()
        
        # Draw UI elements
        self.ui_panel.draw(
            viewport_center=self.current_center,
            hex_count=len(self.world.hexes),
            mouse_hex=self.mouse_hex,
            world_stats=world_stats
        )
        
        # Draw crosshair
        self.draw_crosshair()
        
        pygame.display.flip()
    
    def draw_crosshair(self):
        """Draw crosshair at screen center"""
        center_x = Config.SCREEN_WIDTH // 2
        center_y = Config.SCREEN_HEIGHT // 2
        color = (100, 100, 100)
        pygame.draw.line(self.screen, color, 
                        (center_x - 10, center_y), (center_x + 10, center_y), 1)
        pygame.draw.line(self.screen, color,
                        (center_x, center_y - 10), (center_x, center_y + 10), 1)
    
    def run(self):
        """Main game loop"""
        print(f"\nStarting exploration at world seed: {self.world.world_seed}")
        print("Right-click any hex to edit it!")
        
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(Config.FPS)
        
        # Print final statistics
        print(f"\nFinal exploration statistics:")
        self.print_world_statistics()
        
        pygame.quit()