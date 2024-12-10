import pyexiv2


def update_exif_date(file_path, new_date):
    try:
        with pyexiv2.Image(file_path) as img:
            metadata = img.read_exif()
            metadata["Exif.Photo.DateTimeOriginal"] = new_date
            img.modify_exif(metadata)
    except Exception as e:
        print(f"Failed to update EXIF value. {e}")
