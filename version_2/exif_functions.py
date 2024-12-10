import os
import shutil
import pyexiv2


def exif_update(new_date, source_path, destination_path):
    try:
        if os.path.abspath(source_path) == os.path.abspath(destination_path):
            raise ValueError(
                "Source and destination paths cannot be the same.")

        shutil.copy2(source_path, destination_path)
        print(f"The image file has been copied to {destination_path}")

        with pyexiv2.Image(destination_path) as img:
            metadata = img.read_exif()
            metadata["Exif.Photo.DateTimeOriginal"] = new_date
            img.modify_exif(metadata)

        print(f"Updated EXIF value of {source_path}")

    except Exception as e:
        print(f"Failed to update the EXIF value of file: {source_path}\n{e}")


def exif_get_original_date(file_path):
    try:
        if not os.path.isfile(file_path):
            raise ValueError(f"{file_path} is not a file.")

        with pyexiv2.Image(file_path) as img:
            metadata = img.read_exif()
            original_date = metadata.get("Exif.Photo.DateTimeOriginal")

            if not original_date:
                raise ValueError(
                    f"No DateTimeOriginal value in the file: {file_path}")

        return original_date
    except Exception as e:
        print(f"Failed to read EXIF data.\n{e}")
        return None
