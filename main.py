"""
main.py - Entry point for Hex Explorer
"""

from config import get_world_seed
from ui.game_window import HexGridGame

def main():
    """Entry point for the application with enhanced seed handling"""
    # Get seed using priority system
    world_seed = get_world_seed()
    
    # Create and run game with seed
    game = HexGridGame(world_seed=world_seed)
    game.run()

if __name__ == "__main__":
    main()