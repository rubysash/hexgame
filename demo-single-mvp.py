"""
Hex Grid MVP - Pygame Version with Infinite World and Save/Load
================================================================
Run with: python hex_grid_game.py
Required: pip install pygame
"""

import pygame
import math
import json
import os
from enum import Enum
import random
from typing import Dict, Tuple, Optional, List
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

# Hide tkinter root window
tk_root = tk.Tk()
tk_root.withdraw()

# Terrain types with colors and generation rules
class TerrainType(Enum):
    PLAINS = ("Plains", (144, 238, 144), "Flat grasslands suitable for travel", 30)
    FOREST = ("Forest", (34, 139, 34), "Dense woodland with abundant resources", 25)
    HILLS = ("Hills", (205, 133, 63), "Rolling hills with moderate elevation", 20)
    MOUNTAINS = ("Mountains", (139, 115, 85), "Towering peaks difficult to traverse", 10)
    WATER = ("Water", (70, 130, 180), "Lakes and rivers providing fresh water", 10)
    DESERT = ("Desert", (244, 164, 96), "Arid wasteland with scarce resources", 5)
    
    def __init__(self, display_name, color, description, weight):
        self.display_name = display_name
        self.color = color
        self.description = description
        self.weight = weight

# Neighbor influence weights - what terrain likes to be next to what
NEIGHBOR_WEIGHTS = {
    TerrainType.PLAINS: {
        TerrainType.PLAINS: 1.5,
        TerrainType.FOREST: 1.2,
        TerrainType.HILLS: 1.0,
        TerrainType.MOUNTAINS: 0.3,
        TerrainType.WATER: 1.0,
        TerrainType.DESERT: 0.7
    },
    TerrainType.FOREST: {
        TerrainType.PLAINS: 1.0,
        TerrainType.FOREST: 2.0,
        TerrainType.HILLS: 1.3,
        TerrainType.MOUNTAINS: 0.5,
        TerrainType.WATER: 1.5,
        TerrainType.DESERT: 0.1
    },
    TerrainType.HILLS: {
        TerrainType.PLAINS: 0.8,
        TerrainType.FOREST: 1.0,
        TerrainType.HILLS: 1.5,
        TerrainType.MOUNTAINS: 2.0,
        TerrainType.WATER: 0.6,
        TerrainType.DESERT: 0.4
    },
    TerrainType.MOUNTAINS: {
        TerrainType.PLAINS: 0.2,
        TerrainType.FOREST: 0.5,
        TerrainType.HILLS: 2.0,
        TerrainType.MOUNTAINS: 2.5,
        TerrainType.WATER: 0.8,
        TerrainType.DESERT: 0.3
    },
    TerrainType.WATER: {
        TerrainType.PLAINS: 1.2,
        TerrainType.FOREST: 1.5,
        TerrainType.HILLS: 0.5,
        TerrainType.MOUNTAINS: 0.8,
        TerrainType.WATER: 2.0,
        TerrainType.DESERT: 0.1
    },
    TerrainType.DESERT: {
        TerrainType.PLAINS: 0.7,
        TerrainType.FOREST: 0.1,
        TerrainType.HILLS: 0.5,
        TerrainType.MOUNTAINS: 0.3,
        TerrainType.WATER: 0.1,
        TerrainType.DESERT: 2.5
    }
}

