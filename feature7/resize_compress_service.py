from .sub import subscribe_channel
from PIL import Image
import os
import time
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def resize_compress_image(file_name):
    time.sleep(5)

    file_path = os.path.join(BASE_DIR, "uploads", file_name)
    quality=70
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist!")

    with Image.open(file_path) as img:
        # cmpress 
        ext = img.format if img.format else "PNG"
        if ext.upper() == "PNG":
            img.save(file_path, "PNG", optimize=True)
        else:
            img = img.convert("RGB") 
            img.save(file_path, "JPEG", optimize=True, quality=quality)

        # resize
        resized_img = img.resize((1080, 1350))
        resized_img.save(file_path)
    return file_path


if __name__ == "__main__":
    subscribe_channel("channel1", "Resize Compress Service", resize_compress_image)