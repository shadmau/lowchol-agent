"""
OCR processing functionality for extracting text from images.
"""

import os
import tempfile
import base64
import io
from typing import Optional
from paddleocr import PaddleOCR
from PIL import Image

# Initialize PaddleOCR with minimal settings
ocr = PaddleOCR(use_angle_cls=True, lang='en')


def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using PaddleOCR.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted text as a string, or error message if processing fails
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return f"Error: Image file not found: {image_path}"
        
        print(f"Processing image: {image_path}")
        
        # Run OCR on the image
        result = ocr.ocr(image_path)
        
        print(f"OCR result type: {type(result)}")
        
        # Extract text from results - handle different OCR result formats
        text_lines = []
        if result and len(result) > 0:
            # New format: result is a list with dict containing 'rec_texts'
            if isinstance(result[0], dict) and 'rec_texts' in result[0]:
                text_lines = result[0]['rec_texts']
                scores = result[0].get('rec_scores', [])
                for i, text in enumerate(text_lines):
                    score = scores[i] if i < len(scores) else 0
                    print(f"Detected text: '{text}' (confidence: {score:.2f})")
            # Old format: result is nested array
            elif isinstance(result[0], list):
                for line in result[0]:
                    if line and len(line) > 1:
                        text = line[1][0]
                        confidence = line[1][1]
                        print(f"Detected text: '{text}' (confidence: {confidence:.2f})")
                        text_lines.append(text)
        
        # Join all text lines
        extracted_text = '\n'.join(text_lines)
        return extracted_text if extracted_text.strip() else "No text found in image"
        
    except Exception as e:
        print(f"Exception details: {e}")
        return f"Error processing image: {str(e)}"


def extract_text_from_base64(base64_string: str) -> str:
    """
    Extract text from a base64 encoded image.
    
    Args:
        base64_string: Base64 encoded image string
        
    Returns:
        Extracted text as a string, or error message if processing fails
    """
    try:
        # Decode base64 to image
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            image.save(temp_file.name)
            temp_path = temp_file.name
        
        # Extract text
        text = extract_text_from_image(temp_path)
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        return text
        
    except Exception as e:
        return f"Error processing base64 image: {str(e)}" 