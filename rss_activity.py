from datetime import datetime, timedelta
from time import mktime

import feedparser
import warnings

def get_date(obj, attribute_name):
  """Returns a datetime.datetime if the field exists, otherwise returns None.

  Args:
    obj: An object to retrieve the date from.
    attribute_name: The name of the attribute to access."""
  time_struct = getattr(obj, attribute_name, None)
  if time_struct is None:
    return None
  else:
    return datetime.fromtimestamp(mktime(time_struct))


def max_date(a, b):
  """Returns the later datetime.datetime between a and b.

  If both a and b are None, it returns None.
  If only a or b is None, it returns the other.
  Otherwise it returns the later date.

  Args:
    a: The first datetime.datetime to compare.
    b: The second datetime.datetime to compare.
  """
  if a is None:
    return b
  if b is None:
    return a
  return max(a, b)


def get_entry_last_modified(entry):
  """Returns a datetime.datetime for when the entry was last modified.

  If no date is found, returns None.

  This method will look at the pubDate for an item in an RSS feed.

  It does not check the lastBuildDate. That is because it does not appear that
  lastBuildDate is an appropriate field for an item, even though feedparser
  parses it without complaint. The documentation on entries[i].updated is
  unclear,
  https://pythonhosted.org/feedparser/reference-entry-updated.html?highlight=updated
  but it seems compatible with it existing only because there was once a bug
  where that field was created instead of entries[i].published. It does not
  seem to be used in any of the RSS feeds I check and sources such as
  https://validator.w3.org/feed/docs/rss2.html#optionalChannelElements list
  it only as an element at the channel level.

  Args:
    entry: A feedparser.FeedParserDict representing an entry in a RSS feed.
  """
  return get_date(entry, 'published_parsed')


def get_feed_last_modified(feed):
  """Returns a datetime.datetime for when the feed was last modified.

  Returns None if the feed is not parsed correctly, or no valid date is found.

  Unlike the entry level, if the feed does not successfully determine a last
  modified date, it raises a warning.

  Args:
    feed: A URL, file, stream, or string representing a RSS feed. See
      https://pythonhosted.org/feedparser/introduction.html for more details.
  """
  d = feedparser.parse(feed)

  title = getattr(d.feed, 'title', str(feed))

  if d.bozo:
    warnings.warn('There was an error processing "%s": %s' % (
        title, d.bozo_exception))
    return None

  updated = get_date(d.feed, 'updated_parsed')
  published = get_date(d.feed, 'published_parsed')
  modified = get_date(d, 'modified_parsed')

  feed_last_modified = max_date(max_date(updated, published), modified)

  for entry in d.entries:
    entry_last_modified = get_entry_last_modified(entry)
    feed_last_modified = max_date(feed_last_modified, entry_last_modified)

  if feed_last_modified is None:
    warnings.warn('No date found for "%s"!' % title)
  return feed_last_modified
