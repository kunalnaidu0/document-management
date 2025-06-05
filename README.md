# Document Manager

A modern, cross-platform desktop application for uploading and managing documents, with a built-in auto-updater via GitHub releases.

## Features

- 📅 **Date Picker**: Select a date associated with your file (e.g., invoice date).
- 📁 **File Upload**: Upload a document from your local system.
- 🌙 **Dark Mode**: Toggle between light and dark themes.
- 🔄 **Auto-Updater**: Automatically checks for new versions via GitHub.
- 🚀 **Single Executable**: Packaged using PyInstaller for easy distribution.

## Installation

### Option 1: Use the Pre-Built Executable

Visit the [Releases](https://github.com/kunalnaidu0/document-management/releases) page and download the latest `.exe` file.

No installation required—just run the executable.

### Option 2: Run from Source

1. Clone the repository:

```bash
git clone https://github.com/kunalnaidu0/document-management.git
cd document-management
```

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

## Packaging

To generate an executable:

```bash
pyinstaller main.py --noconfirm --onefile --windowed --name DocumentManager
```

## Auto-Update Mechanism

- On startup, the app checks GitHub for a new version listed in `version.txt`.
- If a new version is found, the user is prompted to install it.
- The new executable is downloaded and replaces the current one using a temporary batch script.

## Versioning

The version is tracked in:

- `version.py` – Python-level version reference (e.g., `__version__ = "0.1.0"`)
- `version.txt` – Used for remote update checks

Use [`bump2version`](https://github.com/c4urself/bump2version) to update versions consistently:

```bash
bump2version patch    # or use major / minor
```

## Folder Structure

```
.
├── gui.py               # GUI logic and layout
├── main.py              # Entry point
├── updater.py           # Update logic (GitHub version check + downloader)
├── version.py           # Stores __version__
├── version.txt          # Public file for GitHub auto-update comparison
├── .venv/               # Virtual environment (ignored)
├── __pycache__/         # Compiled Python cache (ignored)
├── .gitignore
└── README.md
```

## License

MIT License
