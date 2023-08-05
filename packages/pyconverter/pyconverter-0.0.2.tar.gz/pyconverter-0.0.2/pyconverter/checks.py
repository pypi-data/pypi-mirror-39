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


# ================== CHECK IF HEXADECIMAL ================== #
def is_hex(hexa: str):
    from .Constants import HEXVALUE
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
