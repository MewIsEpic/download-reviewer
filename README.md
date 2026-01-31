Download Reviewer is a Python-based desktop utility I developed to improve the organization of the Downloads directory on Windows.

I created this tool to address a recurring issue in my own workflow: temporary downloads accumulating over time, being forgotten, and often downloaded again unnecessarily. Manually sorting these files was inefficient, so I designed a lightweight solution to encourage regular and structured review.

Overview

The application presents files downloaded within the last 24 hours in a review queue, allowing quick decisions to Move, Keep, or Delete each file. This approach helps prevent long-term clutter while keeping the process simple and intentional.

Download Reviewer features a modern GUI built with CustomTkinter and integrates safely with the Windows filesystem, focusing on usability rather than complex automation.

## Key Features

* **Automated Detection:** Scans and filters files created within the last 24-hour window.
* **Safe Deletion:** Utilizes `send2trash` to move files to the Recycle Bin rather than permanently deleting them.
* **Batch Workflow:** Processes files sequentially to ensure a clean directory state.

## Technical Requirements

* **OS:** Windows 10/11 (Required for `pywin32` icon extraction)
* **Language:** Python 3.10+
* **Core Libraries:** `customtkinter`, `send2trash`, `opencv-python`, `PyMuPDF`

## Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/mewisepic/download-reviewer.git](https://github.com/mewisepic/download-reviewer.git)
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


