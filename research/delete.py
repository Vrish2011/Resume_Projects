from pathlib import Path

folder = Path(".")  # Current folder

for file in folder.glob("*.png"):
    try:
        file.unlink()
        print(f"Deleted: {file.name}")
    except OSError as error:
        print(f"Could not delete {file.name}: {error}")