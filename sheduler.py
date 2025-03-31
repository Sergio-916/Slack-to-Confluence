import schedule
import time
import subprocess
import sys
from config.config import SCHEDULE_TIME, SCHEDULE_INTERVAL, SCHEDULE_UNIT


def run_main_script():
    """Runs main.py"""
    print(
        f"Starting Slack-Confluence synchronization ({time.strftime('%Y-%m-%d %H:%M:%S')})"
    )
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
        print(
            f"Synchronization completed successfully ({time.strftime('%Y-%m-%d %H:%M:%S')})"
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running main.py: {e}")


# Setting up schedule according to parameters from config.py
if SCHEDULE_INTERVAL == "day" and SCHEDULE_TIME:
    schedule.every(SCHEDULE_UNIT).days.at(SCHEDULE_TIME).do(run_main_script)
elif SCHEDULE_INTERVAL == "hour":
    schedule.every(SCHEDULE_UNIT).hours.do(run_main_script)
elif SCHEDULE_INTERVAL == "minute":
    schedule.every(SCHEDULE_UNIT).minutes.do(run_main_script)
elif SCHEDULE_INTERVAL == "second":
    schedule.every(SCHEDULE_UNIT).seconds.do(run_main_script)
else:
    # Default - every day at 10:00
    schedule.every().day.at("10:00").do(run_main_script)

print(f"Scheduler started. Next run scheduled at: {schedule.next_run()}")

# Run the task once immediately when the script starts (optional)
# run_main_script()

while True:
    schedule.run_pending()
    time.sleep(1)
