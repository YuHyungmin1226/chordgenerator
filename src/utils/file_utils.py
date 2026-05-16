"""
File processing utility module

This module provides file path management, file creation, download,
and other file-related utility functions.
"""

import os
import sys
from datetime import datetime
from typing import Optional
import io
import base64
from music21 import stream


def get_documents_dir() -> str:
    """
    Gets the user's Documents folder path.
    
    Returns:
        str: Documents folder path
    """
    try:
        if sys.platform == "win32":
            # Windows
            return os.path.join(os.environ['USERPROFILE'], 'Documents')
        elif sys.platform == "darwin":
            # macOS
            return os.path.join(os.path.expanduser("~"), "Documents")
        else:
            # Linux and others
            return os.path.join(os.path.expanduser("~"), "Documents")
    except Exception as e:
        print(f"[ERROR] Failed to get Documents directory: {e}")
        # Return default path
        return os.path.join(os.path.expanduser("~"), "Documents")


def get_unique_filename(base_name: str, ext: str, save_dir: str) -> str:
    """
    Generates a unique filename.
    
    Args:
        base_name: Base filename
        ext: File extension
        save_dir: Save directory
    
    Returns:
        str: Unique file path
    """
    today = datetime.now().strftime("%Y%m%d")
    n = 1
    # Create Score folder
    score_dir = os.path.join(save_dir, "Score")
    os.makedirs(score_dir, exist_ok=True)
    
    while True:
        filename = f"{base_name}_{today}_{n}.{ext}"
        full_path = os.path.join(score_dir, filename)
        if not os.path.exists(full_path):
            return full_path
        n += 1


def create_musicxml_download(score: stream.Score, filename: str) -> str:
    """
    Converts a Music21 Score object to a downloadable MusicXML format.
    
    Args:
        score: music21 Score object
        filename: Filename
    
    Returns:
        str: base64 encoded download link
    """
    try:
        # Create MusicXML using a temporary file
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.musicxml', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Save as MusicXML file
            score.write('musicxml', fp=temp_path)
            
            # Read file
            with open(temp_path, 'rb') as f:
                file_data = f.read()
            
            # base64 encoding
            b64 = base64.b64encode(file_data).decode('utf-8')
            
            # Create download link
            href = f'<a href="data:application/vnd.recordare.musicxml+xml;base64,{b64}" download="{filename}">Download {filename}</a>'
            
            return href
            
        finally:
            # Delete temporary file
            try:
                os.unlink(temp_path)
            except:
                pass
                
    except Exception as e:
        print(f"[ERROR] Failed to create MusicXML download: {e}")
        return f"<p>Download generation failed: {e}</p>"