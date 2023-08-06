from datetime import datetime
from secrets import randbelow
from universalid.settings import Settings
from universalid.encode import Encode


# UNID format, default length = 32:
# * Position 1-20: Custom - defaults to a random (20 digits)
# * Position 21-27: Date/time (7 digits)
# * Position 28-31: microseconds (4 digits)
# * Position 32: sequence (1 digig)

class Unid:
    time_sequence = 0  # Add a sequence number to make the datetime part unique when Unid's is created simultaneously

    @staticmethod
    def create(time=None, prefix=None):
        time = time if time else datetime.utcnow()
        prefix = Unid._strip(prefix) if prefix else ""

        # start with the optional prefix (limited to the max length)
        unid = prefix[:Settings.CUSTOM_LENGTH]

        # add random chars
        size = Settings.CUSTOM_LENGTH - len(prefix)
        unid += Unid._get_random(size)

        # add the datetime
        unid += Encode.encode_time(time)

        # add the sequence
        unid += Encode.digit_to_char(Unid._inc_sequence())

        return unid.upper()

    @staticmethod
    def get_time(unid):
        # decode the datetime
        date_str = unid[-12:-5]

        timestamp = Encode.str_to_int(date_str)
        date = datetime.fromtimestamp(timestamp)

        # decode the microseconds
        micro_str = unid[-5:-1]
        microsecond = Encode.str_to_int(micro_str)

        # return
        date = date.replace(microsecond=microsecond)
        return date

    @staticmethod
    def _inc_sequence():
        result = Unid.time_sequence
        Unid.time_sequence += 1
        if Unid.time_sequence == Settings.BASE:
            Unid.time_sequence = 0
        return result

    @staticmethod
    def _get_random(length):
        s = ""
        while len(s) < length:
            r = randbelow(Settings.BASE)
            s += Encode.digit_to_char(r)
        return s

    @staticmethod
    def _strip(value):
        result = ""
        for c in value:
            result += c if Encode.valid_char(c) else ''
        return result
