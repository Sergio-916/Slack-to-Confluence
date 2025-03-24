   Program overview:
   This program parses selected Slack channels, processes them using an LLM, formats them as documents, and stores them in Confluence in selected space as draft pages.
   Every night, the program checks for any changes in the Slack channels; if changes are detected, the program regenerates and replaces the relevant pages.

1. Create or select the necessary Slack channels that need to be processed.
2. Add the Channel IDs to `config.py` under the `SLACK_CHANNELS` section.

3. In the Slack API:
   a. Create a bot and generate the Bot User OAuth Token.
   b. Ensure that the bot has all necessary permissions in Slack API:     
      `channels:read`
      `channels:history`
      `groups:read`
      `groups:history`     
   c. Add the bot to the channel using the following command:
      `/invite @<your bot name>`
   d. Click "Add to Channel."
   e. Confirm that you have the necessary permissions to invite bots to the channel.

4. In Confluence:
   a. Create a separate space in Confluence Cloud where the generated pages will be stored.
   b. Add the space name to `config.py` under the `SPACE_KEY` section.

5. Fill in all listed credentials in the `.env` file:
   ```
   SLACK_TOKEN=""
   CONFLUENCE_URL=""
   CONFLUENCE_USERNAME=""
   CONFLUENCE_API_TOKEN=""
   CONFLUENCE_SPACE_KEY=""
   OPENAI_API_KEY=""
   ```
