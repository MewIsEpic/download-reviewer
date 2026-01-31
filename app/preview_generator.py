"""
PreviewGenerator class for generating previews of various file types.
Handles images, PDFs, videos, and application icons.
"""

from pathlib import Path
from PIL import Image
import io

# Try to import optional dependencies
try:
    import fitz  # PyMuPDF
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    import win32api
    import win32gui
    import win32con
    ICON_SUPPORT = True
except ImportError:
    ICON_SUPPORT = False

try:
    import cv2
    VIDEO_SUPPORT = True
except ImportError:
    VIDEO_SUPPORT = False


class PreviewGenerator:
    """Generates preview images for various file types."""
    
    def __init__(self):
        """Initialize PreviewGenerator."""
        self.pdf_support = PDF_SUPPORT
        self.icon_support = ICON_SUPPORT
        self.video_support = VIDEO_SUPPORT
    
    def is_image_file(self, file_path):
        """Check if a file is an image based on extension."""
        # Note: SVG requires special handling, so we'll skip it for now
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.webp', '.tiff', '.tif'}
        return file_path.suffix.lower() in image_extensions
    
    def is_pdf_file(self, file_path):
        """Check if a file is a PDF."""
        return file_path.suffix.lower() == '.pdf'
    
    def is_executable_file(self, file_path):
        """Check if a file is an executable/application."""
        exe_extensions = {'.exe', '.msi', '.app', '.dmg', '.deb', '.rpm', '.pkg'}
        return file_path.suffix.lower() in exe_extensions
    
    def is_video_file(self, file_path):
        """Check if a file is a video."""
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
        return file_path.suffix.lower() in video_extensions
    
    def get_image_preview(self, file_path, max_size=(500, 200)):
        """Get image preview from image file."""
        try:
            img = Image.open(file_path)
            
            # Handle different image modes
            if img.mode == 'RGBA':
                # Create white background for transparency
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode == 'P':  # Palette mode
                img = img.convert('RGB')
            elif img.mode not in ('RGB', 'L'):  # L is grayscale
                img = img.convert('RGB')
            
            # Resize maintaining aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            return img
        except Exception as e:
            return None
    
    def get_pdf_preview(self, file_path, max_size=(500, 200)):
        """Get first page preview from PDF file."""
        if not self.pdf_support:
            return None
        
        try:
            pdf_document = fitz.open(str(file_path))
            if len(pdf_document) == 0:
                return None
            
            # Get first page
            first_page = pdf_document[0]
            
            # Render page to image (pixmap)
            zoom = min(max_size[0] / first_page.rect.width, max_size[1] / first_page.rect.height, 2.0)
            mat = fitz.Matrix(zoom, zoom)
            pix = first_page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))
            
            pdf_document.close()
            return img
        except Exception as e:
            return None
    
    def get_app_icon(self, file_path, max_size=(128, 128)):
        """Extract icon from executable/application file."""
        if not self.icon_support:
            return None
        
        try:
            # Extract icon using Windows API
            large, small = win32api.ExtractIconEx(str(file_path), 0)
            if not large and not small:
                return None
            
            # Use large icon if available, otherwise small
            icon_handle = large[0] if large else small[0]
            
            # Get icon info
            icon_info = win32gui.GetIconInfo(icon_handle)
            hbm = icon_info[3]  # hbmColor (color bitmap)
            hbm_mask = icon_info[4]  # hbmMask
            
            # Get bitmap dimensions
            bmp = win32gui.GetObject(hbm)
            if hasattr(bmp, 'bmWidth'):
                width = bmp.bmWidth
                height = bmp.bmHeight
            else:
                # Fallback: try to get size from bitmap header
                width = 32
                height = 32
            
            # Get bitmap bits
            try:
                bmp_size = width * height * 4
                bmpstr = win32gui.GetBitmapBits(hbm, bmp_size)
                
                # Convert to PIL Image (BGRA format)
                img = Image.frombuffer(
                    'RGBA',
                    (width, height),
                    bmpstr, 'raw', 'BGRA', 0, 1
                )
                
                # Convert to RGB
                img = img.convert('RGB')
            except Exception:
                # If bitmap extraction fails, create a placeholder
                img = Image.new('RGB', (32, 32), color=(200, 200, 200))
            
            # Clean up
            win32gui.DeleteObject(hbm)
            if hbm_mask:
                win32gui.DeleteObject(hbm_mask)
            win32api.DestroyIcon(icon_handle)
            
            # Resize if needed
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            return img
        except Exception as e:
            # If icon extraction fails, return None
            return None
    
    def get_video_preview(self, file_path, max_size=(500, 200)):
        """Get preview frame from video file."""
        if not self.video_support:
            return None
        
        try:
            # Open video file
            cap = cv2.VideoCapture(str(file_path))
            
            if not cap.isOpened():
                return None
            
            # Get first frame (or frame at 1 second if available)
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
            
            if not ret:
                cap.release()
                return None
            
            # Convert BGR to RGB (OpenCV uses BGR, PIL uses RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            img = Image.fromarray(frame_rgb)
            
            # Release video capture
            cap.release()
            
            # Resize maintaining aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            return img
        except Exception as e:
            return None
    
    def get_file_preview_image(self, file_path):
        """Get preview image based on file type."""
        if self.is_image_file(file_path):
            return self.get_image_preview(file_path)
        elif self.is_pdf_file(file_path):
            return self.get_pdf_preview(file_path)
        elif self.is_video_file(file_path):
            return self.get_video_preview(file_path)
        elif self.is_executable_file(file_path):
            return self.get_app_icon(file_path)
        else:
            return None
    
    def get_preview_error_message(self, file_path):
        """
        Get error message for preview not available.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Error message string
        """
        if self.is_image_file(file_path):
            return "Image preview not available"
        elif self.is_pdf_file(file_path):
            if not self.pdf_support:
                return "PDF preview not available\n(Install PyMuPDF for PDF support)"
            else:
                return "PDF preview not available"
        elif self.is_video_file(file_path):
            if not self.video_support:
                return "Video preview not available\n(Install opencv-python for video support)"
            else:
                return "Video preview not available"
        elif self.is_executable_file(file_path):
            if not self.icon_support:
                return "App icon not available\n(Install pywin32 for icon support)"
            else:
                return "App icon not available"
        else:
            return "Preview not available\n(Only images, PDFs, videos, and apps are previewed)"

