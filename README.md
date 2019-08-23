# RSS-Inactive-Companies
Python program using feedparser library to find companies that have not had any activity on their RSS feeds for a given period of time. Uses Python 3.7.3, [feedparser](https://pypi.org/project/feedparser/).

## Change to function input/output
There is a tension between receiving a dictionary where the key is a company and the value is a single RSS feed and companies having multiple RSS feeds. I resolved this by instead taking in a dictionary where the key is a company and the value is a list of RSS feeds.

## General approach to errors/warnings
Since RSS feeds do not conform very tightly to the same standards, for the program to be reasonably useful it should not raise exceptions that stop the program, and should only give warnings when a relatively large scale entity cannot be parsed correctly. Currently, it only gives warnings if it was unable to determine a last modification date for either an entire feed or an entire company.

Another design decision was to not take shortcuts. For example, if the first item in the first feed of a company was recent enough we already know that the company will not be included in the output of get_inactive_companies. But instead of skipping the remaining items and feeds, the program continues to check the others. The main reason is for simplicity. It makes testing a bit more subtle if it is possible to unintentially skip edges cases. For instance, in my example, if the second feed was not a valid link, that error would be missed if the shortcut is taken. That being said, it would be quite straightforward to restructure the program so that it did take shortcuts. The easiest way would be to change the get last modified functions to instead return whether that entity had been active in the last min_active_days days.

### Other noteworthy edge cases/omissions
1. RSS feeds with unreasonable dates. RSS 0.9 was released in March 1999 ([source](https://en.wikipedia.org/wiki/History_of_web_syndication_technology)), so any RSS feed from before 1999 would be suspicious. Additionally, any feed from the future would raise eyebrows. I think these are each handled reasonably by without special treatment. Very old dates can only be impactful if the user is interested in feeds that have been inactive since before 1999, and feeds from the future could potentially be things like rounding to the next day, which shouldn't disqualify a feed.

2. No dates/Empty feed/Empty company. All of these are treated as though they empty entities don't exist, except for companies with no provided feeds. For instance, if an entry has no date, it is considered to inactive, which is the same as if it hadn't existed at all. For a company though, if it has no feeds, meaning that there was no activity, it is included in the output. This behavior could easily be changed by requiring finding at least one valid date in one of the company's feeds.

3. Fields such as expiration dates (RSS 0.93 ([source](https://pythonhosted.org/feedparser/reference-entry-expired.html#reference-entry-expired)) and lastBuildDate for items are ignored. There is some discussion about lastBuildDate in the docstring for get_entity_last_modified, and I think it is a reasonable interpretation that something expiring does not count as activity.

4. d.feed.modified uses the last-modified field of the HTTP header ([source](https://pythonhosted.org/feedparser/http-etag.html)), which is arguably not in the RSS, and is not something that I tested, but I did allow the get_feed_last_modified to check it.

5. For the boundary of k days, I took the interpretation that 2 days means 48 hours, as opposed to any rounding to based on date boundaries.

6. None of the unit tests check formats of RSS other than 2.0, but the parser presents the same abstraction for each of them, and it is capable of handling all of them. I figured it was overkill to dive any deeper into the differences between the different versions.

7. I didn't do extensive input sanitization since feedparser is quite robust and able to handle many inputs, and it seemed reasonable to simply defer to the bozo bit ([source](https://pythonhosted.org/feedparser/bozo.html)) it used for whether a feed was a valid input.

8. Related, feedparser can sometimes partially parse malformed RSS feeds. Instead of retrieving dates from partially malformed feeds, if the parser thought the feed was malformed, the program gives up on the feed and returns that it was unable to find a valid date.

9. Any other edge cases that feedparser is not able to handle. For instance it can handle many, but not all concievable date formats.
