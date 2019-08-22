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
