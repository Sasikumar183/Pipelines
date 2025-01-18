from typing import List, Union
import json
import traceback
import re

class Pipeline:
    def __init__(self):
        self.name = "WorkwithFile"
        print(f"Pipeline {self.name} initialized.")

    async def on_startup(self):
        print(f"Pipeline {self.name} starting up...")

    async def on_shutdown(self):
        print(f"Pipeline {self.name} shutting down...")

    def process_file(self, file_content):
        try:
            order_entries = re.findall(r"<source_context>(.*?)</source_context>", file_content, re.DOTALL)
            orders = []
            for entry in order_entries:
                try:
                    lines = entry.strip().split('\n')
                    order = {}
                    for line in lines:
                        if ":" in line:
                            key, value = line.split(":", 1)
                            order[key.strip()] = value.strip()
                    if order:
                        orders.append(order)
                except ValueError:
                    print(f"Skipping malformed entry: {entry}")

            return json.dumps(orders, indent=4)

        except Exception as e:
            traceback.print_exc()
            return f"An error occurred during file processing: {str(e)}"

    def extract_context(self, messages: List[dict]) -> Union[str, None]:
        context = ""
        for message in messages:
            if message.get("role") == "system":
                content = message.get("content", "")
                if "<context>" in content and "</context>" in content:
                    context_start = content.find("<context>") + len("<context>")
                    context_end = content.find("</context>")
                    context = content[context_start:context_end]
                    break
        return context

    def extract_all_file_contents(self, context: str) -> List[str]:  # Returns a list
        """Extracts ALL file contents from the context string."""
        return re.findall(r"<source_context>(.*?)</source_context>", context, re.DOTALL)

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, None]:
        print(f"Body: {body}")
        print(f"Body keys: {body.keys()}")

        try:
            context = self.extract_context(messages)
            if not context:
                return "No context found in the messages."

            file_contents = self.extract_all_file_contents(context) #Get all file contents
            if file_contents:
                all_orders = []
                for file_content in file_contents: #Iterate through all content and process them
                    json_output = self.process_file(file_content)
                    try:
                        orders = json.loads(json_output)
                        all_orders.extend(orders) #extend the list instead of appending
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        print(f"JSON String that caused the error: {json_output}")
                        return "Error in json decoding"


                return f'''{json.dumps(all_orders, indent=4)}'''#Return the final json using '''

            else:
                return "No file content found in the context."

        except Exception as e:
            traceback.print_exc()
            return f"An error occurred: {str(e)}"