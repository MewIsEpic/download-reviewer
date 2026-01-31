"""
Download Reviewer
A desktop application to help organize Windows Downloads folder
by reviewing files one by one.
"""

import customtkinter as ctk
from app.ui import DownloadReviewer

# Configure customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    """Main entry point."""
    root = ctk.CTk()
    app = DownloadReviewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()