class Hex:
    """Represents a single hex in the grid"""
    def __init__(self, q: int, r: int, terrain: TerrainType):
        self.q = q  # Axial coordinate q
        self.r = r  # Axial coordinate r
        self.s = -q - r  # Axial coordinate s (for cubic coordinates)
        self.terrain = terrain
        self.id = f"{q},{r}"
        
    def to_dict(self):
        """Convert hex to dictionary for JSON serialization"""
        return {
            'q': self.q,
            'r': self.r,
            'terrain': self.terrain.name
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create hex from dictionary"""
        return cls(
            data['q'],
            data['r'],
            TerrainType[data['terrain']]
        )

class InfiniteHexGrid:
    """Manages an infinite hex grid with lazy loading"""
    def __init__(self, hex_size: int = 35):
        self.hex_size = hex_size
        self.hexes: Dict[Tuple[int, int], Hex] = {}
        self.viewport_center = (0, 0)  # q, r coordinates
        self.viewport_radius = 15  # Hexes to show in each direction
        self.buffer_radius = 20  # Hexes to keep loaded
        self.world_seed = random.randint(0, 1000000)
        
    def get_hex(self, q: int, r: int) -> Hex:
        """Get or generate a hex at the given coordinates"""
        if (q, r) not in self.hexes:
            self.generate_hex(q, r)
        return self.hexes[(q, r)]
    
    def generate_hex(self, q: int, r: int):
        """Generate a new hex with terrain based on neighbors"""
        # Set seed based on position for consistent generation
        random.seed(self.world_seed + q * 10000 + r)
        
        # Get neighbor terrains
        neighbors = self.get_neighbor_terrains(q, r)
        
        # Calculate weighted probabilities
        weights = {}
        for terrain_type in TerrainType:
            weights[terrain_type] = terrain_type.weight
            
        # Apply neighbor influences
        for neighbor_terrain in neighbors:
            for terrain_type in TerrainType:
                weights[terrain_type] *= NEIGHBOR_WEIGHTS[neighbor_terrain][terrain_type]
        
        # Select terrain type
        total_weight = sum(weights.values())
        rand_val = random.random() * total_weight
        
        current_weight = 0
        selected_terrain = TerrainType.PLAINS
        for terrain_type, weight in weights.items():
            current_weight += weight
            if rand_val <= current_weight:
                selected_terrain = terrain_type
                break
        
        self.hexes[(q, r)] = Hex(q, r, selected_terrain)
        
        # Reset random seed
        random.seed()
    
    def get_neighbor_terrains(self, q: int, r: int) -> List[TerrainType]:
        """Get terrain types of neighboring hexes"""
        neighbors = []
        # Axial coordinate neighbors
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        
        for dq, dr in directions:
            nq, nr = q + dq, r + dr
            if (nq, nr) in self.hexes:
                neighbors.append(self.hexes[(nq, nr)].terrain)
                
        return neighbors
    
    def update_viewport(self, center_q: int, center_r: int):
        """Update viewport center and load/unload hexes as needed"""
        self.viewport_center = (center_q, center_r)
        
        # Load hexes in buffer radius using cube coordinates for proper distance
        for q in range(center_q - self.buffer_radius, center_q + self.buffer_radius + 1):
            for r in range(center_r - self.buffer_radius, center_r + self.buffer_radius + 1):
                s = -q - r
                # Use cube coordinate distance
                distance = (abs(q - center_q) + abs(r - center_r) + abs(s - (-center_q - center_r))) / 2
                if distance <= self.buffer_radius:
                    if (q, r) not in self.hexes:
                        self.generate_hex(q, r)
        
        # Optional: Unload distant hexes to save memory
        # keys_to_remove = []
        # for (q, r) in self.hexes.keys():
        #     s = -q - r
        #     distance = (abs(q - center_q) + abs(r - center_r) + abs(s - (-center_q - center_r))) / 2
        #     if distance > self.buffer_radius * 2:
        #         keys_to_remove.append((q, r))
        # for key in keys_to_remove:
        #     del self.hexes[key]
        
    def get_visible_hexes(self) -> List[Hex]:
        """Get list of hexes visible in current viewport"""
        visible = []
        center_q, center_r = self.viewport_center
        
        for q in range(center_q - self.viewport_radius, center_q + self.viewport_radius + 1):
            for r in range(center_r - self.viewport_radius, center_r + self.viewport_radius + 1):
                s = -q - r
                # Use cube coordinate distance for circular viewport
                distance = (abs(q - center_q) + abs(r - center_r) + abs(s - (-center_q - center_r))) / 2
                if distance <= self.viewport_radius:
                    visible.append(self.get_hex(q, r))
                    
        return visible
    
    def save_world(self, filename: str):
        """Save the world to a JSON file"""
        data = {
            'seed': self.world_seed,
            'viewport_center': self.viewport_center,
            'hexes': [hex_obj.to_dict() for hex_obj in self.hexes.values()]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_world(self, filename: str):
        """Load the world from a JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.world_seed = data['seed']
        self.viewport_center = tuple(data['viewport_center'])
        self.hexes = {}
        
        for hex_data in data['hexes']:
            hex_obj = Hex.from_dict(hex_data)
            self.hexes[(hex_obj.q, hex_obj.r)] = hex_obj

class HexRenderer:
    """Handles rendering of hexes to pygame surface"""
    def __init__(self, hex_size: int = 35):
        self.hex_size = hex_size
        self.hex_height = hex_size * 2
        self.hex_width = math.sqrt(3) * hex_size
        self.font = None
        
    def init_font(self):
        """Initialize pygame font (must be called after pygame.init())"""
        pygame.font.init()
        self.font = pygame.font.Font(None, 16)
        
    def hex_to_pixel(self, q: int, r: int) -> Tuple[float, float]:
        """Convert hex coordinates to pixel coordinates"""
        x = self.hex_size * (3/2 * q)
        y = self.hex_size * (math.sqrt(3) * (r + q/2))
        return x, y
    
    def pixel_to_hex(self, x: float, y: float) -> Tuple[int, int]:
        """Convert pixel coordinates to hex coordinates"""
        # Convert to fractional axial coordinates
        q = (2/3 * x) / self.hex_size
        r = (-1/3 * x + math.sqrt(3)/3 * y) / self.hex_size
        
        # Round to nearest hex
        return self.axial_round(q, r)
    
    def axial_round(self, q: float, r: float) -> Tuple[int, int]:
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
            
        return rq, rr
    
    def draw_hexagon(self, surface: pygame.Surface, center_x: float, center_y: float, color: Tuple[int, int, int]):
        """Draw a hexagon at the given center position"""
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            x = center_x + self.hex_size * math.cos(angle)
            y = center_y + self.hex_size * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (50, 50, 50), points, 2)
        
    def draw_hex(self, surface: pygame.Surface, hex_obj: Hex, camera_x: float, camera_y: float):
        """Draw a single hex with its terrain color and coordinates"""
        pixel_x, pixel_y = self.hex_to_pixel(hex_obj.q, hex_obj.r)
        screen_x = pixel_x + camera_x
        screen_y = pixel_y + camera_y
        
        self.draw_hexagon(surface, screen_x, screen_y, hex_obj.terrain.color)
        
        # Draw coordinates
        if self.font:
            text = f"{hex_obj.q},{hex_obj.r}"
            text_surface = self.font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(screen_x, screen_y))
            surface.blit(text_surface, text_rect)

