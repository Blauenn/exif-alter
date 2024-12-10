import os
import shutil
from datetime import datetime, timedelta
import pyexiv2

from exif_update import update_exif_date

source_path = r""
destination_path = r""

overwrite = False


def get_original_date(file_path):
    try:
        if not os.path.isfile(file_path):
            raise ValueError(f"{file_path} is not a file.")
        with pyexiv2.Image(file_path) as img:
            metadata = img.read_exif()
            original_date = metadata.get("Exif.Photo.DateTimeOriginal", None)

            if not original_date:
                raise ValueError(
                    f"No DateTimeOriginal value in the file: {file_path}")

            return original_date
    except Exception as e:
        print(f"Failed to read EXIF data. {e}")
        return None


def update_date_taken(source_path, destination_folder, overwrite=False):
    try:
        if not os.path.exists(source_path):
            raise FileNotFoundError(
                f"Source path does not exist: {source_path}")

        # Create the destination directory if not overwriting #
        if not overwrite and not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # If a single file is given #
        if os.path.isfile(source_path):
            file_to_update = (
                source_path if overwrite
                else os.path.join(destination_folder, os.path.basename(source_path))
            )

            if not overwrite:
                shutil.copy(source_path, file_to_update)

            original_date = get_original_date(source_path)
            if original_date:
                new_time = datetime.strptime(
                    original_date, "%Y:%m:%d %H:%M:%S") + timedelta(hours=12)
                new_date = new_time.strftime("%Y:%m:%d %H:%M:%S")
                update_exif_date(file_to_update, new_date)

            print(f"Metadata updated for file: {file_to_update}")

        # If a directory is given #
        elif os.path.isdir(source_path):
            for filename in os.listdir(source_path):
                file_path = os.path.join(source_path, filename)

                if os.path.isfile(file_path):
                    file_to_update = (
                        file_path if overwrite
                        else os.path.join(destination_folder, filename)
                    )

                    if not overwrite:
                        shutil.copy(file_path, file_to_update)

                    original_date = get_original_date(file_path)
                    if original_date:
                        new_time = datetime.strptime(
                            original_date, "%Y:%m:%d %H:%M:%S") + timedelta(hours=12)
                        new_date = new_time.strftime("%Y:%m:%d %H:%M:%S")
                        update_exif_date(file_to_update, new_date)

                    print(f"Metadata updated for file: {file_to_update}")

        else:
            raise ValueError(
                "Provided source path is neither a file nor a directory.")

    except Exception as error:
        print(f"Wow, {error} happened!!!")


update_date_taken(source_path, destination_path, overwrite=overwrite)
