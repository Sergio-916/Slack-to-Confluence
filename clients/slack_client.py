import requests
import os
import datetime


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

    def fetch_threads_ts(self, channel_id):
        messages = self.fetch_messages(channel_id, 100)
        threads_ts = [msg["ts"] for msg in messages if msg.get("ts")]
        return threads_ts

    def fetch_thread_replies(self, channel_id, thread_ts):
        """Fetch all replies in a specific thread"""
        url = "https://slack.com/api/conversations.replies"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"channel": channel_id, "ts": thread_ts}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200 and response.json().get("ok"):
            return response.json()["messages"]
        else:
            print("❌ Error fetching replies from Slack:", response.text)
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

    def fetch_images(self, messages):
        images = []
        counter = 0
        for message in messages:
            if message.get("files"):
                for file in message.get("files"):
                    if file.get("filetype") in ["jpg", "jpeg", "png", "gif", "bmp"]:
                        counter += 1
                        images.append(
                            {
                                "text": message.get("text"),
                                "url": file.get("url_private_download"),
                                "name": str(counter) + "_" + file.get("name"),
                                "size": file.get("size"),
                                "timestamp": message.get("ts"),
                            }
                        )

        return images

    def download_images(self, images):
        images_dir = "./data/images"
        os.makedirs(images_dir, exist_ok=True)
        headers = {"Authorization": f"Bearer {self.token}"}
        counter = 0
        for image in images:
            counter += 1
            response = requests.get(image.get("url"), headers=headers)

            if response.status_code == 200:
                image_name = image.get("name")
                with open(f"{images_dir}/{image_name}", "wb") as f:
                    f.write(response.content)

                print(f"✅ Saved: {image_name}")

            else:
                print(
                    f"Failed to download {image.get('name')}: HTTP {response.status_code}"
                )
