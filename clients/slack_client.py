import requests


class SlackClient:
    def __init__(self, token):
        self.token = token

    def fetch_messages(self, channel_id, limit=100):
        url = "https://slack.com/api/conversations.history"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"channel": channel_id, "limit": limit}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200 and response.json().get("ok"):
            return response.json()["messages"]
        else:
            print("❌ Error fetching messages from Slack:", response.text)
            return []

    def get_channel_name(self, channel_id):
        url = "https://slack.com/api/conversations.info"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"channel": channel_id}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200 and response.json().get("ok"):
            return response.json()["channel"]["name"]
        else:
            print("❌ Error getting channel info from Slack:", response.text)
        return None
