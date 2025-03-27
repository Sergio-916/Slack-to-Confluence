from clients.slack_client import SlackClient
from clients.confluence_client import ConfluenceClient
from formatters.slack_to_confluence_formatter import SlackToConfluenceFormatter
from sync import SlackConfluenceSync
from config import config
from state.state_manager import StateManager
from ai.chat_analyzer import ChatAnalyzer

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

state_manager = StateManager()
slack_client = SlackClient(config.SLACK_TOKEN)
confluence_client = ConfluenceClient(
    config.CONFLUENCE_URL, config.CONFLUENCE_USERNAME, config.CONFLUENCE_API_TOKEN
)

analyzer = ChatAnalyzer(config.MODEL)

formatter = SlackToConfluenceFormatter()

syncer = SlackConfluenceSync(
    slack_client, confluence_client, formatter, state_manager, analyzer
)

for channel_id in config.SLACK_CHANNELS:
    syncer.sync_channel_to_confluence(channel_id, config.SPACE_KEY)
