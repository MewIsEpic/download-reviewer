"""
UI module for Download Reviewer.
Contains the DownloadReviewer class that handles all user interface logic.
"""

import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog, messagebox
from app.file_manager import FileManager
from app.preview_generator import PreviewGenerator
from PIL import ImageTk
import config


class DownloadReviewer:
    """Main UI class for the Download Reviewer application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Download Reviewer")
        self.root.geometry(config.WINDOW_SIZE)
        
        # Initialize FileManager and PreviewGenerator
        self.file_manager = FileManager()
        self.preview_generator = PreviewGenerator()
        
        # Get files from configured hours threshold
        try:
            self.files_to_review = self.file_manager.get_recent_files(hours=config.HOURS_THRESHOLD)
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
            self.files_to_review = []
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.files_to_review = []
        
        self.current_index = 0
        
        # Create UI
        self.create_ui()
        
        # Show first file or completion message
        if self.files_to_review:
            self.show_current_file()
        else:
            self.show_all_clean()
    
    def create_ui(self):
        """Create the user interface."""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Content area (scrollable if needed)
        self.content_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="Download Reviewer",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(10, 20))
        
        # File info frame
        self.info_frame = ctk.CTkFrame(self.content_frame)
        self.info_frame.pack(fill="x", pady=(0, 10))
        
        # File name label
        self.file_name_label = ctk.CTkLabel(
            self.info_frame,
            text="File Name:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.file_name_label.pack(pady=(20, 5))
        
        self.file_name_value = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=500
        )
        self.file_name_value.pack(pady=(0, 10))
        
        # File size label
        self.file_size_label = ctk.CTkLabel(
            self.info_frame,
            text="Size:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.file_size_label.pack(pady=(10, 5))
        
        self.file_size_value = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.file_size_value.pack(pady=(0, 10))
        
        # Creation time label
        self.creation_time_label = ctk.CTkLabel(
            self.info_frame,
            text="Created:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.creation_time_label.pack(pady=(10, 5))
        
        self.creation_time_value = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.creation_time_value.pack(pady=(0, 10))
        
        # Preview section
        self.preview_label = ctk.CTkLabel(
            self.info_frame,
            text="Preview:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.preview_label.pack(pady=(10, 5))
        
        # Preview image label - limit size to prevent overflow
        self.preview_image_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            width=550,
            height=200
        )
        self.preview_image_label.pack(pady=(0, 5), padx=10)
        self.preview_image = None  # Keep reference to prevent garbage collection
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(pady=(5, 5))
        
        # Fixed bottom section for buttons (always visible)
        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        # Navigation buttons frame
        self.nav_frame = ctk.CTkFrame(self.bottom_frame)
        self.nav_frame.pack(anchor="center", pady=(10, 5))
        
        # Previous button
        self.prev_button = ctk.CTkButton(
            self.nav_frame,
            text="◀ Previous",
            command=self.previous_file,
            fg_color="#616161",
            hover_color="#424242",
            width=100
        )
        self.prev_button.pack(side="left", padx=5)
        
        # Next button
        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next ▶",
            command=self.next_file,
            fg_color="#616161",
            hover_color="#424242",
            width=100
        )
        self.next_button.pack(side="left", padx=5)
        
        # Buttons frame - centered
        self.buttons_frame = ctk.CTkFrame(self.bottom_frame)
        self.buttons_frame.pack(anchor="center", pady=10)
        
        # Delete button
        self.delete_button = ctk.CTkButton(
            self.buttons_frame,
            text="Delete",
            command=self.delete_file,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            width=120
        )
        self.delete_button.pack(side="left", padx=10, pady=10)
        
        # Keep button
        self.keep_button = ctk.CTkButton(
            self.buttons_frame,
            text="Keep",
            command=self.keep_file,
            fg_color="#388e3c",
            hover_color="#2e7d32",
            width=120
        )
        self.keep_button.pack(side="left", padx=10, pady=10)
        
        # Move button
        self.move_button = ctk.CTkButton(
            self.buttons_frame,
            text="Move",
            command=self.move_file,
            fg_color="#1976d2",
            hover_color="#1565c0",
            width=120
        )
        self.move_button.pack(side="left", padx=10, pady=10)
    
    def show_current_file(self):
        """Display the current file information."""
        if self.current_index >= len(self.files_to_review):
            self.show_all_clean()
            return
        
        # Remove files that no longer exist from the list
        self.files_to_review = [f for f in self.files_to_review if f.exists()]
        
        # Adjust index if it's now out of bounds
        if self.current_index >= len(self.files_to_review):
            if len(self.files_to_review) == 0:
                self.show_all_clean()
                return
            self.current_index = len(self.files_to_review) - 1
        
        if self.current_index < 0:
            self.current_index = 0
        
        current_file = self.files_to_review[self.current_index]
        
        try:
            # Get file info using FileManager
            file_info = self.file_manager.get_file_info(current_file)
            
            # Update UI
            self.file_name_value.configure(text=current_file.name)
            self.file_size_value.configure(text=file_info['size_formatted'])
            self.creation_time_value.configure(text=file_info['creation_time_str'])
            
            # Update preview
            preview_img = self.preview_generator.get_file_preview_image(current_file)
            if preview_img:
                # Convert PIL Image to PhotoImage
                preview_img_tk = ImageTk.PhotoImage(preview_img)
                self.preview_image = preview_img_tk  # Keep reference
                self.preview_image_label.configure(image=preview_img_tk, text="")
            else:
                # No preview available
                self.preview_image = None
                message = self.preview_generator.get_preview_error_message(current_file)
                self.preview_image_label.configure(
                    image=None,
                    text=message
                )
            
            # Update progress
            progress_text = f"File {self.current_index + 1} of {len(self.files_to_review)}"
            self.progress_label.configure(text=progress_text)
            
            # Enable/disable navigation buttons
            self.prev_button.configure(state="normal" if self.current_index > 0 else "disabled")
            self.next_button.configure(state="normal" if self.current_index < len(self.files_to_review) - 1 else "disabled")
            
            # Enable action buttons
            self.delete_button.configure(state="normal")
            self.keep_button.configure(state="normal")
            self.move_button.configure(state="normal")
            
        except (OSError, PermissionError) as e:
            messagebox.showerror(
                "Error",
                f"Cannot access file: {current_file.name}\n{str(e)}"
            )
            # Skip this file and move to next
            self.current_index += 1
            self.show_current_file()
    
    def delete_file(self):
        """Delete the current file to Recycle Bin."""
        if self.current_index >= len(self.files_to_review):
            return
        
        current_file = self.files_to_review[self.current_index]
        
        try:
            self.file_manager.delete_file(current_file)
            messagebox.showinfo("Success", f"'{current_file.name}' moved to Recycle Bin")
            
            # Remove deleted file from the list
            self.files_to_review.pop(self.current_index)
            
            # Adjust index if needed (don't increment if we're at the end)
            if self.current_index >= len(self.files_to_review) and self.current_index > 0:
                self.current_index = len(self.files_to_review) - 1
            
            self.show_current_file()
        except PermissionError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete file: {str(e)}")
    
    def keep_file(self):
        """Keep the current file and move to the next one."""
        self.current_index += 1
        self.show_current_file()
    
    def previous_file(self):
        """Navigate to the previous file."""
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_file()
    
    def next_file(self):
        """Navigate to the next file."""
        if self.current_index < len(self.files_to_review) - 1:
            self.current_index += 1
            self.show_current_file()
    
    def move_file(self):
        """Move the current file to a selected folder."""
        if self.current_index >= len(self.files_to_review):
            return
        
        current_file = self.files_to_review[self.current_index]
        
        try:
            # Open folder selection dialog
            destination = filedialog.askdirectory(title="Select destination folder")
            
            if destination:
                destination_path = Path(destination)
                
                # Check if file already exists in destination
                overwrite = False
                destination_file = destination_path / current_file.name
                if destination_file.exists():
                    response = messagebox.askyesno(
                        "File Exists",
                        f"'{current_file.name}' already exists in the destination folder. "
                        "Do you want to overwrite it?"
                    )
                    if not response:
                        return
                    overwrite = True
                
                # Move the file using FileManager
                self.file_manager.move_file(current_file, destination_path, overwrite=overwrite)
                messagebox.showinfo(
                    "Success",
                    f"'{current_file.name}' moved to:\n{destination}"
                )
                
                # Remove moved file from the list (it's no longer in Downloads)
                self.files_to_review.pop(self.current_index)
                
                # Adjust index if needed (don't increment if we're at the end)
                if self.current_index >= len(self.files_to_review) and self.current_index > 0:
                    self.current_index = len(self.files_to_review) - 1
                
                self.show_current_file()
        except PermissionError as e:
            messagebox.showerror("Error", str(e))
        except FileExistsError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move file: {str(e)}")
    
    def show_all_clean(self):
        """Show the 'All Clean!' message when there are no more files."""
        # Hide file info
        self.info_frame.pack_forget()
        
        # Hide buttons (but keep bottom frame visible)
        self.nav_frame.pack_forget()
        self.buttons_frame.pack_forget()
        self.progress_label.pack_forget()
        
        # Clear preview
        self.preview_image = None
        self.preview_image_label.configure(image=None, text="")
        
        # Show completion message in content frame
        self.completion_label = ctk.CTkLabel(
            self.content_frame,
            text="All Clean! ✨",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#4caf50"
        )
        self.completion_label.pack(pady=50)
        
        self.completion_subtitle = ctk.CTkLabel(
            self.content_frame,
            text="No files from the last 24 hours to review.",
            font=ctk.CTkFont(size=14)
        )
        self.completion_subtitle.pack(pady=(10, 30))
        
        # Close button in bottom frame (centered)
        self.close_button = ctk.CTkButton(
            self.bottom_frame,
            text="Close",
            command=self.root.quit,
            width=120,
            height=40
        )
        self.close_button.pack(anchor="center", pady=20)

