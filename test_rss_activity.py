from datetime import datetime

import rss_activity
import time
import unittest


class TestRssActivity(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
