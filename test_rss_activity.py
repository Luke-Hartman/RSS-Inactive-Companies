from datetime import datetime

import rss_activity
import time
import unittest


class TestGetDate(unittest.TestCase):

    def test_get_date(self):
        class DummyObject():
          def __init__(self, attribute, value):
            setattr(self, attribute, value)

        obj = DummyObject('epoch', time.gmtime(0))
        actual = rss_activity.get_date(obj, 'epoch')
        expected = datetime(1970, 1, 1, 0, 0)
        self.assertEquals(actual, expected)

    def test_get_date_missing_attribute(self):
        class DummyObject():
            pass

        obj = DummyObject()
        actual = rss_activity.get_date(obj, 'epoch')
        expected = None
        self.assertEquals(actual, expected)

class TestMaxDate(unittest.TestCase):

    def test_max_date(self):
        earlier_date = datetime(1970, 1, 1, 0, 0)
        later_date = datetime(1971, 1, 1, 0, 0)

        actual = rss_activity.max_date(earlier_date, later_date)
        expected = later_date
        self.assertEquals(actual, expected)

    def test_max_date_one_missing(self):
        missing_date = None
        present_date = datetime(1970, 1, 1, 0, 0)

        # Test first date missing
        actual = rss_activity.max_date(missing_date, present_date)
        expected = present_date
        self.assertEquals(actual, expected)

        # Test second date missing
        actual = rss_activity.max_date(present_date, missing_date)
        expected = present_date
        self.assertEquals(actual, expected)

    def test_max_date_both_missing(self):
        actual = rss_activity.max_date(None, None)
        expected = None
        self.assertEquals(actual, expected)

if __name__ == '__main__':
    unittest.main()
