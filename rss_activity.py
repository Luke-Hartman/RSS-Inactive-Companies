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


def get_company_last_modified(feeds, company='(untitled)'):
  """Returns a datetime.datetime for when the company was last modified.

  If no valid date is found, returns None.

  Similar to get_feed_last_modified, this raises a warning if it is unable to
  determine a last modified date.

  Args:
    feeds: A list of URLs, files, streams, or strings representing RSS feeds.
      See https://pythonhosted.org/feedparser/introduction.html for more
      details.
    company: An optional representation of a company, used for warning when a
      date is unable to be determined.
  """
  company_last_modified = None
  for feed in feeds:
    feed_last_modified = get_feed_last_modified(feed)
    company_last_modified = max_date(company_last_modified, feed_last_modified)
  if company_last_modified is None:
    warnings.warn('No date found for "%s"!' % company)
  return company_last_modified


def get_inactive_companies(company_to_feeds, min_days_inactive):
  """Returns a list of all companies that have been inactive for a given number.

  If a date is not able to be determined for a company, it is considered to have
  been inactive for long enough.

  Args:
    company_to_feeds: A dictionary from an object representing a company to a
      list of RSS feeds. The RSS feeds can be represented as a list of URLs,
      files, streams or strings. See
      https://pythonhosted.org/feedparser/introduction.html for more details.
    min_days_inactive: The minimum number of days since the latest activity on
      any of the given feeds for a company to be included in the output. It does
      not have to be an integer number of days. For instance, 1.5 would mean any
      companies with no activity in the last 36 hours.
  """
  latest_activity_threshold = datetime.now() - timedelta(days=min_days_inactive)

  inactive_companies = []
  for company, feeds in company_to_feeds.items():
    last_modified = get_company_last_modified(feeds, company)
    if last_modified is None or last_modified <= latest_activity_threshold:
      inactive_companies.append(company)
  return inactive_companies
