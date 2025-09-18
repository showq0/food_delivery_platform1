from .sub import subscribe_channel
from PIL import Image
import os
import time
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def check_image_quality(file_name):
    """
    {
    format,
    dimensions, 
    file_size, 
    mode
    }
    """
    time.sleep(5)
    file_path = os.path.join(BASE_DIR, "uploads", file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist!")
    with Image.open(file_path) as img:
        info = {
            "format": img.format,
            "mode": img.mode,
            "dimensions": img.size,
            "file_size_kb": round(os.path.getsize(file_path) / 1024,1)
        }
    return info


if __name__ == "__main__":
    subscribe_channel("channel1", "Quality Service", check_image_quality)