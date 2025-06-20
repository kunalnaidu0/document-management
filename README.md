# Document Manager

A modern, cross-platform desktop application for uploading and managing documents, featuring dark mode and an integrated auto-updater powered by GitHub Releases.

## ✨ Features

- 📅 **Date Picker**: Choose the date associated with the uploaded document (e.g., invoice date).
- 📁 **File Upload**: Select and attach documents for submission.
- 🌙 **Dark Mode Support**: Automatic or toggleable dark/light theme.
- 🔄 **Auto-Updater**:
  - Checks GitHub for a new version on launch or on demand.
  - Downloads latest `.exe` and replaces the old version automatically.
  - Uses a separate update runner to avoid file lock issues.
- ✅ **Update Confirmation**: After a successful update, the app shows a "Update Complete" confirmation.
- 💼 **Single Executable**: Built with PyInstaller for easy distribution.

---

## 📦 Installation

### Option 1: Use the Pre-Built Executable

1. Visit the [Releases page](https://github.com/kunalnaidu0/document-management/releases).
2. Download the latest `DocumentManager.exe`.
3. Double-click to run — no installation needed.

### Option 2: Run From Source

```bash
git clone https://github.com/kunalnaidu0/document-management.git
cd document-management

python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

---

## 🏗️ Build Executable

To build the Windows `.exe`:

```bash
pyinstaller main.py --onefile --windowed --name DocumentManager
```

This generates `dist/DocumentManager.exe`.

> ℹ️ Run from **Windows** (not WSL) to build a Windows executable.

---

## 🔁 Auto-Update System

### How It Works:

1. `version.txt` (hosted on GitHub) stores the latest public version.
2. On startup or via menu, the app checks if your version (`version.py`) is outdated.
3. If outdated:
   - It downloads the new executable to a temporary directory.
   - Launches `update_runner.py` to safely overwrite the old file.
   - Shows confirmation on next launch if update succeeded.

### Update Success Flag:

- After replacing the executable, a file named `update_success.flag` is created.
- This is checked on next startup to confirm update success.

---

## 🏷️ Versioning & Releases

### Version Stored In:

- `version.py` – Local application version (`__version__ = "x.y.z"`)
- `version.txt` – Public version for GitHub update checks

### Tagging Releases in Git:

```bash
git tag v0.0.2
git push origin v0.0.2
```

Then go to **GitHub > Releases** and create a new release using the tag, attaching the built `.exe`.

---

## 🧭 Project Structure

```
document-management/
├── gui.py               # PySide6 GUI interface
├── main.py              # Main application entry
├── updater.py           # Version check and update downloader
├── update_runner.py     # File replacement after download
├── version.py           # Local version (Python readable)
├── version.txt          # Public version (GitHub readable)
├── requirements.txt     # Package dependencies
├── README.md            # Project documentation
├── .gitignore
├── .venv/               # Virtual environment (ignored)
└── __pycache__/         # Python bytecode (ignored)
```

---

## 📑 License

MIT License
