import ctypes
from cimageio import ImageValueError


class BYTE_BUFFER(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.c_void_p),
        ('size', ctypes.c_size_t),
    ]


class ARRAY_BUFFER(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.c_void_p),
        ('height', ctypes.c_uint),
        ('width', ctypes.c_uint),
        ('color_type', ctypes.c_int),
        ('bit_depth', ctypes.c_int),
    ]


# Some utility functions
def get_array_header(array,
                     codec,
                     color_type_hint=None,
                     allowables=None):
    if not allowables:
        allowables = [
            (8, 'GRAY'),
            (16, 'GRAY'),
            (8, 'RGB'),
            (8, 'RGBA'),
        ]

    # Parse bit-depth
    bit_depth = array.dtype.itemsize * 8

    # Parse color type
    if color_type_hint:
        color_type = color_type_hint
    elif not (2 <= array.ndim <= 3):
        color_type = None
    elif array.ndim == 2 or (array.ndim == 3 and array.shape[2] == 1):
        color_type = 'GRAY'
    elif array.shape[2] == 3:
        color_type = 'RGB'
    else:
        color_type = 'RGBA'

    # Check
    if (bit_depth, color_type) not in allowables:
        raise ImageValueError(bit_depth, color_type, codec)

    return bit_depth, color_type
