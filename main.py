#!/usr/bin/env python3
"""
Chord Progression Generator - Main Entry Point

This file serves as the main entry point for the web application.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main execution function"""
    try:
        print("[WEB] Starting local web app...")
        print("Please open http://localhost:5000 in your browser.")
        
        from src.web.app import app
        # Run the Flask app
        app.run(host='127.0.0.1', port=5000, debug=False)
            
    except ImportError as e:
        print(f"[ERROR] Could not import module: {e}")
        print("Please install required packages:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()