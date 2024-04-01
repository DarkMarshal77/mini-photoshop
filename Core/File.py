import numpy as np


def open_image(file_path):
    def btoi(b):
        return int.from_bytes(b, byteorder='little')

    def parse_header(f):
        f.seek(14)
        assert btoi(f.read(4)) == 40  # header size
        w = btoi(f.read(4))
        h = btoi(f.read(4))
        f.read(2)
        assert btoi(f.read(2)) == 24  # bits per pixel
        assert btoi(f.read(4)) == 0  # compression
        f.seek(54)

        return h, w

    with open(file_path, 'rb') as img_file:
        height, width = parse_header(img_file)
        img = []
        for _ in range(height):
            img.insert(0, [])
            for _ in range(width):
                b = btoi(img_file.read(1))
                g = btoi(img_file.read(1))
                r = btoi(img_file.read(1))
                img[0].append([r, g, b])

    return np.require(img, np.uint8, 'C'), height, width


def save_as(image, path, format):
    pass
