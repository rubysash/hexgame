"""
ui/game_window.py - Main pygame window and game loop (Updated with Settlement Features)
"""

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
from data.persistence import WorldPersistence

class HexGridGame:
    """Main game class managing the pygame window and game loop"""
    
    def __init__(self):
        pygame.init()
        Config.ensure_directories()
        
        # Setup display
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Hex Explorer - Infinite World with Settlements")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game components
        self.world = World(Config.DEFAULT_WORLD_SEED)
        self.viewport = Viewport(self.world, Config.VIEWPORT_RADIUS, Config.BUFFER_RADIUS)
        self.renderer = HexRenderer(Config.HEX_SIZE)
        self.renderer.init_fonts()
        
        # UI components
        self.ui_panel = UIPanel(self.screen)
        
        # Camera position (in pixels, centered on origin)
        self.camera_x = Config.SCREEN_WIDTH // 2
        self.camera_y = Config.SCREEN_HEIGHT // 2
        
        # Current state
        self.current_center = HexCoordinate(0, 0)
        self.mouse_hex = None
        
        # Persistence
        self.persistence = WorldPersistence()
        
        # Initialize viewport
        self.viewport.update(HexCoordinate(0, 0))
        
        print("Hex Explorer initialized with settlement system!")
        print("Controls:")
        print("  Arrow Keys: Move camera")
        print("  Shift + Arrow: Fast movement")
        print("  Space: Reset to origin")
        print("  N: Toggle settlement names")
        print("  I: Toggle settlement icons") 
        print("  L: Toggle legend")
        print("  P: Toggle settlement panel")
        print("  S: Toggle statistics")
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
                self.update_mouse_hex(event.pos)
                
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
            # Always show coordinates since settlement names are disabled by default
            self.renderer.draw_hex(self.screen, hex_obj, self.camera_x, self.camera_y, show_coords=True)
        
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
        print("Move around to discover new settlements!")
        
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(Config.FPS)
        
        # Print final statistics
        print(f"\nFinal exploration statistics:")
        self.print_world_statistics()
        
        pygame.quit()