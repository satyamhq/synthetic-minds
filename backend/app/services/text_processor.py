"""
Text Processing Service.
Handles document extraction, chunking, and text normalization.
"""

from typing import List, Optional
from ..utils.file_parser import FileParser, split_text_into_chunks


class TextProcessor:
    """Text processing utility class."""
    
    @staticmethod
    def extract_from_files(file_paths: List[str]) -> str:
        """Extract and concatenate text from multiple files."""
        return FileParser.extract_from_multiple(file_paths)
    
    @staticmethod
    def split_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Source text string
            chunk_size: Target characters per chunk
            overlap: Overlap characters between chunks
            
        Returns:
            List of text chunks
        """
        return split_text_into_chunks(text, chunk_size, overlap)
    
    @staticmethod
    def preprocess_text(text: str) -> str:
        """
        Preprocess text: normalize line endings and whitespace.
        
        Args:
            text: Raw input text
            
        Returns:
            Normalized clean text string
        """
        import re
        
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Collapse multiple empty lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Strip trailing and leading line whitespace
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text.strip()
    
    @staticmethod
    def get_text_stats(text: str) -> dict:
        """Calculate summary statistics for text."""
        return {
            "total_chars": len(text),
            "total_lines": text.count('\n') + 1,
            "total_words": len(text.split()),
        }
