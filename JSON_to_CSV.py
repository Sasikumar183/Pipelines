from typing import List, Union, Generator, Iterator
import json
import csv
from io import StringIO
import requests


class Pipeline:
    def __init__(self):
        self.name = "JsonToCsvPipeline"

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
            return "JsonToCsvPipeline"
        else:
            try:
                # Parse the JSON string
                json_data = json.loads(user_message)

                # Validate the JSON data format
                if not isinstance(json_data, list) or not all(isinstance(item, dict) for item in json_data):
                    return "Invalid JSON format. Expected a list of dictionaries."

                # Extract headers and write CSV with formatting options
                headers = json_data[0].keys()
                csv_output = StringIO()
                csv_writer = csv.DictWriter(csv_output, fieldnames=headers, extrasaction='ignore')  # Ignore extra keys
                csv_writer.writeheader()

                # Option 1: Default formatting
                csv_writer.writerows(json_data)

                # Option 2: Quoting all fields (can be useful for data with special characters)
                # for row in json_data:
                #     csv_writer.writerow({k: v for k, v in row.items()})

                # Option 3: Custom formatting using a loop (more control)
                # for row in json_data:
                #     formatted_row = {k: f"{v}" for k, v in row.items()}  # Customize formatting here
                #     csv_writer.writerow(formatted_row)

                # Get CSV as string
                csv_data = csv_output.getvalue()
                csv_output.close()

                return csv_data

            except json.JSONDecodeError:
                return "Error: Invalid JSON input."
            except Exception as e:
                return f"Error: {e}"