import math


class Clock:

    #######
    # O(1) - constant
    # creates a clock object (used to keep/calculate HH:MM time values)
    def __init__(self, time='8:00', period='AM'):
        self.hours = int(time[0:time.index(':')])
        self.minutes = int(time[time.index(':') + 1:])
        self.period = period.upper()

    #######
    # O(1) - constant
    # increment the time value by minutes.
    def add_minutes(self, minutes):
        new_minutes = math.ceil(minutes) + self.minutes
        if new_minutes >= 60:
            self.add_hours(int(new_minutes / 60))
            self.minutes = new_minutes % 60
        else:
            self.minutes = new_minutes

    #######
    # O(1) - constant
    # decrement the time value by minutes
    def subtract_minutes(self, minutes):
        new_minutes = self.minutes - math.ceil(minutes)
        if new_minutes < 0:
            self.hours -= 1 if self.hours != 1 else 12
            self.minutes = 60 + new_minutes
        else:
            self.minutes = new_minutes

    #######
    # O(1) - constant
    # increment the time value by hours
    def add_hours(self, hours):
        new_hours = math.ceil(hours) + self.hours
        if new_hours > 11:
            if new_hours > 12:
                self.hours = new_hours % 12
            else:
                self.period = 'PM' if self.period == 'AM' else 'AM'
                self.hours = new_hours
        else:
            self.hours = new_hours

    #######
    # O(1) - constant
    # used to print a formatted time stamp i.e. 8:00 AM
    def time_string(self):
        return '{hours}:{minutes} {period}' \
            .format(hours=self.hours,
                    minutes=self.minutes
                    if self.minutes >= 10
                    else '0{minutes}'.format(minutes=self.minutes),
                    period=self.period)

    #######
    # O(1) - constant
    # checks if current time is within threshold of a specified deadline (defaults to 60 minutes)
    def is_approaching_deadline(self, deadline, time_frame=60):
        time = deadline[0: deadline.index(' ')]
        period = deadline[deadline.index(' ')+1:]
        deadline_clock = Clock(time, period)
        deadline_clock.subtract_minutes(time_frame)

        if self.greater_than(deadline_clock):
            return True
        return False

    #######
    # O(1) - constant
    # convert object into an integer for comparison operations i.e 9:34 -> 934
    def int_time(self):
        return self.hours * 100 + self.minutes + (1200 if self.period == 'PM' and self.hours != 12 else 0)

    #######
    # O(1) - constant
    # compare times to see if one time is greater(after) the other
    def greater_than(self, clock):
        return self.int_time() > clock.int_time()
