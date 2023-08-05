from .checks import is_hex
from .Constants import HEXVALUE


# ================== BIN ================== #
def hextobin(hexa: str):
    # Raise error if not string
    if not (type(hexa) is str):
        raise TypeError("The argument is not a string")

    # Remove the possible 0x
    if hexa.startswith('0x'):
        hexa = hexa[2:]
    hexa = hexa.upper()

    # Raise error if not hexadecimal format
    if not is_hex(hexa):
        raise TypeError("The argument is not hexadecimal")

    from .fromint import inttobin

    return inttobin(hextoint(hexa))


# ================== DECIMAL ================== #
def hextoint(hexa: str):
    # Raise error if not string
    if not (type(hexa) is str):
        raise TypeError("The argument is not a string")

    # Remove the possible 0x
    if hexa.startswith('0x'):
        hexa = hexa[2:]
    hexa = hexa.upper()

    # Raise error if not hexadecimal format
    if not is_hex(hexa):
        raise TypeError("The argument is not hexadecimal")

    dec = 0
    for value in hexa:
        dec += HEXVALUE.index(value)

    return dec


# ================== UTF8 ================== #
def hextoutf8(hexa: str):
    # Raise error if not string
    if not (type(hexa) is str):
        raise TypeError("The argument is not a string")

    # Remove the possible 0x
    if hexa.startswith('0x'):
        hexa = hexa[2:]
    hexa = hexa.upper()

    # Raise error if not hexadecimal format
    if not is_hex(hexa):
        raise TypeError("The argument is not hexadecimal")

    from .frombin import bintoutf8

    return bintoutf8(hextobin(hexa))


# ================== UTF16 ================== #
def hextoutf16(hexa: str):
    # Raise error if not string
    if not (type(hexa) is str):
        raise TypeError("The argument is not a string")

    # Remove the possible 0x
    if hexa.startswith('0x'):
        hexa = hexa[2:]
    hexa = hexa.upper()

    # Raise error if not hexadecimal format
    if not is_hex(hexa):
        raise TypeError("The argument is not hexadecimal")

    from .frombin import bintoutf16

    return bintoutf16(hextobin(hexa))


# ================== SINGLE PRECISION FLOAT ================== #
def hextofloat(hexa: str):
    # Raise error if not string
    if not (type(hexa) is str):
        raise TypeError("The argument is not a string")

    # Remove the possible 0x
    if hexa.startswith('0x'):
        hexa = hexa[2:]
    hexa = hexa.upper()

    # Raise error if not hexadecimal format
    if not is_hex(hexa):
        raise TypeError("The argument is not hexadecimal")

    from .frombin import bintofloat

    return bintofloat(hextobin(hexa))


# ================== DOUBLE PRECISION FLOAT ================== #
def hextodouble(hexa: str):
    # Raise error if not string
    if not (type(hexa) is str):
        raise TypeError("The argument is not a string")

    # Remove the possible 0x
    if hexa.startswith('0x'):
        hexa = hexa[2:]
    hexa = hexa.upper()

    # Raise error if not hexadecimal format
    if not is_hex(hexa):
        raise TypeError("The argument is not hexadecimal")

    from .frombin import bintodouble

    return bintodouble(hextobin(hexa))


# ================== OCT ================== #
def hextooct(hexa: str):
    # Raise error if not string
    if not (type(hexa) is str):
        raise TypeError("The argument is not a string")

    # Remove the possible 0x
    if hexa.startswith('0x'):
        hexa = hexa[2:]
    hexa = hexa.upper()

    # Raise error if not hexadecimal format
    if not is_hex(hexa):
        raise TypeError("The argument is not hexadecimal")

    return oct(hextoint(hexa))[2:].upper()
