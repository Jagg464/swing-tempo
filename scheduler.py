"""APScheduler entry: nightly Committee Reporter sweep + daily Deadline Sentinel +
monthly Savings Agent check-in. Start with: python scheduler.py

This is the always-on process for the Mac. In DRY_RUN it logs intended actions.
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from config import settings
import main

sched = BlockingScheduler()


@sched.scheduled_job("cron", hour=2, minute=0)        # nightly web monitoring
def nightly_reporter():
    main.run(entry="committee_reporter", dry_run=settings.DRY_RUN)


@sched.scheduled_job("interval", seconds=settings.GMAIL_POLL_SECONDS)   # email polling
def poll_email():
    main.run(entry="email_monitor", dry_run=settings.DRY_RUN)


# Daily Deadline Sentinel + monthly Savings check-in are TODO wiring:
# the sentinel runs at the start of every pipeline pass already; the standalone
# daily alert sweep and the first-Sunday Savings check-in need their own jobs.
# [TODO] add cron jobs for: daily sentinel alert sweep; monthly savings check-in
#        (first Sunday — see config.SAVINGS_CHECKIN_WEEKDAY).

if __name__ == "__main__":
    print("Acton Finance Agent scheduler starting (DRY_RUN=%s)" % settings.DRY_RUN)
    sched.start()