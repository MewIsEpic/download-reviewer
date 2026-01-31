# Download Reviewer

A simple Python utility to keep your Windows Downloads folder clean.

## Why I Built This

I built this because my Downloads folder was constantly cluttered with temporary files I'd forget to delete. Instead of manually sorting them, I wanted a quick way to review files from the last 24 hours and decide: Keep, Move, or Trash.

## Features

- **Auto-Scan:** Finds files downloaded in the last 24 hours
- **Safe Deletion:** Sends files to the Recycle Bin (no accidental data loss)
- **Visual Previews:** Shows previews for images, PDFs, videos, and app icons so you know what you're deleting
- **Navigation:** Navigate back and forth through files for flexible review
- **File Organization:** Move files to organized folders with ease

## Technical Requirements

- **OS:** Windows 10/11 (Required for `pywin32` icon extraction)
- **Language:** Python 3.10+
- **Core Libraries:** `customtkinter`, `send2trash`, `opencv-python`, `PyMuPDF`, `Pillow`, `pywin32`

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mewisepic/download-reviewer.git
   cd download-reviewer
   ```

2. **Set up the virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Execute the application entry point:

```bash
python main.py
```

The application will scan your Downloads folder and display files from the last 24 hours one by one. You can:
- **Delete:** Send file to Recycle Bin
- **Keep:** Skip and move to next file
- **Move:** Organize file into a folder
- **Previous/Next:** Navigate through files

## Project Structure

```
download-reviewer/
├── main.py                    # Application entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── .gitignore                 # Git ignore rules
└── app/
    ├── __init__.py
    ├── file_manager.py        # File operations (scan, delete, move)
    ├── preview_generator.py   # Preview generation for various file types
    └── ui.py                  # User interface logic
```

## Configuration

Edit `config.py` to customize:
- `HOURS_THRESHOLD` - Hours to look back for recent files (default: 24)
- `DOWNLOADS_PATH` - Path to Downloads folder (default: Windows Downloads)
- `WINDOW_SIZE` - Application window size (default: "800x750")

## License

Feel free to use this tool for your own digital decluttering journey!
