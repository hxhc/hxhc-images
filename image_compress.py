import os
import pathlib
from PIL import Image
import multiprocessing
import argparse


def compress_image(input_image)->None:
    print(f"Compressing: {input_image}")
    size = os.path.getsize(input_image)
    if size >= 5 * 1024 * 1024:
        quality = 50
    elif size >= 2 * 1024 * 1024:
        quality = 70
    else:
        quality = 95
    with Image.open(input_image) as image:
        image.save(input_image, optimize=True, quality=quality)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", type=str)
    args = parser.parse_args()

    image_list = []
    for ext in ["jpg", "png", "webp"]:
        image_list += [x for x in pathlib.Path(args.file_path).rglob(f"*.{ext}")]
    print(f"Found {len(image_list)} images")
    print("Compressing images...")
    print("======================")
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    for image in image_list:
        pool.apply_async(compress_image, args=(image,))
    pool.close()
    pool.join()
