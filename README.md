# ideal-chainsaw

# Simple Python Editor — Run & Commit

A minimal Tkinter-based Python editor that saves, runs a Python file, then stages, commits, and pushes the change to the repository containing the file.

Requirements
- Python 3.8+
- Git installed and the repository remote configured (SSH or credential manager)

Usage
1. Install Python if you don't have it.
2. Run the editor:

```bash
python main.py
```

3. In the editor: Open or create a `.py` file, edit, Save, then press "Run + Commit".

Notes
- The tool looks for a `.git` folder in the file's directory or any parent directory. If none is found, commit/push is skipped.
- Pushing requires valid git credentials on your machine (SSH key or saved credentials).

