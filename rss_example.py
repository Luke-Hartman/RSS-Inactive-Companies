import rss_activity

company_to_feeds = {
  'Joe Rogan': ['http://podcasts.joerogan.net/feed'],
  'NY Times': ['https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'],
  'NPR': ['https://www.npr.org/rss/podcast.php?id=510289'],
  'Hacker News': ['https://hnrss.org/frontpage', 'https://hnrss.org/jobs'],
  'Bill Maher': ['http://billmaher.hbo.libsynpro.com/rss'],
  'ESPN': ['https://www.espn.com/espn/rss/nfl/news',
           'https://www.espn.com/espn/rss/nba/news',
           'https://www.espn.com/espn/rss/mlb/news']
}

for min_days_inactive in [1/24, 1, 2, 7]:
  inactive_companies = rss_activity.get_inactive_companies(
      company_to_feeds, min_days_inactive)
  print("Companies that have not been active in the last %f days: %s" % (
      min_days_inactive, inactive_companies))
