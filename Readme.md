   ## Program overview: ##
   This program parses selected Slack channels, processes threads using an LLM as separate documents, formats them as Confluence documents, and stores them in Confluence in selected space as draft pages.
   Every night, the program checks for any changes in the assigned Slack channels; if changes are detected in any of the threads, the program regenerates and replaces the relevant pages in Confluence.

## Prerequisites: ##
1. Create or select the necessary Slack channels that need to be processed.
2. Add the Channel IDs to `config.py` under the `SLACK_CHANNELS` section.

3. Create a bot in the Slack API:
   a. Create a bot and generate the Bot User OAuth Token.
   b. Ensure that the bot has all necessary permissions in Slack API:     
      `channels:read`
      `channels:history`
      `groups:read`
      `groups:history`  
      `files:read`
      `files:write`
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
## Features: ##
1. Process threads as separate documents.
2. Format documents as Confluence documents based on html format supporting links, bold, italic, underline, and tables.
3. Store documents in Confluence in selected space as draft pages.
4. Check for changes in the assigned Slack channels every night.
5. Current state of the threads is stored on the `data/state.json` file.
6. Regenerate and replace the relevant pages if changes in threads are detected.
7. Creates name for the docunet based on the content.
8. Keeps the same name if the same content is changed and updated (not regenerate new name with LLM).
9. Parce images from the thread and add context to the document. It is possible to process multiple images and create common images summary.
10. If the same images are kept in the thread, the program will use existing images summary and not download and process images one more time.
11. Image files store in the `data/images` folder.
12. it is possible to disconnect image processing from the main logic.
13. if document is deleted in Confluence, the program will regenerate the docunent based on Slack content.

