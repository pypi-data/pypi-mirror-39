import datetime
import CoroCron
import asyncio
from collections import Iterable

class Job():
    def __init__(self, cron = None):
        self.cron = None
        if cron is not None:
            if not isinstance(cron, CoroCron.Cron):
                TypeError("cron must be a CoroCron.Cron object")
            self.cron = cron

        self.__set = False

        self.__monthly = False
        self.__daily = False
        self.__weekly = False
        self.__hourly = False
        self.__minutely = False
                
        self.__months = None
        self.__days = None
        self.__weekdays = None
        self.__hours = None
        self.__minutes = None

        self.__function = None
        self.__args = None
        

    def Months(self, months = None):
        if self.__monthly:
            ValueError("Can only have 1 Months schedule set")     
        self.__monthly = True
        self.__set = True
        self.__months = self.__ensure_iterable(months)
        return self

    def Days(self, days = None):
        if self.__weekly:
            ValueError("Can only choose Days or Weekdays, not both")
        if self.__daily:
            ValueError("Can only have 1 Days schedule set")
        self.__daily = True
        self.__set = True
        self.__days = self.__ensure_iterable(days)
        return self

    def Weekdays(self, days_of_week=None):
        if self.__daily:
            ValueError("Can only choose Days or Weekdays, not both")
        if self.__weekly:
            ValueError("Can only have 1 Weekdays schedule set")
        self.__weekly = True
        self.__set = True
        self.__weekdays = self.__ensure_iterable(days_of_week)
        return self

    def Hours(self, hours=None):
        if self.__hourly:
            ValueError("Can only have 1 Hours schedule set")
        self.__hourly = True
        self.__set = True
        self.__hours = self.__ensure_iterable(hours)
        return self

    def Minutes(self, minutes=None):
        if self.__minutely:
            ValueError("Can only have 1 Minuets schedule set")
        self.__minutely = True
        self.__set = True
        self.__minutes = self.__ensure_iterable(minutes)
        return self

    def Do(self, function, args=()):
        if not self.__set:
            ValueError("Must have at least 1 period (month, day, hour, etc.) set first")
        if not asyncio.iscoroutinefunction(function):
            TypeError("Function must be a coroutine")
        self.__function = function
        self.__args = args
        if self.cron is not None:
            self.cron.AddJob(self)
        return self

    def Test(self, dt):
        if not isinstance(dt, datetime.datetime):
            TypeError("dt must be a datetime instance")
        if not self.__set:
            return False
        first_period = True
        
        #Monthly
        if self.__monthly:
            first_period = False
            if self.__months is not None:
                if dt.month not in self.__months:
                    return False
              
        #Days
        if self.__daily:
            first_period = False
            if self.__days is not None:
                if dt.day not in self.__days:
                    return False
        elif self.__weekly:
            first_period = False
            if self.__weekdays is not None:
                if dt.weekday() not in self.__weekdays:
                    return False
        elif not first_period:
            if dt.day != 1:
                return False
        
        #Hours
        if self.__hourly:
            first_period = False
            if self.__hours is not None:
                if dt.hour not in self.__hours:
                    return False
        elif not first_period:
            if dt.hour != 0:
                return False
        
        #Minutes
        if self.__minutely:
            first_period = False
            if self.__minutes is not None:
                if dt.minute not in self.__minutes:
                    return False
        else:
            if dt.minute != 0:
                return False
        
        return True

    def __ensure_iterable(self, value):
        if value is None:
            return None
        if isinstance(value, Iterable):
            return value
        return (value,)
    
    async def Execute(self):
        try:
            await self.__function(*self.__args)
        except Exception as ex:
            print(ex)
        