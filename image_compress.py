import os
import pathlib
from PIL import Image
import multiprocessing

def compress_image(input_image):
    print(f"Compressing: {input_image}")
    size = os.path.getsize(input_image)
    if size >= 5 * 1024 * 1024:
        quality = 50
    else:
        quality = 70

    with Image.open(input_image) as image:

        image.save(input_image, optimize=True, quality=quality)


if __name__ == "__main__":
    image_list = []
    for ext in ["jpg", "png", "webp"]:
        image_list +=  [x for x in pathlib.Path("./content").rglob(f"*.{ext}")]
    print(f"Found {len(image_list)} images")
    print("Compressing images...")
    print("======================")
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    for image in image_list:
        pool.apply_async(compress_image, args=(image,))
    pool.close()
    pool.join()


