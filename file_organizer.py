#!/usr/bin/env python3

import os
import shutil


def organize_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            source_file_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1].lower()
            if extension:
                # Construct the destination folder path while preserving the original folder structure
                if os.path.exists(os.path.join(folder_path, extension[1:])):
                    destination_file_path = os.path.join(
                        folder_path,
                        extension[1:],
                        os.path.relpath(root, source_file_path),
                    )
                    if os.path.exists(destination_file_path):
                        continue
                relative_path = os.path.relpath(root, folder_path)
                destination_folder = os.path.join(
                    folder_path, extension[1:], relative_path
                )
                os.makedirs(destination_folder, exist_ok=True)
                destination_file_path = os.path.join(destination_folder, file)

                # Check if the file already exists in the destination folder
                if not os.path.exists(destination_file_path):
                    shutil.move(source_file_path, destination_file_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python file_organizer.py <folder_path>")
    else:
        folder_path = sys.argv[1]

        if os.path.exists(folder_path):
            organize_folder(folder_path)
            print("Folder organized successfully!")
        else:
            print("Invalid folder path.")
