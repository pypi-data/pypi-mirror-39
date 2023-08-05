

# ================== BIN ================== #
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


# ================== HEX ================== #
def inttohex(dec: int):
    # Raise error if not int
    if not (type(dec) is int):
        raise TypeError("The argument is not a int")

    return hex(dec)[2:].upper()
