# Project File Size Checker

A GUI application created to help manage file sizes in game development projects, specifically designed to help maintain GitHub's file size limits (100MB per file, 100GB total repository size). Originally created to assist with Godot 4 project collaboration, but useful for any project requiring file size management.

## Why This Tool?

This tool was born out of a practical need during Godot 4 game development collaboration. GitHub has specific limitations:
- 100MB per file size limit
- 100GB total repository size

To stay within these limits while collaborating on game projects, this tool provides an easy way to:
- Quickly identify files that exceed GitHub's limits
- Monitor overall project size
- Specifically handle game engine folders (currently optimized for Godot projects)

## Features
- Browse and select any folder to analyze
- Set custom file size threshold in MB
- Option to include/exclude .git and .godot folders
- Custom folder exclusion list - specify any folders to skip during scanning
- Interactive results with clickable file paths
- Clean, modern interface

## Installation

1. Make sure you have Python installed (3.6 or higher)
2. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/file-size-checker.git
cd file-size-checker
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python file_size_checker_gui.py
```

1. Click "Browse" to select a folder
2. Set your desired size limit in MB
3. Choose whether to include .git and .godot folders
4. (Optional) Enter folder names to exclude from scanning (one per line)
5. Click "Scan Files"
6. Results will show files exceeding the size limit
7. Click on file paths to open their location in File Explorer

## Building Executable (Optional)

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed file_size_checker_gui.py
```

The executable will be created in the `dist` directory.

## License

MIT License - Feel free to use and modify as needed.
