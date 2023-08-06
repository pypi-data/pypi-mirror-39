from universalid.settings import Settings


class Encode:

    @staticmethod
    def encode_time(time):
        time_unid = Encode.int_to_str(int(time.timestamp()), 7)
        micro_unid = Encode.int_to_str(time.microsecond, 4)

        return time_unid + micro_unid

    @staticmethod
    def int_to_str(number, width):
        # convert to string
        s = Encode.str_base(number)

        # If number is to big, then return largest possible number
        if len(s) > width:
            return Encode.digit_to_char(Settings.BASE - 1) * width

        # Return the number, padded with zeros
        return ('0' * width + s)[-width:]

    @staticmethod
    def valid_char(c):
        try:
            Encode.str_to_int(c)
        except:
            return False
        return True


    @staticmethod
    def str_to_int(s):
        i = int(s, base=Settings.BASE)
        return i

    @staticmethod
    def digit_to_char(digit):
        # encode a single digit to a char
        if digit < 10:
            return str(digit)
        return chr(ord('a') + digit - 10)

    @staticmethod
    def str_base(number):
        # convert a number to an encoded string
        (d, m) = divmod(abs(number), Settings.BASE)
        if d > 0:
            return Encode.str_base(d) + Encode.digit_to_char(m)
        return Encode.digit_to_char(m)
