from datetime import datetime

import feedparser
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
    self.assertEqual(actual, expected)

  def test_get_date_missing_attribute(self):
    class DummyObject():
      pass

    obj = DummyObject()
    actual = rss_activity.get_date(obj, 'epoch')
    expected = None
    self.assertEqual(actual, expected)


class TestMaxDate(unittest.TestCase):

  def test_max_date(self):
    earlier_date = datetime(1970, 1, 1, 0, 0)
    later_date = datetime(1971, 1, 1, 0, 0)

    actual = rss_activity.max_date(earlier_date, later_date)
    expected = later_date
    self.assertEqual(actual, expected)

  def test_max_date_one_missing(self):
    missing_date = None
    present_date = datetime(1970, 1, 1, 0, 0)

    # Test first date missing
    actual = rss_activity.max_date(missing_date, present_date)
    expected = present_date
    self.assertEqual(actual, expected)

    # Test second date missing
    actual = rss_activity.max_date(present_date, missing_date)
    expected = present_date
    self.assertEqual(actual, expected)

  def test_max_date_both_missing(self):
    actual = rss_activity.max_date(None, None)
    expected = None
    self.assertEqual(actual, expected)


class TestGetEntryLastModified(unittest.TestCase):

  def test_get_entry_last_modified(self):
    feed = """
    <rss version="2.0">
      <channel>
        <title>My Feed</title>
      </channel>
      <item>
        <title>Item 1</title>
        <pubDate>Thu, 1 Jan 1970</pubDate>
      </item>
    </rss>
    """
    d = feedparser.parse(feed)
    entry = d.entries[0]
    actual = rss_activity.get_entry_last_modified(entry)
    expected = datetime(1970, 1, 1, 0, 0)
    self.assertEqual(actual, expected)

  def test_get_entry_last_modified_missing_date(self):
    feed = """
    <rss version="2.0">
      <channel>
        <title>My Feed</title>
      </channel>
      <item>
        <title>Item 1</title>
      </item>
    </rss>
    """
    d = feedparser.parse(feed)
    entry = d.entries[0]
    actual = rss_activity.get_entry_last_modified(entry)
    expected = None
    self.assertEqual(actual, expected)

  def test_get_entry_last_modified_multiple_entries(self):
    feed = """
    <rss version="2.0">
      <channel>
        <title>My Feed</title>
      </channel>
      <item>
        <title>Item 1</title>
      </item>
      <item>
        <title>Item 2</title>
        <pubDate>Fri, 2 Jan 1970</pubDate>
      </item>
      <item>
        <title>Item 3</title>
      </item>
      <item>
        <title>Item 4</title>
        <pubDate>Thu, 1 Jan 1970</pubDate>
      </item>
    </rss>
    """
    d = feedparser.parse(feed)
    actual = [rss_activity.get_entry_last_modified(entry)
              for entry in d.entries]
    expected = [
        None,
        datetime(1970, 1, 2, 0, 0),
        None,
        datetime(1970, 1, 1, 0, 0)]
    self.assertCountEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
