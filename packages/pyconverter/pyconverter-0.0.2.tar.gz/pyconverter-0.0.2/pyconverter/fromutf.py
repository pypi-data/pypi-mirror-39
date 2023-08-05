

# ========================================== #
# ================== UTF8 ================== #
# ========================================== #

# ================== BIN ================== #
def utf8tobin(text: str):
    # Raise error if not string
    if not (type(text) is str):
        raise TypeError("The argument is not a string")

    from .fromint import inttobin

    binary = ""
    for char in text:
        binary += inttobin(ord(char), 8, 8)
    return binary


# ================== HEX ================== #
def utf8tohex(text: str):
    # Raise error if not string
    if not (type(text) is str):
        raise TypeError("The argument is not a string")

    from .frombin import bintohex

    return bintohex(utf8tobin(text))


# ================== OCT ================== #
def utf8tooct(text: str):
    # Raise error if not string
    if not (type(text) is str):
        raise TypeError("The argument is not a string")

    from .frombin import bintooct

    return bintooct(utf8tobin(text))


# =========================================== #
# ================== UTF16 ================== #
# =========================================== #

# ================== BIN ================== #
def utf16tobin(text: str):
    # Raise error if not string
    if not (type(text) is str):
        raise TypeError("The argument is not a string")

    from .fromint import inttobin

    binary = ""
    for char in text:
        binary += inttobin(ord(char), 16, 16)
    return binary


# ================== HEX ================== #
def utf16tohex(text: str):
    # Raise error if not string
    if not (type(text) is str):
        raise TypeError("The argument is not a string")

    from .frombin import bintohex

    return bintohex(utf16tobin(text))


# ================== OCT ================== #
def utf16tooct(text: str):
    # Raise error if not string
    if not (type(text) is str):
        raise TypeError("The argument is not a string")

    from .frombin import bintooct

    return bintooct(utf16tobin(text))
