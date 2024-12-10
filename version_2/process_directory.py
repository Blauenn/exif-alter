import os
from pathlib import Path
from datetime import datetime, timedelta

from exif_functions import exif_update
from exif_functions import exif_get_original_date

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".dng", ".tiff")

SOURCE_DIRECTORY = r""
DESTINATION_DIRECTORY = r""
ADDED_HOURS = 12


def validate_directory(directory):
    if not os.path.isdir(directory):
        raise ValueError(f"{directory} is not a valid directory.")


def process_directory(input_directory, output_directory, added_hours):
    for root, _, files, in os.walk(input_directory):
        relative_path = os.path.relpath(root, input_directory)
        new_directory = os.path.join(output_directory, relative_path)

        os.makedirs(new_directory, exist_ok=True)

        for file in files:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(new_directory, file)

                original_date = exif_get_original_date(input_file_path)
                if not original_date:
                    continue

                try:
                    new_time = datetime.strptime(
                        original_date, "%Y:%m:%d %H:%M:%S") + timedelta(hours=added_hours)
                    new_date = new_time.strftime("%Y:%m:%d %H:%M:%S")

                    exif_update(new_date, input_file_path, output_file_path)
                except Exception as e:
                    print(f"Failed to process file {input_file_path}\n{e}")


if __name__ == "__main__":
    try:
        validate_directory(SOURCE_DIRECTORY)
        os.makedirs(DESTINATION_DIRECTORY, exist_ok=True)

        process_directory(SOURCE_DIRECTORY, DESTINATION_DIRECTORY, ADDED_HOURS)
        print("Processing complete.")
    except Exception as e:
        print(f"Error: {e}")
