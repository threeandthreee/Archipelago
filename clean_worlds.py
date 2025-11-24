import os

ROOT = "worlds"

for dirpath, dirnames, filenames in os.walk(ROOT, topdown=False):
    # Remove __pycache__ directories
    for d in dirnames:
        if d == "__pycache__":
            full = os.path.join(dirpath, d)
            try:
                # Remove all files inside first
                for f in os.listdir(full):
                    os.remove(os.path.join(full, f))
                os.rmdir(full)
            except OSError:
                pass

    # After removing pycache, delete directory if empty
    try:
        if not os.listdir(dirpath):
            os.rmdir(dirpath)
    except OSError:
        pass
