from datetime import date as Date
from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta
import re

today = Date.today

def absolute_date(info):
    if isinstance(info, Date):
        return info
    elif isinstance(info, tuple):
        return Date(*info)
    elif isinstance(info, str):
        return DateTime.strptime(info, '%Y-%m-%d').date()
    else:
        raise RuntimeError("Invalid date %s" % info)

def date_for(time_info):
    if isinstance(time_info, str):
        if time_info == 'tomorrow': return today() + TimeDelta(1)
        if time_info == 'today': return today()
        days_match = re.match('^(\d+)\s+days?$', time_info)
        if days_match:
            days = int(days_match.group(1))
            return today() + TimeDelta(days)
        d_match = re.match('^(\d+)d$', time_info)
        if d_match:
            days = int(d_match.group(1))
            return today() + TimeDelta(days)
    return absolute_date(time_info)
