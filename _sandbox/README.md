# 🧪 Sandbox Folder

This folder is for **temporary work files** during daily updates.

## Usage
- All temporary scripts, coordinate files, and test files go here
- Can be safely deleted after each session
- Archive important files to `_archive/` before deleting

## After Each Session
```powershell
# Archive if needed
Move-Item _sandbox\* _archive\YYYY-MM-DD_session\

# Or just delete
Remove-Item _sandbox\* -Force
```

## What Goes Here
- Coordinate extraction scripts (`get_*_coords.py`)
- Update scripts (`update_*.py`)
- Temporary JSON files (`*_coords.json`)
- Test files (`test_*.py`)
