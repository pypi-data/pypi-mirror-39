# TODO: replace concatenations with string ''.join()s of lists.
# TODO: input validation? Validate input in bin scripts.


def build_roman_digit(digit, exponent=0):
    romanchars = [('I', 'V'), ('X', 'L'), ('C', 'D'), ('M', ''), ('', '')]
    # Using a dict here instead should allow using the same code below even if a
    # more exotic system with more symbols than 1&5 or non-decimal bases is used.
    # This would also make the code neater with rc[exp][digit] style where we
    # don't need to worry about whether the 1 & 5 symbols are the 0 and 1 indices.
    rc = romanchars
    e = exponent

    if digit == 0:
        return ''
    elif digit < 4:
        return digit * rc[e][0]
    elif digit == 4:
        if e == 3:
            return digit * rc[e][0]  # Special case for 4000 MMMM, since no symbol for 5000 exists.
        else:
            return rc[e][0] + rc[e][1]
    elif digit < 9:
        return rc[e][1] + (digit - 5) * rc[e][0]
    else:  # digit == 9 (or more, if input is bad)
        return rc[e][0] + rc[e + 1][0]


def smallnum2r(num):
    # Validate input: Don't; let n2r/scripts handle this.
    # Get thousands/hundreds/tens/one digits: obvious math method
    th = num / 1000
    hu = (num - th * 1000) / 100
    te = (num - th * 1000 - hu * 100) / 10
    on = num - th * 1000 - hu * 100 - te * 10
    # Alt: loop through % 10 and //= 10 on every loop
    # Alt: with string input: loop through string chars after trimming/cleaning.

    retstr = ""

    for digit, exponent in zip([th, hu, te, on], [3, 2, 1, 0]):
        retstr += build_roman_digit(digit, exponent)
    return retstr


def n2r(num):
    sign_prefix = ""
    if num < 0:
        sign_prefix = "-"
        num = abs(num)  # Conversion here will cause the - prefix to appear only at first level.

    if num == 0:
        return "nulla"  # Can't think of a better way here.
    elif num < 5000:
        return sign_prefix + smallnum2r(num)
    else:
        aux = num % 5000
        return sign_prefix + "(" + n2r((num - aux) / 1000) + ")" + smallnum2r(aux)
