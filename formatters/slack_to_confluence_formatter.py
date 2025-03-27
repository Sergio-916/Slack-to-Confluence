class SlackToConfluenceFormatter:
    def format(self, slack_replies):
        formatted_messages = ""

        for reply in slack_replies:
            formatted_messages += reply["text"]
        print(formatted_messages)
        return "<p>" + formatted_messages + "</p>"
