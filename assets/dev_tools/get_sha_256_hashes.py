import hashlib
import sys
import os

def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"Error: {e}"

def main():
    # Check if files were dragged onto the script
    if len(sys.argv) < 2:
        print("No files provided. Drag and drop files onto this script.")
        input("Press Enter to exit...")
        return

    print("Processing files:\n")

    for file_path in sys.argv[1:]:
        if os.path.isfile(file_path):
            print(f"File: {file_path}")
            print(f"SHA-256: {calculate_sha256(file_path)}\n")
        else:
            print(f"Skipped (not a file): {file_path}\n")

    input("Processing complete. Press Enter to exit...")

if __name__ == "__main__":
    main()