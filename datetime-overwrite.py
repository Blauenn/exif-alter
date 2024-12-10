import os
import shutil
import pyexiv2

source_path = r""
destination_path = r""
new_date = "2024:08:09 17:27:32"


def update_date_taken(source_path, destination_path, new_date):
    try:
        # Validate source path
        if not os.path.exists(source_path):
            raise FileNotFoundError(
                f"Source file does not exist: {source_path}")

        if not new_date:
            raise ValueError(
                "New date must be provided in 'YYYY:MM:DD HH:MM:SS' format.")

        shutil.copy(source_path, destination_path)

        with pyexiv2.Image(destination_path) as img:
            metadata = img.read_exif()
            metadata["Exif.Photo.DateTimeOriginal"] = new_date
            metadata["Exif.Photo.DateTimeDigitized"] = new_date
            img.modify_exif(metadata)

        print(f"Metadata updated and saved to: {destination_path}")

    except Exception as error:
        print(f"Wow, {error} happened!!!")


update_date_taken(source_path, destination_path, new_date)
