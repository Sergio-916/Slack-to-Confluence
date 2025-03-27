from openai import OpenAI
import base64
from config.config import OPENAI_API_KEY, MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


class ChatAnalyzer:
    def __init__(self, model):
        self.model = model

    def create_article_name(self, replies):
        prompt = """
                Please create naming for article based on context.
                Output format: string not more than 120 characters
                """

        replies_text = "\n".join(
            [reply.get("text", "") for reply in replies if reply.get("text")]
        )
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": replies_text},
            ],
        )

        raw_title = completion.choices[0].message.content.strip()
        if raw_title.startswith('"') and raw_title.endswith('"'):
            raw_title = raw_title[1:-1]
        return raw_title

    def images_summary(self, images):
        content_images = []
        for image in images:
            image_name = image.get("name")
            image_path = f"./data/images/{image_name}"

            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")

            content_images.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                }
            )
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "what's in this images? You have to analyze and summary inpormation, this information will be part of the Confluence article.",
                        },
                        *content_images,
                    ],
                }
            ]
        if not content_images:
            return None
        completion = client.chat.completions.create(
            model=MODEL, messages=messages, max_tokens=4000
        )
        images_summary = completion.choices[0].message.content
        print("images_summary processed")
        return images_summary

    def summarize(self, replies, images_summary=None):
        prompt = """You are a helpful assistant that can analyze messages from Slack thread and 
        create Confluence document with all relative data and information for confluence knowledge base.
        - remove ubsolutely unrelevant messages
        - Convert messages to HTML format. Use only <h1>, <h2>, <h3>, <p>, <ul>, <a>, <b>, <i> tags.
        - use images summary to update article if it's relevant
        Output format: 
        - for title and text use example: <h2>Title</h2><p>Message</p>
        - for code snippet use example: 
        <ac:structured-macro ac:name="code">
        <ac:parameter ac:name="language">python</ac:parameter>
        <ac:plain-text-body><![CDATA[
        def hello_world():
         print("Hello, world!")
          ]]></ac:plain-text-body>
            </ac:structured-macro>
            example: <h1>Example</h1><ac:structured-macro ac:name=\"code\"><ac:parameter 
            ac:name=\"language\">python</ac:parameter><ac:plain-text-body><![CDATA[\ndef hello():\n    
            print(\"Hello, world!\")\n]]></ac:plain-text-body></ac:structured-macro>
        - for tables use example: <table>
            <tr>
            <th>Header 1</th>
            <th>Header 2</th>
            </tr>
            <tr>
            <td>Cell 1</td>
            <td>Cell 2</td>
        - do not use (```html ```) tags
"""
        replies_text = "\n".join(
            [reply.get("text", "") for reply in replies if reply.get("text")]
        )
        if images_summary:
            images_summary = f"\n\nFile summary: {images_summary}"
            replies_text = f"{replies_text}\n\n{images_summary}"

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": replies_text},
            ],
        )

        return completion.choices[0].message.content
