import hashlib
import sys
import os
from tomlkit import parse

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEPENDENCIES_DIR = os.path.join(SCRIPT_DIR, "../base/assets/dependencies")

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"Error: {e}"

def load_sha256_from_toml(directory):
    hash_list = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".toml"):
                toml_file_path = os.path.join(root, file_name)
                try:
                    with open(toml_file_path, 'r') as file:
                        config = parse(file.read())
                    if 'dependency_config_structure' in config:
                        dependency_config = config['dependency_config_structure']
                        if 'sha_256_hash' in dependency_config:
                            hash_value = str(dependency_config['sha_256_hash']).strip()
                            hash_list.append((toml_file_path, hash_value))  # Save full TOML file path
                except Exception as e:
                    pass
    return hash_list

def main():
    if len(sys.argv) < 2:
        input("No files provided. Press Enter to exit...")
        return

    dependencies_path = os.path.abspath(DEPENDENCIES_DIR)
    hash_list = load_sha256_from_toml(dependencies_path)

    collisions = []
    new_hashes = []

    for file_path in sys.argv[1:]:
        file_path = os.path.normpath(file_path)
        if os.path.isfile(file_path):
            file_hash = calculate_sha256(file_path)
            collision_found = False
            for toml_file_path, db_hash in hash_list:
                if file_hash.strip() == db_hash.strip():
                    collisions.append((file_path, file_hash, toml_file_path, db_hash))  # Store file paths for both
                    collision_found = True
                    break
            if not collision_found:
                new_hashes.append((file_path, file_hash))

    if new_hashes:
        print("\nNew Hashes:")
        for file_path, file_hash in new_hashes:
            print(f"File: {file_path}\n  SHA-256: {file_hash}\n")

    if collisions:
        print("\nCollision Info:")
        for file_path, file_hash, toml_file_path, db_hash in collisions:
            print(f"File: {file_path}\n  SHA-256: {file_hash}\n  Collides with TOML entry in {toml_file_path}\n")

    if not collisions and not new_hashes:
        print("No files processed or no collisions/new hashes found.")

    input("Processing complete. Press Enter to exit...")

if __name__ == "__main__":
    main()
