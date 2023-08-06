import unittest
from universalid.universalid import Unid
import datetime
from universalid.settings import Settings
from universalid.encode import Encode

class TestUniversalID(unittest.TestCase):
    max_time = datetime.datetime(2999, 12, 31, 23, 59, 59, 9998, tzinfo=None)
    min_time = datetime.datetime(1971, 1, 1, 0, 0, 0, 0, tzinfo=None)

    def test_int_to_string(self):
        self.assertEqual(Encode.int_to_str(35, 3), '00z')
        self.assertEqual(Encode.int_to_str(0, 3), '000')
        self.assertEqual(Encode.int_to_str(999, 3), '0rr')
        self.assertEqual(Encode.int_to_str(100, 3), '02s')
        self.assertEqual(Encode.int_to_str(-100, 3), '02s')  # only absolute values.
        self.assertEqual(Encode.int_to_str(99999, 3), 'zzz')  # out of range, return largest possible

    def test_string_to_int(self):
        self.assertEqual(Encode.str_to_int('z'), 35)
        self.assertEqual(Encode.str_to_int('0000z'), 35)
        self.assertEqual(Encode.str_to_int('zzz'), 46655)

    def test_encode_time(self):
        self.assertEqual(Encode.encode_time(TestUniversalID.max_time), "exjul7z07pq")
        self.assertEqual(Encode.encode_time(TestUniversalID.min_time), "00iruk00000")

    def test_timestamp(self):
        t_max = TestUniversalID.max_time.timestamp()
        d_max = datetime.datetime.fromtimestamp(t_max)
        self.assertEqual(TestUniversalID.max_time, d_max)

        t_min = TestUniversalID.min_time.timestamp()
        d_min = datetime.datetime.fromtimestamp(t_min)
        self.assertEqual(TestUniversalID.min_time, d_min)

    def test_get_time(self):
        self.assertEqual(Unid.get_time("ZZZZexjul7z07pq0"), TestUniversalID.max_time)
        self.assertEqual(Unid.get_time("00iruk000000"), TestUniversalID.min_time)

        now = datetime.datetime.utcnow()
        unid = Unid.create(now)
        self.assertEqual(now, Unid.get_time(unid))

    def test_create(self):
        self.assertEqual(len(Unid.create()), Settings.TOTAL_LENGTH)
        self.assertEqual(len(Unid.create(prefix='XX')), Settings.TOTAL_LENGTH)
        self.assertEqual(Unid.create(prefix='XX')[0:2], 'XX')
        self.assertNotEqual(Unid.create(), Unid.create())

    def test_create_prefix(self):
        t = datetime.datetime.now()
        unid = Unid.create(t, prefix="ThisPrefixIsLongerThan20Characters")
        self.assertEqual(len(unid), Settings.TOTAL_LENGTH)
        self.assertEqual(Unid.get_time(unid), t)

        unid = Unid.create(prefix="Illegal Æ_./? Chars")
        self.assertEqual(unid[:12], "ILLEGALCHARS")


if __name__ == '__main__':
    unittest.main()
