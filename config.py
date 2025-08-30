"""
config.py - Global configuration settings
"""
import hashlib
import argparse
import random
import os
from typing import Optional

# Updated config.py
class Config:
    """Global configuration settings with enhanced seed support"""
    
    # Display settings
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    FPS = 60
    
    # Hex settings
    HEX_SIZE = 35
    VIEWPORT_RADIUS = 15
    BUFFER_RADIUS = 20
    
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
    
    # Game settings - Enhanced seed configuration
    DEFAULT_WORLD_SEED = None  # None means random
    SHOW_SEED_IN_TITLE = True  # Display seed in window title
    
    # GURPS integration
    MOVEMENT_POINTS_PER_DAY = 8
    BASE_VISIBILITY_RANGE = 3
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        os.makedirs(cls.SAVE_DIR, exist_ok=True)
        os.makedirs(cls.CAMPAIGN_DIR, exist_ok=True)
        os.makedirs(cls.TEMPLATE_DIR, exist_ok=True)
    
    @classmethod
    def parse_seed(cls, seed_input: str) -> Optional[int]:
        """
        Parse seed from string input with deterministic hashing.
        Returns None if invalid or empty.
        """
        if not seed_input:
            return None
            
        seed_input = seed_input.strip()
        if not seed_input:
            return None
        
        try:
            # Handle numeric seeds directly
            seed = int(seed_input)
            # Ensure seed is within reasonable bounds
            if seed < -2147483648 or seed > 2147483647:
                print(f"Warning: Seed {seed} is out of range, using truncated value")
                seed = seed & 0x7FFFFFFF  # Keep it within 32-bit signed range
            return seed
        except ValueError:
            # Use deterministic hashing for string seeds
            if len(seed_input) <= 50:  # Reasonable length limit
                # Use SHA-256 for deterministic hashing across Python sessions
                hash_object = hashlib.sha256(seed_input.encode('utf-8'))
                hex_dig = hash_object.hexdigest()
                # Take first 8 hex characters and convert to int
                seed = int(hex_dig[:8], 16) % 1000000
                print(f"String seed '{seed_input}' hashed to: {seed}")
                return seed
            else:
                print(f"Warning: Seed string too long, using random seed")
                return None


def get_world_seed() -> int:
    """
    Get world seed using priority order:
    1. Command line argument (--seed)
    2. Environment variable (HEX_WORLD_SEED) 
    3. Config.DEFAULT_WORLD_SEED
    4. Random generation
    """
    
    # 1. Check command line arguments first
    parser = argparse.ArgumentParser(description='Hex Explorer - Infinite World Generator')
    parser.add_argument('--seed', '-s', 
                       type=str, 
                       help='World generation seed (integer or string)')
    parser.add_argument('--random-seed', 
                       action='store_true',
                       help='Force random seed generation (overrides other seed settings)')
    
    args, _ = parser.parse_known_args()  # Allow unknown args for other uses
    
    # Force random if requested
    if args.random_seed:
        seed = random.randint(0, 999999)
        print(f"Using forced random seed: {seed}")
        return seed
    
    # Try command line seed
    if args.seed:
        seed = Config.parse_seed(args.seed)
        if seed is not None:
            print(f"Using command line seed: {seed} (from '{args.seed}')")
            return seed
        else:
            print(f"Invalid command line seed '{args.seed}', falling back to next option")
    
    # 2. Check environment variable
    env_seed = os.environ.get('HEX_WORLD_SEED')
    if env_seed:
        seed = Config.parse_seed(env_seed)
        if seed is not None:
            print(f"Using environment variable seed: {seed} (from '{env_seed}')")
            return seed
        else:
            print(f"Invalid environment seed '{env_seed}', falling back to next option")
    
    # 3. Check config default
    if Config.DEFAULT_WORLD_SEED is not None:
        print(f"Using config default seed: {Config.DEFAULT_WORLD_SEED}")
        return Config.DEFAULT_WORLD_SEED
    
    # 4. Generate random seed
    seed = random.randint(0, 999999)
    print(f"Using random seed: {seed}")
    return seed
