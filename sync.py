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
        images_summary=True,
    ):
        space_id = self.confluence.get_space_id(SPACE_KEY)
        messages = self.slack.fetch_messages(channel_id)

        threads_ts = self.slack.fetch_threads_ts(channel_id)

        for thread_ts in threads_ts:
            replies = self.slack.fetch_thread_replies(channel_id, thread_ts)
            if images_summary:
                images = self.slack.fetch_images(replies)

            page_title = self.state.get_channel_state(channel_id, thread_ts).get(
                "page_title"
            )

            reply_count = len(replies)

            latest_reply = messages[0].get("latest_reply")
            prev_state = self.state.get_channel_state(channel_id, thread_ts)
            prev_page_id = prev_state.get("page_id")
            prev_reply_count = prev_state.get("reply_count")
            prev_images = prev_state.get("images")
            prev_images_summary = prev_state.get("images_summary")
            page_id = self.confluence.get_page_id(prev_page_id)
            if not page_title or not page_id:
                self.state.delete_channel_state(channel_id, thread_ts)
                page_title = self.analyzer.create_article_name(replies)

            if reply_count != prev_reply_count or not page_id:
                if summarize and self.analyzer:
                    if images_summary and prev_images != images:
                        self.slack.download_images(images)
                        images_summary = self.analyzer.images_summary(images)
                    else:
                        images_summary = prev_images_summary

                    formatted_content = self.analyzer.summarize(replies, images_summary)
                else:
                    formatted_content = self.formatter.format(replies)

                if prev_page_id and page_id:
                    self.confluence.delete_page(prev_page_id)

                new_page_id = self.confluence.create_page(
                    space_id, page_title, formatted_content
                )

                self.state.update_channel_state(
                    channel_id,
                    new_page_id,
                    reply_count,
                    latest_reply,
                    page_title,
                    thread_ts,
                    images,
                    images_summary,
                )

        else:
            print(f"No new messages in thread: {thread_ts}")
