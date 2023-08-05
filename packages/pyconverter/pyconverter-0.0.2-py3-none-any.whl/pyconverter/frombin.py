from .checks import is_bin


# ================== INTEGER ================== #
def bintoint(binary):
    # If number is int, convert to string
    if type(binary) is int:
        binary = str(binary)
    # Raise error if not in binary format
    if not is_bin(binary):
        raise TypeError("The argument is not binary")

    # Calculate decimal from binary
    dec = 0
    for i in range(len(binary) - 1, -1, -1):
        if int(binary[0]):
            dec += 2**i
        binary = binary[1:]
    return dec


# ================== UTF8 ================== #
def bintoutf8(binary):
    # If number is int, convert to string
    if type(binary) is int:
        binary = str(binary)
    # Raise error if not in binary format
    if not is_bin(binary):
        raise TypeError("The argument is not binary")
    return _bintoutf(binary, 8)


# ================== UTF16 ================== #
def bintoutf16(binary):
    # If number is int, convert to string
    if type(binary) is int:
        binary = str(binary)
    # Raise error if not in binary format
    if not is_bin(binary):
        raise TypeError("The argument is not binary")
    return _bintoutf(binary, 16)


# ================== COMMON UTF ================== #
def _bintoutf(binary, typeutf: int = 8):
    # Get binary letter by letter
    binary_split = []
    while not (binary == ""):
        binary_split.append(binary[:typeutf])
        binary = binary[typeutf:]

    # Convert binary to utf with chr()
    text = ""
    for byte in binary_split:
        text += chr(bintoint(byte))

    return text


# ================== SINGLE PRECISION FLOAT ================== #
def bintofloat(binary):
    # If number is int, convert to string
    if type(binary) is int:
        binary = str(binary)
    # Raise error if not in binary format
    if not is_bin(binary):
        raise TypeError("The argument is not binary")
    # Raise error if binary is not the correct lenght
    if not len(binary) == 64:
        raise ValueError("The binary is not a double (must be 64-bits long)")

    return _bintofloat(binary, 8, 23)


# ================== DOUBLE PRECISION FLOAT ================== #
def bintodouble(binary):
    # If number is int, convert to string
    if type(binary) is int:
        binary = str(binary)
    # Raise error if not in binary format
    if not is_bin(binary):
        raise TypeError("The argument is not binary")
    # Raise error if binary is not the correct lenght
    if not len(binary) == 64:
        raise ValueError("The binary is not a double (must be 64-bits long)")

    return _bintofloat(binary, 11, 52)


# ================== COMMON FLOAT ================== #
def _bintofloat(binary, exponentbit: int, mantissabit: int):
    # Get the sign of float (0: +, 1: -)
    sign = ""
    if int(binary[0]):
        sign = "-"
    binary = binary[1:]

    # Get the binary of exponenent and convert to a decimal value
    exponentbin = binary[:exponentbit]
    binary = binary[exponentbit:]
    exponent = bintoint(exponentbin) - ((2 ** (exponentbit - 1)) - 1)

    # Convert the rest of the binary (mantissa) to float
    decimal = 1.0
    for i in range(1, mantissabit + 1):
        if int(binary[0]):
            decimal += (1 / 2 ** i)
        binary = binary[1:]

    return float(sign + str(decimal * (2**exponent)))


# ================== HEX ================== #
def bintohex(binary):
    # If number is int, convert to string
    if type(binary) is int:
        binary = str(binary)
    # Raise error if not in binary format
    if not is_bin(binary):
        raise TypeError("The argument is not binary")

    hexa = hex(bintoint(binary))[2:].upper()

    return hexa


# ================== OCT ================== #
def bintooct(binary):
    # If number is int, convert to string
    if type(binary) is int:
        binary = str(binary)
    # Raise error if not in binary format
    if not is_bin(binary):
        raise TypeError("The argument is not binary")

    octa = oct(bintoint(binary))[2:].upper()

    return octa
