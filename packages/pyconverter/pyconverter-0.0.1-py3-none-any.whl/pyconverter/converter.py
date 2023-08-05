# -*- coding: utf8 -*-

HEXVALUE = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

# ============================================== #
# ================== FROM BIN ================== #
# ============================================== #


# ================== CHECK IF BINARY ================== #
def is_bin(binary):
    # Verify if number is a binary number (example : 10101)
    if type(binary) is str and binary.isdigit():
        for digit in binary:
            if not (int(digit) == 0 or int(digit) == 1):
                return False
    else:
        return False
    return True


# ================== DECIMAL ================== #
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
    return _bintofloat(binary, 8, 23)


# ================== DOUBLE PRECISION FLOAT ================== #
def bintodouble(binary):
    # If number is int, convert to string
    if type(binary) is int:
        binary = str(binary)
    # Raise error if not in binary format
    if not is_bin(binary):
        raise TypeError("The argument is not binary")
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


# ============================================ #
# ================== TO BIN ================== #
# ============================================ #

# ================== UTF8 ================== #
def utf8tobin(text: str):
    # Raise error if not string
    if not (type(text) is str):
        raise TypeError("The argument is not a string")
    binary = ""
    for char in text:
        binary += inttobin(ord(char), 8, 8)
    return binary


# ================== UTF16 ================== #
def utf16tobin(text: str):
    # Raise error if not string
    if not (type(text) is str):
        raise TypeError("The argument is not a string")
    binary = ""
    for char in text:
        binary += inttobin(ord(char), 16, 16)
    return binary


# ================== DECIMAL ================== #
def inttobin(dec: int, minbit: int = 8, maxbit: int = -1):
    # Raise error if not int
    if not (type(dec) is int) and (type(minbit) is int) and (type(maxbit) is int):
        raise TypeError("Arguments are not a int")

    # Get the minimum and maximum bits to return
    binary = ""
    if maxbit == -1:
        while dec > (2**minbit)-1:
            minbit += 1
    else:
        while dec > (2**minbit)-1 and minbit <= maxbit:
            minbit += 1

    # Convert decimal to bin
    for i in range(minbit - 1, -1, -1):
        if dec >= 2**i:
            dec -= 2**i
            binary += "1"
        else:
            binary += "0"
    return binary


# ================== SINGLE PRECISION FLOAT ================== #
def floattobin(fl: float):
    # Raise error if not float
    if not (type(fl) is float):
        raise TypeError("The argument is not a float")
    return _floattobin(fl, 8, 23)


# ================== DOUBLE PRECISION FLOAT ================== #
def doubletobin(db: float):
    # Raise error if not float
    if not (type(db) is float):
        raise TypeError("The argument is not a float")
    return _floattobin(db, 11, 52)


# ================== COMMON FLOAT ================== #
def _floattobin(fl: float, exponentbit: int, mantissabit: int):
    # Raise error if not float
    if not (type(fl) is float):
        raise TypeError("The argument is not a float")

    sign = 0
    mantissa = ""

    # Get the sign
    if fl < 0:
        sign = 1
        fl = -fl

    # Get the integer value and add to mantissa
    intvalue = 0
    while not (0 <= fl < 1):
        intvalue += 1
        fl -= 1
    mantissa += inttobin(intvalue, 1, mantissabit + 1)
    mantissa += "."

    # Get the decimal value and add to mantissa
    for i in range(1, (mantissabit + 1) * 2):
        if 1/(2**i) <= fl:
            mantissa += "1"
            fl -= (1/(2**i))
        else:
            mantissa += "0"

    # Get the exponent and makes the mantissa compliant with the IEEE 754 standard
    # (https://en.wikipedia.org/wiki/IEEE_754)
    exponent = 0
    mantissafloat = float(mantissa)
    while not (2 > mantissafloat >= 1):
        indexpoint = mantissa.index(".")

        if mantissafloat > 1:
            exponent += 1
            tmp = mantissa[indexpoint - 1]
            mantissa = mantissa[:indexpoint-1] + "." + mantissa[indexpoint:]
            mantissa = mantissa[:indexpoint] + tmp + mantissa[indexpoint + 1:]

        else:
            exponent -= 1
            tmp = mantissa[indexpoint + 1]
            mantissa = mantissa[:indexpoint + 1] + "." + mantissa[indexpoint + 2:]
            mantissa = mantissa[:indexpoint] + tmp + mantissa[indexpoint + 1:]
        mantissafloat = float(mantissa)

    # Convert exponent to binary format
    expbin = inttobin(exponent + ((2 ** (exponentbit - 1)) - 1), exponentbit, exponentbit)
    for i in range(0, mantissabit + 2):
        mantissa += "0"

    return str(sign) + expbin + mantissa[2:mantissabit+2]


# ============================================ #
# ================== TO HEX ================== #
# ============================================ #


# ================== BIN ================== #
def bintohex(binary):
    # If number is int, convert to string
    if type(binary) is int:
        binary = str(binary)
    # Raise error if not in binary format
    if not is_bin(binary):
        raise TypeError("The argument is not binary")

    hexa = hex(bintoint(binary))[2:].upper()

    return hexa


# ================== UTF8 ================== #
def utf8tohex(text: str):
    # Raise error if not string
    if not (type(text) is str):
        raise TypeError("The argument is not a string")

    return bintohex(utf8tobin(text))


# ================== UTF16 ================== #
def utf16tohex(text: str):
    # Raise error if not string
    if not (type(text) is str):
        raise TypeError("The argument is not a string")

    return bintohex(utf16tobin(text))


# ================== DECIMAL ================== #
def inttohex(dec: int):
    # Raise error if not int
    if not (type(dec) is int):
        raise TypeError("The argument is not a int")

    return hex(dec)[2:].upper()


# ================== SINGLE PRECISION FLOAT ================== #
def floattohex(fl: float):
    # Raise error if not float
    if not (type(fl) is float):
        raise TypeError("The argument is not a float")

    return bintohex(floattobin(fl))


# ================== DOUBLE PRECISION FLOAT ================== #
def doubletohex(db: float):
    # Raise error if not float
    if not (type(db) is float):
        raise TypeError("The argument is not a float")

    return bintohex(doubletobin(db))


# ============================================== #
# ================== FROM HEX ================== #
# ============================================== #

# ================== CHECK IF BINARY ================== #
def is_hex(hexa: str):
    # Raise error if not string
    if not (type(hexa) is str):
        raise TypeError("The argument is not a string")

    # Remove the possible 0x
    if hexa.startswith("0x"):
        hexa = hexa[2:]

    # Check if all char is a hexadecimal value
    hexa = hexa.upper()
    for value in hexa:
        if value not in HEXVALUE:
            return False
    return True


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

    return bintodouble(hextobin(hexa))
