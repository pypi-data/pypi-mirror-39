import ctypes
from os.path import join


# Error definitions
class ImageValueError(Exception):
    def __init__(self, bit_depth, color_type, codec):
        message = 'Unsupported type for {}: ({}-bit / {})'
        message = message.format(codec, bit_depth, color_type)
        super(ImageValueError, self).__init__(message)


# Load compiled library
if '__lib__' not in globals():
    __lib__ = ctypes.cdll.LoadLibrary(join(__path__[0], 'libcimageio.so'))


from cimageio.png import encode_to_png, decode_from_png
from cimageio.jpeg import encode_to_jpeg, decode_from_jpeg


def imread(file, image_type='auto'):
    """

    :param file:
    :param image_type:
    :return:
    """
    from os.path import splitext

    file_opened_by_function = False

    if isinstance(file, str):
        # Parse dtype from filename
        if image_type == 'auto':
            image_type = splitext(file)[-1]
        file = open(file, 'rb')
        file_opened_by_function = True

    contents = file.read()
    image_type = image_type.lstrip('.').lower()
    if image_type == 'png':
        contents = decode_from_png(contents)
    elif image_type == 'jpeg' or image_type == 'jpg':
        contents = decode_from_jpeg(contents)
    else:
        raise ValueError('Unsupported image type: {}'.format(image_type))

    if file_opened_by_function:
        file.close()
    return contents


def imwrite(file, contents, image_type='auto'):
    """

    :param file:
    :param contents:
    :param image_type:
    :return:
    """
    from os.path import splitext

    file_opened_by_function = False

    if isinstance(file, str):
        # Parse dtype from filename
        if image_type == 'auto':
            image_type = splitext(file)[-1]
        file = open(file, 'wb')
        file_opened_by_function = True

    image_type = image_type.lstrip('.').lower()
    if image_type == 'png':
        contents = encode_to_png(contents)
    elif image_type in['jpeg', 'jpg']:
        contents = encode_to_jpeg(contents)
    else:
        raise ValueError('Unsupported image type: {}'.format(image_type))
    file.write(contents)

    if file_opened_by_function:
        file.close()


__all__ = [
    'ImageValueError',
    'encode_to_png', 'decode_from_png',
    'encode_to_jpeg', 'decode_from_jpeg',
    'imread', 'imwrite',
]