class HexGridGame:
    """Main game class managing the pygame window and game loop"""
    def __init__(self):
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Hex Grid Explorer - Infinite World")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize components
        self.grid = InfiniteHexGrid()
        self.renderer = HexRenderer()
        self.renderer.init_font()
        
        # Camera position (in pixels, centered on origin)
        self.camera_x = self.screen_width // 2
        self.camera_y = self.screen_height // 2
        
        # Current viewport center in hex coordinates
        self.current_center_q = 0
        self.current_center_r = 0
        
        # UI elements
        self.ui_font = pygame.font.Font(None, 24)
        self.tooltip_font = pygame.font.Font(None, 18)
        self.mouse_hex = None
        
        # Initialize viewport
        self.grid.update_viewport(0, 0)
        
        # Movement
        self.camera_speed = 5
        
    def handle_events(self):
        """Handle pygame events"""
        keys = pygame.key.get_pressed()
        
        # Camera movement with arrow keys
        if keys[pygame.K_LEFT]:
            self.camera_x += self.camera_speed
        if keys[pygame.K_RIGHT]:
            self.camera_x -= self.camera_speed
        if keys[pygame.K_UP]:
            self.camera_y += self.camera_speed
        if keys[pygame.K_DOWN]:
            self.camera_y -= self.camera_speed
            
        # Faster movement with shift
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            temp_speed = self.camera_speed * 3
            if keys[pygame.K_LEFT]:
                self.camera_x += temp_speed - self.camera_speed
            if keys[pygame.K_RIGHT]:
                self.camera_x -= temp_speed - self.camera_speed
            if keys[pygame.K_UP]:
                self.camera_y += temp_speed - self.camera_speed
            if keys[pygame.K_DOWN]:
                self.camera_y -= temp_speed - self.camera_speed
        
        # Calculate which hex is at screen center
        center_world_x = self.screen_width // 2 - self.camera_x
        center_world_y = self.screen_height // 2 - self.camera_y
        center_q, center_r = self.renderer.pixel_to_hex(center_world_x, center_world_y)
        
        # Update viewport if center has moved
        if (center_q, center_r) != (self.current_center_q, self.current_center_r):
            self.current_center_q = center_q
            self.current_center_r = center_r
            self.grid.update_viewport(center_q, center_r)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.save_world()
                elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.load_world()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Reset camera to origin
                    self.camera_x = self.screen_width // 2
                    self.camera_y = self.screen_height // 2
                    self.grid.update_viewport(0, 0)
            elif event.type == pygame.MOUSEMOTION:
                self.update_mouse_hex(event.pos)
                
    def update_mouse_hex(self, mouse_pos):
        """Update which hex the mouse is hovering over"""
        mx, my = mouse_pos
        # Convert mouse position to world coordinates
        world_x = mx - self.camera_x
        world_y = my - self.camera_y
        
        # Convert to hex coordinates
        q, r = self.renderer.pixel_to_hex(world_x, world_y)
        
        # Check if this hex exists
        if (q, r) in self.grid.hexes:
            self.mouse_hex = self.grid.hexes[(q, r)]
        else:
            self.mouse_hex = None
    
    def save_world(self):
        """Open file dialog to save world"""
        def save_thread():
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                try:
                    self.grid.save_world(filename)
                    print(f"World saved to {filename}")
                except Exception as e:
                    messagebox.showerror("Save Error", f"Failed to save world: {e}")
        
        # Run in thread to not block game loop
        threading.Thread(target=save_thread, daemon=True).start()
    
    def load_world(self):
        """Open file dialog to load world"""
        def load_thread():
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                try:
                    self.grid.load_world(filename)
                    # Reset camera to loaded viewport center
                    q, r = self.grid.viewport_center
                    px, py = self.renderer.hex_to_pixel(q, r)
                    self.camera_x = self.screen_width // 2 - px
                    self.camera_y = self.screen_height // 2 - py
                    self.current_center_q = q
                    self.current_center_r = r
                    print(f"World loaded from {filename}")
                except Exception as e:
                    messagebox.showerror("Load Error", f"Failed to load world: {e}")
        
        # Run in thread to not block game loop
        threading.Thread(target=load_thread, daemon=True).start()
    
    def draw(self):
        """Draw the game screen"""
        # Clear screen
        self.screen.fill((30, 30, 30))
        
        # Draw visible hexes
        visible_hexes = self.grid.get_visible_hexes()
        for hex_obj in visible_hexes:
            self.renderer.draw_hex(self.screen, hex_obj, self.camera_x, self.camera_y)
        
        # Draw crosshair at center
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        pygame.draw.line(self.screen, (100, 100, 100), (center_x - 10, center_y), (center_x + 10, center_y), 1)
        pygame.draw.line(self.screen, (100, 100, 100), (center_x, center_y - 10), (center_x, center_y + 10), 1)
        
        # Draw UI panel
        panel_rect = pygame.Rect(0, 0, self.screen_width, 40)
        pygame.draw.rect(self.screen, (20, 20, 20), panel_rect)
        pygame.draw.line(self.screen, (60, 60, 60), (0, 40), (self.screen_width, 40), 2)
        
        # Draw instructions
        instructions = "Arrow Keys: Move | Shift: Fast | Space: Reset | Ctrl+S: Save | Ctrl+L: Load | ESC: Quit"
        text = self.ui_font.render(instructions, True, (200, 200, 200))
        self.screen.blit(text, (10, 10))
        
        # Draw viewport info
        vp_text = f"Viewport: ({self.current_center_q}, {self.current_center_r}) | Hexes Loaded: {len(self.grid.hexes)}"
        text = self.ui_font.render(vp_text, True, (150, 150, 150))
        self.screen.blit(text, (self.screen_width - 350, 10))
        
        # Draw tooltip for hovered hex
        if self.mouse_hex:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            tooltip_lines = [
                f"Hex ({self.mouse_hex.q}, {self.mouse_hex.r})",
                f"Terrain: {self.mouse_hex.terrain.display_name}",
                self.mouse_hex.terrain.description
            ]
            
            # Calculate tooltip size
            max_width = max(self.tooltip_font.size(line)[0] for line in tooltip_lines)
            tooltip_height = len(tooltip_lines) * 20 + 10
            
            # Adjust tooltip position to stay on screen
            tooltip_x = mouse_x + 10
            tooltip_y = mouse_y - tooltip_height - 10
            
            if tooltip_x + max_width + 20 > self.screen_width:
                tooltip_x = mouse_x - max_width - 30
            if tooltip_y < 50:
                tooltip_y = mouse_y + 10
            
            # Draw tooltip background
            tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, max_width + 20, tooltip_height)
            pygame.draw.rect(self.screen, (10, 10, 10), tooltip_rect)
            pygame.draw.rect(self.screen, (70, 130, 180), tooltip_rect, 2)
            
            # Draw tooltip text
            for i, line in enumerate(tooltip_lines):
                text = self.tooltip_font.render(line, True, (200, 200, 200))
                self.screen.blit(text, (tooltip_x + 10, tooltip_y + 5 + i * 20))
        
        # Draw legend in bottom right
        legend_x = self.screen_width - 250
        legend_y = self.screen_height - 200
        
        pygame.draw.rect(self.screen, (20, 20, 20), (legend_x - 10, legend_y - 10, 240, 190))
        pygame.draw.rect(self.screen, (60, 60, 60), (legend_x - 10, legend_y - 10, 240, 190), 2)
        
        legend_title = self.ui_font.render("Terrain Types", True, (200, 200, 200))
        self.screen.blit(legend_title, (legend_x, legend_y - 5))
        
        for i, terrain_type in enumerate(TerrainType):
            y_pos = legend_y + 25 + i * 25
            # Draw color sample
            pygame.draw.rect(self.screen, terrain_type.color, (legend_x, y_pos, 20, 20))
            pygame.draw.rect(self.screen, (60, 60, 60), (legend_x, y_pos, 20, 20), 1)
            # Draw terrain name
            text = self.tooltip_font.render(terrain_type.display_name, True, (180, 180, 180))
            self.screen.blit(text, (legend_x + 30, y_pos + 2))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()

def main():
    """Entry point for the application"""
    game = HexGridGame()
    game.run()

if __name__ == "__main__":
    main()