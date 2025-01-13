import csv
import json
import io
from typing import Union, Generator, Iterator
from fastapi import UploadFile

class Pipeline:
    def __init__(self):
        # Define the name of your pipeline
        self.name = "File Conversion Pipeline"

    async def on_startup(self):
        # Called when the server starts
        print(f"on_startup: {self.name}")

    async def on_shutdown(self):
        # Called when the server stops
        print(f"on_shutdown: {self.name}")

    def csv_to_json(self, csv_content: str) -> str:
        """Converts CSV content to JSON format."""
        data = []
        csv_file = io.StringIO(csv_content)
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
        return json.dumps(data, indent=4)

    def json_to_csv(self, json_content: str) -> str:
        """Converts JSON content to CSV format."""
        data = json.loads(json_content)
        if isinstance(data, list) and data:
            output = io.StringIO()
            csv_writer = csv.DictWriter(output, fieldnames=data[0].keys())
            csv_writer.writeheader()
            for row in data:
                csv_writer.writerow(row)
            return output.getvalue()
        else:
            raise ValueError("JSON data is not a list or is empty.")

    async def pipe(
        self, user_message: str, model_id: str, messages: list, body: dict
    ) -> Union[str, Generator, Iterator]:
        """Main pipeline function to handle file conversion."""
        file: UploadFile = body.get("file")
        target_format: str = body.get("target_format")

        if not file or not target_format:
            return "Error: Missing file or target format."

        content = await file.read()
        content_str = content.decode('utf-8')

        try:
            if file.content_type == 'text/csv' and target_format == 'json':
                return self.csv_to_json(content_str)
            elif file.content_type == 'application/json' and target_format == 'csv':
                return self.json_to_csv(content_str)
            else:
                return "Error: Unsupported file type or target format."
        except Exception as e:
            return f"Error during conversion: {e}"
