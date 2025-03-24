class SlackConfluenceSync:
    def __init__(
        self, slack_client, confluence_client, formatter, state_manager, analyzer
    ):
        self.slack = slack_client
        self.confluence = confluence_client
        self.formatter = formatter
        self.state = state_manager
        self.analyzer = analyzer

    def sync_channel_to_confluence(
        self,
        channel_id,
        SPACE_KEY,
        page_title=None,
        summarize=True,
    ):
        messages = self.slack.fetch_messages(channel_id)
        page_title = self.slack.get_channel_name(channel_id)
        space_id = self.confluence.get_space_id(SPACE_KEY)

        if not messages:
            print(f"No messages found in: {channel_id}")
            return

        message_count = len(messages)
        current_ts = messages[0]["ts"]

        prev_state = self.state.get_channel_state(channel_id)
        prev_count = prev_state["last_message_count"]
        prev_page_id = prev_state.get("page_id")
        page_id = self.confluence.get_page_id(prev_page_id)
        print("page_id", page_id)
        if message_count != prev_count or not page_id:
            if summarize and self.analyzer:
                summary = self.analyzer.summarize(messages)
                formatted_content = self.formatter.format(summary)
            else:
                formatted_content = self.formatter.format(messages)

            if prev_page_id and page_id:
                self.confluence.delete_page(prev_page_id)

            new_page_id = self.confluence.create_page(
                space_id, page_title, formatted_content
            )

            self.state.update_channel_state(
                channel_id, message_count, current_ts, new_page_id
            )

        else:
            print(f"No new messages in: {channel_id}")
