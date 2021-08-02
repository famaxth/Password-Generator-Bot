# - *- coding: utf- 8 - *-

import random
import builtins


def create_password(length, special_symbol, big_symbol, numbers, small_symbol):
    chars = ""
    number = 1
    length = int(length)
    if special_symbol == True:
        special_symbol = "%*)?@#$~"
        chars_1 = chars + special_symbol
    else:
        chars_1 = chars + ""
    if big_symbol == True:
        big_symbol = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars_2 = chars_1 + big_symbol
    else:
        chars_2 = chars_1 + ""
    if numbers == True:
        numbers = "1234567890"
        chars_3 = chars_2 + numbers
    else:
        chars_3 = chars_2 + ""
    if small_symbol == True:
        small_symbol = "abcdefghijklnopqrstuvwxyz"
        chars_4 = chars_3 + small_symbol
    else:
        chars_4 = chars_3 + ""
    for n in range(number):
        password = ""
        for i in range(length):
            password += random.choice(chars_4)
        return password
