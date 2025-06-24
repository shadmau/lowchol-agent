#!/usr/bin/env python3
"""
LowChol Agent - Command line interface for cholesterol risk analysis.

Usage:
    python main.py "Dish Name"           - Analyze cholesterol risk
    python main.py --ocr image_path.jpg  - Extract text from image and analyze
"""

import sys
from src.lowchol_agent.agent import LowCholAgent


def main():
    """Main entry point for the application."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py \"Dish Name\"           - Analyze cholesterol risk")
        print("  python main.py --ocr image_path.jpg   - Extract text from image")
        return
    
    try:
        agent = LowCholAgent()
        
        if sys.argv[1] == "--ocr" and len(sys.argv) > 2:
            # OCR mode
            image_path = sys.argv[2]
            result = agent.analyze_image(image_path)
            print(result)
        else:
            # Dish analysis mode
            dish_name = sys.argv[1]
            result = agent.analyze_dish(dish_name)
            print(result)
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())