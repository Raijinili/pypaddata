#!/usr/bin/env python3
import json
from padutil import output_table
import limited_bonus_data
from limited_bonus_data import Bonus
import dungeon_data

def tolist(self):
    # lst = list(map(lambda dt: dt.strftime('%Y%m%d_%H:%M:%S'), (self.s, self.e)))
    # lst = list(map(DT.isoformat, (self.s, self.e)))
    duration = self.e - self.s
    lst = [self.s.strftime('%Y%m%d_%H:%M:%S'), duration_to_string(duration)]
    for k in Bonus.keys[2:]:
        if hasattr(self, k):
            lst.append(getattr(self, k))
        else:
            lst.append('')
        
    return lst



def show_timediff(start, end):
    """Given start and end time, show the differences.
    
    E.g.
        - If start and end are in the same Time, but different Date, show the new date.
        + Date:
            - If same month, but different day, show the day.
            - If different month, show both month and day.
        + Time:
            - If different hour, show hours.
                ! Coin dungeon bonuses are an hour longer than event.
    """



def duration_to_string(duration):
    """Output a timedelta in a useful format.
    """
    days = duration.days
    seconds = duration.seconds
    assert not duration.microseconds
    # assert bool(days) == (not seconds)
    # if bool(days) != (not seconds):
        # days, seconds = 0, days*24*60*60 + seconds
    hours, seconds = divmod(seconds, 60*60)
    #assert seconds == 0
    s = ''
    s += "%4dD" % days if days else ' '*5
    s += "%4dH" % hours if hours else ' '*5
    return s
    # if days:
        # return "%4dD" % days
    # else:
        # hours, seconds = divmod(seconds, 60*60)
        # assert seconds == 0
        # return "%4dH" % hours


def main():
    try:
        import sys
        try:
            fname = sys.argv[1]
        except IndexError:
            fname = 'bonus.in'
        with open(fname) as f:
            j = json.load(f)
        data = j['bonuses']
        
        limited_bonus_data.dungeons = dungeon_data.load()
        
        output_table(map(tolist, map(Bonus, data)), fpath='bonus.out')
    except:
        import atexit
        atexit.register(input, 'Press Enter to continue...')
        raise



if __name__ == '__main__':
    main()
