import os
import shutil
from datetime import datetime, timedelta
import pyexiv2

source_path = r"C:\Blauen\Projects\Photography\[34] SBAC NON SPORTS GAME 2024\Deliver\Pack 6"
destination_path = r"C:\Blauen\Projects\Photography\[34] SBAC NON SPORTS GAME 2024\Deliver\Pack 6 (Timed)"


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


def update_exif_date(file_path, new_date):
    try:
        with pyexiv2.Image(file_path) as img:
            metadata = img.read_exif()
            metadata["Exif.Photo.DateTimeOriginal"] = new_date
            img.modify_exif(metadata)
    except Exception as e:
        print(f"Failed to update EXIF value. {e}")


def update_date_taken(source_path, destination_folder):
    try:
        if not os.path.exists(source_path):
            raise FileNotFoundError(
                f"Source path does not exist: {source_path}")

        os.makedirs(destination_folder, exist_ok=True)

				# If a single file is given #
        if os.path.isfile(source_path):
            destination_file = os.path.join(
                destination_folder, os.path.basename(source_path))

            shutil.copy(source_path, destination_file)

            original_date = get_original_date(source_path)
            if original_date:
                new_time = datetime.strptime(
                    original_date, "%Y:%m:%d %H:%M:%S") + timedelta(hours=12)
                new_date = new_time.strftime("%Y:%m:%d %H:%M:%S")
                update_exif_date(destination_file, new_date)

            print(f"Metadata updated for file: {destination_file}")
            
        # If a directory is given #
        elif os.path.isdir(source_path):
            for filename in os.listdir(source_path):
                file_path = os.path.join(source_path, filename)

                if os.path.isfile(file_path):
                    destination_file = os.path.join(
                        destination_folder, filename)

                    shutil.copy(file_path, destination_file)

                    original_date = get_original_date(file_path)
                    if original_date:
                        new_time = datetime.strptime(
                            original_date, "%Y:%m:%d %H:%M:%S") + timedelta(hours=12)
                        new_date = new_time.strftime("%Y:%m:%d %H:%M:%S")
                        update_exif_date(destination_file, new_date)

                    print(f"Metadata updated for file: {destination_file}")

        else:
            raise ValueError(
                "Provided source path is neither a file nor a directory.")

    except Exception as error:
        print(f"Wow, {error} happened!!!")


# Run the function
update_date_taken(source_path, destination_path)
