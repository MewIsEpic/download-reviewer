"""
FileManager class for handling file operations.
Handles scanning, deletion, and moving of files.
"""

from pathlib import Path
from datetime import datetime, timedelta
import shutil
from send2trash import send2trash
import config


class FileManager:
    """Manages file operations: scanning, deletion, and moving."""
    
    def __init__(self, downloads_path=None):
        """
        Initialize FileManager.
        
        Args:
            downloads_path: Path to Downloads folder. If None, uses config.DOWNLOADS_PATH.
        """
        if downloads_path is None:
            self.downloads_path = config.DOWNLOADS_PATH
        else:
            self.downloads_path = Path(downloads_path)
    
    def get_recent_files(self, hours=None):
        """
        Scan Downloads folder and return files created in the last N hours.
        
        Args:
            hours: Number of hours to look back (default: config.HOURS_THRESHOLD)
            
        Returns:
            List of Path objects for files created in the last N hours, sorted by creation time (newest first)
        """
        if hours is None:
            hours = config.HOURS_THRESHOLD
        
        recent_files = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        try:
            if not self.downloads_path.exists():
                raise FileNotFoundError(
                    f"Downloads folder not found at: {self.downloads_path}"
                )
            
            for item in self.downloads_path.iterdir():
                # Only process files, not directories
                if item.is_file():
                    try:
                        # Get file creation time (Windows)
                        creation_time = datetime.fromtimestamp(item.stat().st_ctime)
                        
                        if creation_time >= cutoff_time:
                            recent_files.append(item)
                    except (OSError, PermissionError) as e:
                        # Skip files that can't be accessed
                        print(f"Error accessing {item.name}: {e}")
                        continue
            
            # Sort by creation time (newest first)
            recent_files.sort(key=lambda x: x.stat().st_ctime, reverse=True)
            
        except Exception as e:
            raise Exception(f"Error scanning Downloads folder: {e}")
        
        return recent_files
    
    def format_file_size(self, size_bytes):
        """
        Convert bytes to human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted string (e.g., "1.23 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def delete_file(self, file_path):
        """
        Delete a file to Recycle Bin.
        
        Args:
            file_path: Path object or string path to the file
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            PermissionError: If file cannot be deleted (e.g., file is open)
            Exception: For other deletion errors
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            send2trash(str(file_path))
            return True
        except Exception as e:
            error_msg = str(e)
            if "Permission denied" in error_msg or "access" in error_msg.lower():
                raise PermissionError(
                    f"Cannot delete '{file_path.name}'. "
                    "The file may be open in another program. "
                    "Please close it and try again."
                )
            else:
                raise Exception(f"Failed to delete file: {error_msg}")
    
    def move_file(self, file_path, destination_folder, overwrite=False):
        """
        Move a file to a destination folder.
        
        Args:
            file_path: Path object or string path to the file
            destination_folder: Path object or string path to destination folder
            overwrite: If True, overwrite existing file. If False, raise error if exists.
            
        Returns:
            Path object of the moved file
            
        Raises:
            FileNotFoundError: If source file or destination folder doesn't exist
            PermissionError: If file cannot be moved (e.g., file is open)
            FileExistsError: If destination file exists and overwrite=False
            Exception: For other move errors
        """
        file_path = Path(file_path)
        destination_path = Path(destination_folder)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not destination_path.exists():
            raise FileNotFoundError(f"Destination folder not found: {destination_path}")
        
        if not destination_path.is_dir():
            raise ValueError(f"Destination is not a directory: {destination_path}")
        
        destination_file = destination_path / file_path.name
        
        # Check if file already exists in destination
        if destination_file.exists() and not overwrite:
            raise FileExistsError(
                f"'{file_path.name}' already exists in the destination folder."
            )
        
        try:
            # Move the file
            shutil.move(str(file_path), str(destination_file))
            return destination_file
        except PermissionError:
            raise PermissionError(
                f"Cannot move '{file_path.name}'. "
                "The file may be open in another program. "
                "Please close it and try again."
            )
        except Exception as e:
            raise Exception(f"Failed to move file: {str(e)}")
    
    def get_file_info(self, file_path):
        """
        Get file information (size, creation time).
        
        Args:
            file_path: Path object or string path to the file
            
        Returns:
            Dictionary with 'size', 'size_formatted', 'creation_time', 'creation_time_str'
            
        Raises:
            OSError: If file cannot be accessed
        """
        file_path = Path(file_path)
        file_stat = file_path.stat()
        
        size_bytes = file_stat.st_size
        creation_time = datetime.fromtimestamp(file_stat.st_ctime)
        
        return {
            'size': size_bytes,
            'size_formatted': self.format_file_size(size_bytes),
            'creation_time': creation_time,
            'creation_time_str': creation_time.strftime("%Y-%m-%d %H:%M:%S")
        }

