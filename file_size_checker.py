import os
import sys
from pathlib import Path

def check_file_sizes(folder_path, size_limit_mb):
    """
    Check files in folder and subfolders for files exceeding the size limit
    
    Args:
        folder_path (str): Path to the folder to check
        size_limit_mb (float): Size limit in megabytes
    """
    # Convert MB to bytes for comparison
    size_limit_bytes = size_limit_mb * 1024 * 1024
    large_files = []

    try:
        # Walk through all folders and subfolders
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Get file size
                    file_size = os.path.getsize(file_path)
                    
                    # If file size exceeds limit, add to list
                    if file_size > size_limit_bytes:
                        size_mb = file_size / (1024 * 1024)  # Convert to MB for display
                        large_files.append((file_path, size_mb))
                except OSError as e:
                    print(f"Error accessing file {file_path}: {e}")

        # Report results
        if large_files:
            print(f"\nFound {len(large_files)} files exceeding {size_limit_mb} MB:")
            print("-" * 80)
            for file_path, size in large_files:
                print(f"File: {file_path}")
                print(f"Size: {size:.2f} MB")
                print("-" * 80)
        else:
            print(f"\nNo files found exceeding {size_limit_mb} MB")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Get folder path from user if not provided
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = input("Enter the folder path to check: ")

    # Get size limit from user if not provided
    if len(sys.argv) > 2:
        try:
            size_limit = float(sys.argv[2])
        except ValueError:
            print("Invalid size limit. Please enter a number.")
            return
    else:
        while True:
            try:
                size_limit = float(input("Enter size limit in MB (e.g., 50 for 50MB): "))
                break
            except ValueError:
                print("Please enter a valid number.")

    # Convert path to absolute path and check if it exists
    folder_path = os.path.abspath(folder_path)
    if not os.path.exists(folder_path):
        print(f"Error: The path '{folder_path}' does not exist.")
        return
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a directory.")
        return

    # Run the check
    check_file_sizes(folder_path, size_limit)

if __name__ == "__main__":
    main()
