# Publishing to GitHub - Quick Guide

## Step 1: Stage and Commit All Files

```bash
# Add all files to staging
git add .

# Commit with a descriptive message
git commit -m "Initial commit: Download Reviewer - Windows Downloads folder organizer"
```

## Step 2: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `download-reviewer`
3. Description: "A Python utility to keep your Windows Downloads folder clean"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 3: Connect and Push to GitHub

```bash
# Add the remote repository (replace with your GitHub username if different)
git remote add origin https://github.com/mewisepic/download-reviewer.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Verify

Visit your repository: https://github.com/mewisepic/download-reviewer

## Optional: Add Topics/Tags

On GitHub, click the gear icon next to "About" and add topics like:
- `python`
- `windows`
- `file-management`
- `desktop-application`
- `customtkinter`
- `productivity`

## Files Included

✅ All source code (`main.py`, `app/`, `config.py`)
✅ `requirements.txt` - Dependencies
✅ `README.md` - Documentation
✅ `LICENSE` - MIT License
✅ `.gitignore` - Excludes venv, __pycache__, etc.

## Files Excluded (by .gitignore)

❌ `venv/` - Virtual environment
❌ `__pycache__/` - Python cache files
❌ IDE files (`.vscode/`, `.idea/`)

