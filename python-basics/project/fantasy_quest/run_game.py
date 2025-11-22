"""
Fantasy Quest - Game Launcher
Run this file to start the game
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    from src.main import main
    main()
