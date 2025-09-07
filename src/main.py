"""
Main entry point for the Notched Music application.
"""

import sys
import logging
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from gui import main as gui_main

def main():
    """Main entry point."""
    # Set up basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Notched Music application")
    
    try:
        gui_main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

