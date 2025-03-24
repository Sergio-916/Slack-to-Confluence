import json
import os


class StateManager:
    def __init__(self, path="data/state.json"):
        self.path = path
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        if not os.path.exists(self.path):
            self.state = {}
            self._save()
        else:
            with open(self.path, "r") as f:
                self.state = json.load(f)

    def get_channel_state(self, channel_id):
        return self.state.get(
            channel_id,
            {"last_message_count": 0, "last_message_ts": None, "page_id": None},
        )

    def update_channel_state(self, channel_id, message_count, message_ts, page_id):
        self.state[channel_id] = {
            "last_message_count": message_count,
            "last_message_ts": message_ts,
            "page_id": page_id,
        }
        self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)

    def delete_channel_state(self, channel_id):
        self.state[channel_id] = {
            "last_message_count": 0,
            "last_message_ts": None,
            "page_id": None,
        }
        self._save()
