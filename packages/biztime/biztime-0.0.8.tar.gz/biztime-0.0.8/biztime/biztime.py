import datetime as dt


def create_date_range(start, end):
  """Returns a list of date objects spanning from the start to end inputs."""
  date_range = [start]
  if start == end:
    return date_range

  range_size = (end - start).days

  last_date = start
  while last_date < end:
    next_date = last_date + dt.timedelta(days=1)
    date_range.append(next_date)
    last_date = next_date

  return date_range

def convert_timedelta(td, unit):
  """Convert timestamp object to int in specified units."""
  td_s = (td.days * 3600 * 24) + td.seconds
  if unit == 's': return td_s
  if unit == 'm': return div_round(td_s, 60)
  if unit == 'h': return div_round(td_s, 3600)
  raise ValueError('unit not recognized: %s' % unit)

def dt_to_date(dt_in):
  """Returns a date object from a datetime object."""
  return dt.date(dt_in.year, dt_in.month, dt_in.day)

def dt_to_time(dt_in):
  """Returns a date object from a datetime object."""
  return dt.time(dt_in.hour, dt_in.minute, dt_in.second)

def start_of_day(date=None):
  """Returns a time or datetime object of 00:00:00am on the input date."""
  if not date:
    return dt.time(0)
  return dt.datetime.combine(date, dt.time(0))

def end_of_day(date=None):
  """Returns a time or datetime object of 11:59:59pm on the input date."""
  if not date:
    return dt.time(23, 59, 59)
  return dt.datetime.combine(date, dt.time(23, 59, 59))

def div_round(dividend, divisor):
  """Divides two ints with proper rounding."""
  return (dividend + divisor // 2) // divisor


class BizTime:

  def __init__(self, conf):
    # Default business hours configuration.
    self.biz_start = dt.time(9, 0)
    self.biz_end = dt.time(17, 0)
    self.weekend = []
    self.holidays = []

    if 'biz_start' in conf:
      self.biz_start = conf['biz_start']
    if 'biz_end' in conf:
      self.biz_end = conf['biz_end']
    if 'weekend' in conf:
      self.weekend = conf['weekend']
    if 'holidays' in conf:
      self.holidays = conf['holidays']

    self.full_day = self.time_diff(self.biz_start, self.biz_end)

  def time_diff(self, start, end):
    """Returns a timedelta between two times minus non-biz hours."""
    # Validate input.
    if not isinstance(start, dt.time) or not isinstance(start, dt.time):
      raise TypeError('Both inputs must be a datetime.time object.')
    if end < start:
      raise ValueError(
          'The end time must be equal to or later than the start time.')

    # Convert time objects to datetime objects to allow timedelta calcs.
    dummy_date = dt.date(1970, 1, 1)
    start_ = dt.datetime.combine(dummy_date, start)
    end_ = dt.datetime.combine(dummy_date, end)
    biz_start_ = dt.datetime.combine(dummy_date, self.biz_start)
    biz_end_ = dt.datetime.combine(dummy_date, self.biz_end)

    if start_ > biz_end_ or end_ < biz_start_ or start_ == end_:
      return dt.timedelta(0)
    if start_ < biz_start_:
      start_ = biz_start_
    if end_ > biz_end_:
      end_ = biz_end_

    return end_ - start_

  def date_diff(self, start, end):
    """Returns timedelta between two dates minus non-biz hours/days."""
    # Validate input.
    if not isinstance(start, dt.datetime) or not isinstance(start, dt.datetime):
      raise TypeError('Both inputs must be a datetime.datetime object.')
    if end < start:
      raise ValueError(
          'The end date must be equal to or later than the start date.')

    biz_time = dt.timedelta(0)

    # If start and end times are on same day, immediately calculate and return.
    if dt_to_date(start) == dt_to_date(end):
      return self.time_diff(dt_to_time(start), dt_to_time(end))


    # Get biz hours from partial days at beginning and end of inuput range.
    if self.is_biz_day(dt_to_date(start)):
      biz_time += self.time_diff(dt_to_time(start), end_of_day())
    if self.is_biz_day(dt_to_date(end)):
      biz_time += self.time_diff(start_of_day(), dt_to_time(end))

    date_range_start = dt_to_date(start) + dt.timedelta(days=1)
    date_range_end = dt_to_date(end) - dt.timedelta(days=1)
    if date_range_start > date_range_end:
      return biz_time

    # Get working hours from full days between start and end dates. Omit
    # weekends and holidays.
    date_range = create_date_range(date_range_start, date_range_end)
    for date in date_range:
      if self.is_biz_day(dt_to_date(date)):
        biz_time += self.full_day

    return biz_time

  def is_biz_day(self, date):
    return (date.weekday() not in self.weekend and date not in self.holidays)
