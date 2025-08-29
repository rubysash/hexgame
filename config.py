"""
config.py - Global configuration settings
"""

import os
from enum import Enum

class Config:
    """Global configuration settings"""
    
    # Display settings
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    FPS = 60
    
    # Hex settings
    HEX_SIZE = 35
    VIEWPORT_RADIUS = 15  # Hexes visible in each direction
    BUFFER_RADIUS = 20    # Hexes to keep loaded
    
    # Camera settings
    CAMERA_SPEED = 5
    CAMERA_SPEED_FAST = 15
    
    # File paths
    SAVE_DIR = "saves/"
    CAMPAIGN_DIR = "campaigns/"
    TEMPLATE_DIR = "resources/templates/"
    
    # Colors
    BACKGROUND_COLOR = (30, 30, 30)
    UI_PANEL_COLOR = (20, 20, 20)
    UI_BORDER_COLOR = (60, 60, 60)
    TEXT_COLOR = (200, 200, 200)
    
    # Game settings
    DEFAULT_WORLD_SEED = None  # Random if None
    
    # Future: GURPS integration
    MOVEMENT_POINTS_PER_DAY = 8
    BASE_VISIBILITY_RANGE = 3
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        os.makedirs(cls.SAVE_DIR, exist_ok=True)
        os.makedirs(cls.CAMPAIGN_DIR, exist_ok=True)
        os.makedirs(cls.TEMPLATE_DIR, exist_ok=True)