try:
    from CoroCron.Cron import Cron
    from CoroCron.Job import Job
    from CoroCron.Timer import Timer
    from CoroCron.Weekdays import Weekdays
except ImportError:
    pass

__name__ = 'CoroCron'
__version__ = '0.1.4'