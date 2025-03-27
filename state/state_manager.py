import json
import os


class StateManager:
    def __init__(self, path="data/state.json"):
        print(f"Initializing StateManager with path: {path}")
        self.path = path
        print(f"Checking if directory exists: {os.path.dirname(self.path)}")
        if not os.path.exists(os.path.dirname(self.path)):
            print("Creating directory...")
            os.makedirs(os.path.dirname(self.path))
        print(f"Checking if file exists: {self.path}")
        if not os.path.exists(self.path):
            print("Creating new state file...")
            self.state = {}
            self._save()
        else:
            print("Loading existing state file...")
            with open(self.path, "r") as f:
                self.state = json.load(f)

    def get_channel_state(self, channel_id, thread_ts):
        return self.state.get(channel_id, {}).get(
            thread_ts,
            {
                "page_id": None,
                "reply_count": None,
                "page_title": None,
                "latest_reply": None,
                "images": None,
                "images_summary": None,
            },
        )

    def update_channel_state(
        self,
        channel_id,
        page_id,
        reply_count,
        latest_reply,
        page_title,
        thread_ts,
        images,
        images_summary,
    ):
        if channel_id not in self.state:
            self.state[channel_id] = {}
        self.state[channel_id][thread_ts] = {
            "page_id": page_id,
            "reply_count": reply_count,
            "latest_reply": latest_reply,
            "page_title": page_title,
            "images": images,
            "images_summary": images_summary,
        }
        print("state updated")
        self._save()

    def _save(self):
        print(f"Saving state to: {self.path}")
        try:
            with open(self.path, "w") as f:
                json.dump(self.state, f, indent=2)
            print("State saved successfully")
        except Exception as e:
            print(f"Error saving state: {str(e)}")

    def delete_channel_state(self, channel_id, thread_ts):
        if channel_id in self.state:
            self.state[channel_id][thread_ts] = {
                "page_title": None,
                "page_id": None,
                "reply_count": None,
                "latest_reply": None,
                "images": None,
                "images_summary": None,
            }
            self._save()
