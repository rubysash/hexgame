"""
main.py - Entry point for Hex Explorer
"""

from ui.game_window import HexGridGame

def main():
    """Entry point for the application"""
    game = HexGridGame()
    game.run()

if __name__ == "__main__":
    main()