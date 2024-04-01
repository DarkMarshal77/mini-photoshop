from Core import File


class Handler:
    def __init__(self):
        self.states = []

    @staticmethod
    def read_image(path):
        return File.open_image(path)


if __name__ == '__main__':
    Handler.read_image("../input/image1.bmp")
