from openai import OpenAI
from config.config import OPENAI_API_KEY, MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


class ChatAnalyzer:
    def __init__(self, model):
        self.model = model

    def summarize(self, messages):
        prompt = """You are a helpful assistant that can analyze messages from slack channel and 
        create document with all relative data and information for confluence knowledge base.
        Convert messages to HTML format. Use only <h1>, <h2>, <h3>, <p>, <ul>, <a>, <b>, <i> tags.
        Output format: <h1>Title</h1><p>Message</p>
        - if you need to add code snippet use following format 
        <ac:structured-macro ac:name="code">
        <ac:parameter ac:name="language">python</ac:parameter> <!-- язык опционально -->
        <ac:plain-text-body><![CDATA[
        def hello_world():
         print("Hello, world!")
          ]]></ac:plain-text-body>
            </ac:structured-macro>
            example: <h1>Example</h1><ac:structured-macro ac:name=\"code\"><ac:parameter ac:name=\"language\">python</ac:parameter><ac:plain-text-body><![CDATA[\ndef hello():\n    print(\"Hello, world!\")\n]]></ac:plain-text-body></ac:structured-macro>

"""
        messages_text = "\n".join(
            [msg.get("text", "") for msg in messages if msg.get("text")][::-1]
        )

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": messages_text},
            ],
        )

        print(completion.choices[0].message.content)

        return completion.choices[0].message.content
