import schedule
import time

from config.config import (
    SLACK_TOKEN,
    CONFLUENCE_URL,
    CONFLUENCE_USERNAME,
    CONFLUENCE_API_TOKEN,
    MODEL,
    SLACK_CHANNELS,
    SPACE_KEY,
    SCHEDULE_TIME,
    SCHEDULE_INTERVAL,
    SCHEDULE_UNIT,
)

from clients.slack_client import SlackClient
from clients.confluence_client import ConfluenceClient
from formatters.slack_to_confluence_formatter import SlackToConfluenceFormatter
from sync import SlackConfluenceSync
from state.state_manager import StateManager
from ai.chat_analyzer import ChatAnalyzer

from config.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


def run_sync():
    """Runs the main synchronization logic."""
    logger.info(
        f"Starting Slack-Confluence synchronization ({time.strftime('%Y-%m-%d %H:%M:%S')})"
    )
    try:
        state_manager = StateManager()
        slack_client = SlackClient(SLACK_TOKEN)
        confluence_client = ConfluenceClient(
            CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN
        )
        analyzer = ChatAnalyzer(MODEL)
        formatter = SlackToConfluenceFormatter()
        syncer = SlackConfluenceSync(
            slack_client, confluence_client, formatter, state_manager, analyzer
        )

        for channel_id in SLACK_CHANNELS:
            logger.info(f"Syncing channel {channel_id}...")
            syncer.sync_channel_to_confluence(channel_id, SPACE_KEY)
            logger.info(f"Channel {channel_id} sync complete.")

        logger.info(
            f"Synchronization completed successfully ({time.strftime('%Y-%m-%d %H:%M:%S')})"
        )
    except Exception as e:
        logger.error(f"Error during synchronization: {e}", exc_info=True)


if __name__ == "__main__":
    logger.info("Scheduler starting...")

    # Setting up schedule according to parameters from config.py
    if SCHEDULE_INTERVAL == "day" and SCHEDULE_TIME:
        schedule.every(SCHEDULE_UNIT).days.at(SCHEDULE_TIME).do(run_sync)
        logger.info(
            f"Scheduled daily run at {SCHEDULE_TIME} every {SCHEDULE_UNIT} day(s)."
        )
    elif SCHEDULE_INTERVAL == "hour":
        schedule.every(SCHEDULE_UNIT).hours.do(run_sync)
        logger.info(f"Scheduled hourly run every {SCHEDULE_UNIT} hour(s).")
    elif SCHEDULE_INTERVAL == "minute":
        schedule.every(SCHEDULE_UNIT).minutes.do(run_sync)
        logger.info(f"Scheduled minute run every {SCHEDULE_UNIT} minute(s).")
    elif SCHEDULE_INTERVAL == "second":
        schedule.every(SCHEDULE_UNIT).seconds.do(run_sync)
        logger.info(f"Scheduled second run every {SCHEDULE_UNIT} second(s).")
    else:
        # Default - every day at 10:00
        schedule.every().day.at("10:00").do(run_sync)
        logger.info("Scheduled daily run at 10:00 (default).")

    logger.info(f"Next run scheduled at: {schedule.next_run()}")

    # Run the task once immediately when the script starts (optional, uncomment if needed)
    # logger.info("Running initial sync immediately.")
    # run_sync()

    while True:
        schedule.run_pending()
        time.sleep(1)
