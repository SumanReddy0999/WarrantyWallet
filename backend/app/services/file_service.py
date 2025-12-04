import os
import shutil
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException, status

class FileService:
    """Service for handling file uploads and management"""
    
    def __init__(self, upload_dir: str):
        """Initialize with upload directory path"""
        self.upload_dir = Path(upload_dir)
        self.ensure_upload_dir()
    
    def ensure_upload_dir(self) -> None:
        """Ensure upload directory exists"""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def get_file_extension(self, filename: str) -> str:
        """Get file extension in lowercase"""
        return Path(filename).suffix.lower()
    
    def is_allowed_file(self, filename: str) -> bool:
        """Check if the file has an allowed extension"""
        from app.core.config import settings
        allowed_extensions = {".pdf", ".png", ".jpg", ".jpeg"}
        return self.get_file_extension(filename) in allowed_extensions
    
    async def save_upload_file(
        self, 
        file: UploadFile
    ) -> Tuple[Path, str]:
        """
        Save uploaded file to the upload directory
        
        Args:
            file: The uploaded file
            
        Returns:
            Tuple of (saved_file_path, mime_type)
        """
        if not self.is_allowed_file(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(['.pdf', '.png', '.jpg', '.jpeg'])}"
            )
        
        # Create a unique filename to prevent overwrites
        file_extension = self.get_file_extension(file.filename)
        unique_filename = f"{os.urandom(8).hex()}{file_extension}"
        file_path = self.upload_dir / unique_filename
        
        # Save the file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving file: {str(e)}"
            )
        
        return file_path, file.content_type
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            bool: True if deleted, False if file didn't exist
        """
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    
    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes"""
        return os.path.getsize(file_path)
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists"""
        return os.path.exists(file_path)
