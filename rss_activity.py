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
