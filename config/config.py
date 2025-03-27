import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


SLACK_TOKEN = os.getenv("SLACK_TOKEN")
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SPACE_KEY = "testspace"

# SLACK_CHANNELS = ["C08HPBUUNBD", "C08JNCY70TC"]
SLACK_CHANNELS = ["C08HPBUUNBD"]

MODEL = "gpt-4o"
