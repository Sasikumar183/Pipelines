from typing import Union, Generator, Iterator
from fastapi import UploadFile
import io

class Pipeline:
    def __init__(self):
        self.name = "File Display Pipeline"

    async def on_startup(self):
        """Called when the server starts."""
        print(f"on_startup: {self.name}")

    async def on_shutdown(self):
        """Called when the server stops."""
        print(f"on_shutdown: {self.name}")

    async def pipe(
        self, user_message: str, model_id: str, messages: list, body: dict
    ) -> Union[str, Generator, Iterator]:
        """Main pipeline function to handle file display."""
        file: UploadFile = body.get("file")
        return "Hello"
        if not file:
            return "Error: No file uploaded."

        content = await file.read()
        content_str = content.decode('utf-8', errors='ignore')  # Decode with error handling
        print(content_str)
        return content_str
