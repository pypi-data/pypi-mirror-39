class Settings:
    # Max values with base 36
    #   1 digit:    35
    #   2 digits:   1.295
    #   3 digits:   46.655
    #   4 digits:   1.679.615
    #   5 digits:   60.466.175
    #   6 digits:   2.176.782.335

    BASE = 36  # (a-z + 10)

    CUSTOM_LENGTH = 20
    SEQUENCE_LENGTH = 1
    DATETIME_LENGTH = 11  # total length of the datetime part, incl. the microseconds
    TOTAL_LENGTH = CUSTOM_LENGTH + DATETIME_LENGTH + SEQUENCE_LENGTH  # total length of unid to generate
