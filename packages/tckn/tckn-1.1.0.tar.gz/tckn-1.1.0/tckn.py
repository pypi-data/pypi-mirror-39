import random
import string


def generate() -> str:
    """Generate a random valid identity number."""
    digits = range(10)
    first_digit = random.randint(1, 9)  # Must be nonzero
    first_9_digits = [first_digit] + random.choices(digits, k=8)
    first_part = ''.join(str(d) for d in first_9_digits)
    return first_part + last_2_digits(first_part)


def validate(number: str) -> bool:
    """Check if a string is a valid identity number or not."""
    if len(number) != 11:
        return False
    if number[0] == '0':
        return False
    if not all(d in string.digits for d in number):
        return False
    digits = [int(d) for d in number]
    if digits[9] != (sum(digits[:9:2])*7 - sum(digits[1:9:2])) % 10:
        return False
    if digits[10] != sum(digits[:10]) % 10:
        return False
    return True


def last_2_digits(number: str) -> str:
    """Generate last 2 digits for first 9 digits of an identity number."""
    if len(number) != 9:
        raise ValueError('The number should have 9 digits')
    if not all(d in string.digits for d in number):
        raise ValueError('The characters must be all digits')
    first_digits = [int(d) for d in number]
    digit_10 = (sum(first_digits[::2])*7 - sum(first_digits[1::2])) % 10
    first_10_digits = first_digits + [digit_10]
    digit_11 = sum(first_10_digits) % 10
    return str(digit_10) + str(digit_11)
