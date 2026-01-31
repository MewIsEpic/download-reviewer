## Download Reviewer
A simple Python utility to keep your Windows Downloads folder clean.

## Why I Built This
I built this because my Downloads folder was constantly cluttered with temporary files I would forget to delete. Instead of manually sorting them, I wanted a quick way to review files from the last 24 hours and decide: Keep, Move, or Trash.

## Features
**Auto-Scan:** Finds files downloaded in the last 24 hours.

**Safe Deletion:** Sends files to the Recycle Bin (no accidental data loss).

**Visuals:** Shows previews for images and PDFs so you know what you're deleting.

##
<img width="494" height="462" alt="image" src="https://github.com/user-attachments/assets/12a15c2c-8144-45f7-b115-34bf06c09d5d" />



## Technical Requirements

* **OS:** Windows 10/11 (Required for `pywin32` icon extraction)
* **Language:** Python 3.10+
* **Core Libraries:** `customtkinter`, `send2trash`, `opencv-python`, `PyMuPDF`, `Pillow`

## Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/mewisepic/download-reviewer.git
    cd download-reviewer
    ```

2.  **Set up the virtual environment**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Execute the application entry point:

```bash
python main.py
```


