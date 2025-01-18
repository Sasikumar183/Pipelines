from typing import List, Union, Generator, Iterator
import csv
import json
from io import StringIO
import requests


class Pipeline:
    def __init__(self):
        self.name = "CsvToJsonPipeline"

    async def on_startup(self):
        # This function is called when the server starts.
        print(f"on_startup: {self.name}")

    async def on_shutdown(self):
        # This function is called when the server stops.
        print(f"on_shutdown: {self.name}")

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # Custom pipeline logic
        print(f"pipe: {self.name}")

        if body.get("title", False):
            print("Title Generation")
            return "CsvToJsonPipeline"
        else:
            try:
                # Remove BOM if present
                if user_message.startswith("\ufeff"):
                    user_message = user_message.lstrip("\ufeff")

                # Read CSV from string
                csv_input = StringIO(user_message)
                csv_reader = csv.DictReader(csv_input)

                # Read CSV rows into a list of dictionaries
                json_data = [row for row in csv_reader]
                csv_input.close()

                # Return JSON as a formatted string
                json_str = json.dumps(json_data, indent=4)
                return f"**Received JSON Data:**\n```json\n{json_str}\n```" # Embed the JSON string

            except Exception as e:
                return f"Error: {e}"

