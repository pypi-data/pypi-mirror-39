# biztime

`biztime` is a is a utility for calculating the total time between given
dates/times, while omitting non-working hours, weekends, and holidays as
configured by the user. Includes additional helper functions for interacting
with various `datetime` objects.

## Installation

Install and update using [pip](https://pypi.org/project/biztime):

`pip install biztime`

## Usage Example

```python
>>> import biztime
>>> from datetime import date, datetime, time, timedelta
>>> bt = biztime.BizTime({
...   'biz_start': time(9, 0, 0),
...   'biz_end': time(17, 0, 0),
...   'weekend': [5, 6],
...   'holidays': [date(2018, 12, 24), date(2018, 12, 25)],
... })
>>> bt.time_diff(time(13, 0, 0), time(18, 0, 0))
datetime.timedelta(0, 14400)
>>> bt.date_diff(datetime(2018, 12, 9, 8, 0, 0), datetime(2018, 12, 15, 8, 0, 0))
datetime.timedelta(1, 57600)
>>> time_delta = bt.date_diff(datetime(2018, 12, 9, 8, 0, 0), datetime(2018, 12, 15, 8, 0, 0))
>>> biztime.convert_timedelta(time_delta, 'h')
40
>>> xmas_week = bt.date_diff(datetime(2018, 12, 23, 8, 0, 0), datetime(2018, 12, 29, 8, 0, 0))
>>> biztime.convert_timedelta(xmas_week, 'h')
24
>>> bt.is_biz_day(date(2018, 12, 25))
False
```

## Reference

### BizTime Class

<pre>
<b>BizTime</b>(<i>conf</i>)
	Accepts a configuration dict to modify start/end times, weekends, and
	holidays.
	&nbsp;
	Default values:
		'biz_start' - datetime.time(9, 0, 0)   # 9am
		'biz_end'   - datetime.time(17, 0, 0)  # 5pm
		'weekend'   - [5, 6]                   # Sat, Sun
		'holidays'  - []                       # None
	&nbsp;
	Arg Types:
		conf - dictionary
	&nbsp;
BizTime<b>.time_diff</b>(<i>start, end</i>)
	Returns a datetime.timedelta object representing the number of working hours
	between the start and end time.
	&nbsp;
	Arg Types:
		start - datetime.time
		end   - datetime.time
	&nbsp;
BizTime<b>.date_diff</b>(<i>start, end</i>)
	Returns a datetime.timedelta object representing the number of working hours
	between the start and end time, having omitted weekends and holidays.
	&nbsp;
	Arg Types:
		start - datetime.datetime
		end   - datetime.datetime
	&nbsp;
BizTime<b>.is_biz_day</b>(<i>date</i>)
	Returns a bool indicating whether the given date is a weekend or holiday per
	the users' config.
	&nbsp;
	Arg Types:
		date - datetime.date
	&nbsp;
</pre>

### Helper Functions

<pre>
<b>create_date_range</b>(<i>start, stop</i>)
	Returns a list of datetime.date objects for all dates between the given start
	and end dates (inclusive).
	&nbsp;
	Arg Types:
		start - datetime.date
		end   - datetime.date
	&nbsp;
<b>convert_timedelta</b>(<i>td, unit</i>)
	Returns an int value representation of the given timedelta in the specified
	units.
	&nbsp;
	Arg Types:
		td   - datetime.timedelta
		unit - string ('s', 'm', or 'h')
	&nbsp;
<b>dt_to_date</b>(<i>dt_in</i>)
	Returns a datetime.date object from a given datetime object.
	&nbsp;
	Arg Types:
		dt_in - datetime.datetime
	&nbsp;
<b>dt_to_time</b>(<i>dt_in</i>)
	Returns a datetime.time object from a given datetime object.
	&nbsp;
	Arg Types:
		dt_in - datetime.datetime
	&nbsp;
<b>start_of_day</b>(<i>date=None</i>)
	Returns a a datetime.time object representing 12:00:00am. Returns full
	datetime.datetime object if a date is passed to it.
	&nbsp;
	Arg Types:
		date - datetime.date
	&nbsp;
<b>end_of_day</b>(<i>date=None</i>)
	Returns a a datetime.time object representing 11:59:59pm. Returns full
	datetime.datetime object if a date is passed to it.
	&nbsp;
	Arg Types:
		date - datetime.date
	&nbsp;
<b>div_round</b>(<i>dividend, divisor</i>)
	Divides two ints with proper rounding.
	&nbsp;
	Arg Types:
		dividend - integer
		divisor  - integer
	&nbsp;
</pre>
