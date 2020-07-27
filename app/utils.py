import hashlib
from typing import Union


def dict_values_concatenator(
        data: dict,
        required_keys: list,
        separator=':') -> str:
    """ Returns data values by required_keys as concatenated string """

    required_values = [str(data[key]) for key in required_keys]
    data_concatenated = separator.join(required_values)
    return data_concatenated


def generate_sign(sign_source_string: str) -> str:
    """
    Generates SHA-256 hash-sign by sign_source_string
    might be checked at: https://xorbin.com/tools/sha256-hash-calculator
    """

    hash_sign = hashlib.sha256(str.encode(sign_source_string)).hexdigest()
    return hash_sign


def get_currency_code(currency: str) -> Union[str, None]:
    """
    Returns currency numeric code according to ACCESS ISO 4217:2015
    Args:
     - currency (str) 3-letters aphabetic code
    Returns:
     - numeric (str) 3-digits numeric code
    More details about the standard:
    https://www.iso.org/iso-4217-currency-codes.html
    IMPORTANT! The converter contains incomplete data!
    i.e. it convets NOT ALL currencies mentioned at ISO 4217:2015)
    """

    alphabetic_numeric = {
        'EUR': '978',
        'USD': '840',
        'RUB': '643',
    }
    numeric = alphabetic_numeric.get(currency.upper())
    return numeric
