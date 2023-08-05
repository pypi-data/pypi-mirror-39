import asyncio
import datetime
import CoroCron


class Timer():
    def __init__ (self, use_utc = False):
        super(Timer, self).__init__()
        self.utc = use_utc
        self.jobs = []
        

    async def start(self):
        while True:
            try:
                if self.utc:
                    now = datetime.datetime.utcnow()
                else:
                    now = datetime.datetime.now()
                for job in self.jobs:
                    if job.Test(now):
                        asyncio.create_task(job.Execute())
                await self.__wait()
            except KeyboardInterrupt:
                break

    def AddJob(self, job):
        if isinstance(job, CoroCron.Job):
            self.jobs.append(job)

    async def __wait(self):
        now = datetime.datetime.now()
        then = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute) + datetime.timedelta(minutes=1)
        span = then - now
        await asyncio.sleep(span.total_seconds()) #In theory this should be 60 seconds but this will prevent drifting



    

    