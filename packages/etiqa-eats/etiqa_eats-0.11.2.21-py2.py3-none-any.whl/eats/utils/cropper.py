from PIL import Image


class Cropper(object):

    @staticmethod
    def crop_top(image, top):
        width, height = image.size
        return Cropper.crop(image, 0, top, width, height)

    @staticmethod
    def crop_bottom(image, bottom):
        width, height = image.size
        return Cropper.crop(image, 0, 0, width, height - bottom)

    @staticmethod
    def crop_left(image, left):
        width, height = image.size
        return Cropper.crop(image, 0, left, width, height)

    @staticmethod
    def crop_right(image, right):
        width, height = image.size
        return Cropper.crop(image, 0, 0, width - right, height)

    @staticmethod
    def crop(img, x, y, width=None, height=None):
        img_width, img_height = img.size
        if not width:
            width = img_width
        if not height:
            height = img_height
        return img.crop((x, y, width, height))

    @staticmethod
    def image(path):
        return Image.open(path)

    @staticmethod
    def save(image, path):
        image.save(path)

    @staticmethod
    def merge_images(file_name, images):
        total_width = 0
        total_height = 0
        for image in images:
            img = Image.open(image)
            width, height = img.size
            total_width += width
            total_height += height
        new_im = Image.new('RGB', (width, total_height))
        total_width = 0
        total_height = 0
        for image in images:
            img = Image.open(image)
            width, height = img.size
            new_im.paste(img, (0, total_height))
            total_width += width
            total_height += height
        new_im.save(file_name)