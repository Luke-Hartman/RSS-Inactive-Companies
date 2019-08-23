from datetime import datetime, timedelta
from time import mktime

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
