import ctypes
from six import iterkeys, itervalues, iteritems
import numpy as np
from cimageio import __lib__
from cimageio._common import ARRAY_BUFFER, BYTE_BUFFER, get_array_header


__PNG_COLOR_TYPE__ = {
    'GRAY': 0,
    'RGB': 2,
    'PALETTE': 3,
    'RGBA': 2 | 4,
}

__PNG_ALLOWABLE__ = [
    (8, 'GRAY'),
    (16, 'GRAY'),
    (8, 'RGB'),
    (8, 'RGBA'),
]

__lib__.encode_to_png.argtypes = [
    ctypes.POINTER(ARRAY_BUFFER),
    ctypes.POINTER(BYTE_BUFFER),
    ctypes.c_uint,
]
__lib__.encode_to_png.restype = ctypes.c_int

__lib__.decode_from_png.argtypes = [
    ctypes.POINTER(BYTE_BUFFER),
    ctypes.POINTER(ARRAY_BUFFER),
]
__lib__.decode_from_png.restype = ctypes.c_int


def encode_to_png(array,
                  compression_level=6,
                  color_type='auto'):
    """
    Encode numpy.ndarray to PNG format byte-string
    :param array: (numpy.ndarray) Image array to encode. dtype of array should be uint8 or uint16.
    :param compression_level: (int) Compression level. One of 0~9
    :param color_type: (str) Specification of how color channel consisted of. See
                       __PNG_COLOR_TYPE__
    :return: (bytes) byte-string formatted with PNG
    """
    # Parse information from array
    color_type = None if color_type == 'auto' else color_type
    bit_depth, color_type = get_array_header(array, 'png', color_type, __PNG_ALLOWABLE__)

    # Change to big-endian order
    array = array.astype('>u' + str(bit_depth // 8))

    # Pack to C array
    array_buffer = ARRAY_BUFFER(
        array.ctypes.data_as(ctypes.c_void_p),
        array.shape[0],
        array.shape[1],
        __PNG_COLOR_TYPE__[color_type],
        bit_depth,
    )
    byte_buffer = BYTE_BUFFER(
        None,
        0
    )

    # Run C code
    code = __lib__.encode_to_png(ctypes.byref(array_buffer),
                                 ctypes.byref(byte_buffer),
                                 compression_level)
    if code:
        raise RuntimeError('Encoding failed')

    # Unpack to numpy.ndarray
    byte_string = (ctypes.c_byte * byte_buffer.size).from_address(byte_buffer.data)
    byte_string = bytearray(byte_string)
    return byte_string


def decode_from_png(byte_string):
    """
    Decode PNG format byte-string to np.ndarray
    :param byte_string: (bytes) Byte-string to decode.
    :return: (numpy.ndarray) Decoded image array.
    """
    # Pack to C array
    byte_buffer = BYTE_BUFFER(
        ctypes.cast(byte_string, ctypes.c_void_p),
        len(byte_string),
    )
    array_buffer = ARRAY_BUFFER(
        None,
        0,
        0,
        0,
        0,
    )

    # Run C code
    code = __lib__.decode_from_png(ctypes.byref(byte_buffer), ctypes.byref(array_buffer))
    if code:
        raise RuntimeError('Decoding failed')
    height, width = array_buffer.height, array_buffer.width
    bit_depth = array_buffer.bit_depth
    color_type = None
    for k, v in iteritems(__PNG_COLOR_TYPE__):
        if array_buffer.color_type == v:
            color_type = k
            break
    if color_type is None:
        raise ValueError('Unsupported PNG color type %d' % array_buffer.color_type)
    color_channel = 1 if color_type == 'GRAY' else \
                    2 if color_type == 'GRAYA' else \
                    3 if color_type == 'PALETTE' else \
                    3 if color_type == 'RGB' else \
                    4

    # Get array length
    array_length = height * width * (bit_depth // 8) * color_channel
    array_string = (ctypes.c_byte * array_length).from_address(array_buffer.data)
    array = np.frombuffer(array_string, dtype='>u' + str(bit_depth // 8))
    array = array.astype('=u' + str(bit_depth // 8))
    array = np.resize(array, [height, width, color_channel])
    array = array.squeeze()
    return array
