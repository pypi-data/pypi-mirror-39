

# ============================================================ #
# ================== SINGLE PRECISION FLOAT ================== #
# ============================================================ #

# ================== BIN ================== #
def floattobin(fl: float):
    # Raise error if not float
    if not (type(fl) is float):
        raise TypeError("The argument is not a float")
    return _floattobin(fl, 8, 23)


# ================== HEX ================== #
def floattohex(fl: float):
    # Raise error if not float
    if not (type(fl) is float):
        raise TypeError("The argument is not a float")

    from .frombin import bintohex

    return bintohex(floattobin(fl))


# ================== OCT ================== #
def floattooct(fl: float):
    # Raise error if not float
    if not (type(fl) is float):
        raise TypeError("The argument is not a float")

    from .frombin import bintooct

    return bintooct(floattobin(fl))


# ============================================================ #
# ================== DOUBLE PRECISION FLOAT ================== #
# ============================================================ #

# ================== BIN ================== #
def doubletobin(db: float):
    # Raise error if not float
    if not (type(db) is float):
        raise TypeError("The argument is not a float")
    return _floattobin(db, 11, 52)


# ================== HEX ================== #
def doubletohex(db: float):
    # Raise error if not float
    if not (type(db) is float):
        raise TypeError("The argument is not a float")

    from .frombin import bintohex

    return bintohex(doubletobin(db))


# ================== OCT ================== #
def doubletooct(db: float):
    # Raise error if not float
    if not (type(db) is float):
        raise TypeError("The argument is not a float")

    from .frombin import bintooct

    return bintooct(doubletobin(db))


# ================================================== #
# ================== COMMON FLOAT ================== #
# ================================================== #

# ================== BIN ================== #
def _floattobin(fl: float, exponentbit: int, mantissabit: int):
    # Raise error if not float
    if not (type(fl) is float):
        raise TypeError("The argument is not a float")

    from .fromint import inttobin

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
