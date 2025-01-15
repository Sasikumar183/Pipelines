from typing import List, Union
import json
import base64

class Pipeline:
    def __init__(self):
        """Initializes the pipeline."""
        self.name = "Display Uploaded File Content Pipeline"
        print(f"Pipeline {self.name} initialized.")

    async def on_startup(self):
        """Called when the server starts."""
        print(f"Pipeline {self.name} starting up...")

    async def on_shutdown(self):
        """Called when the server shuts down."""
        print(f"Pipeline {self.name} shutting down...")

    async def inlet(self, body: dict, user: dict) -> dict:
        """Processes the incoming request body."""
        print(f"Received body in inlet: {json.dumps(body, indent=2)}")

        files = body.get("files", [])
        if files:
            file_data = files[0]  # Assuming only one file is uploaded
            try:
                file_content = file_data["file"]["data"]["content"]
                body["file_content"] = file_content
            except KeyError as e:
                print(f"Error extracting file content: {e}. Check the body structure.")
                body["file_content"] = None # Important to avoid errors later
        else:
            print("No files found in the request body.")
            body["file_content"] = None # Important to avoid errors later

        return body

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, None]:
        """Processes the file content and returns it."""

        file_content = body.get("file_content")

        if not file_content:
            return "No file uploaded."

        try:
            decoded_content = base64.b64decode(file_content).decode('utf-8')
            output = f"**Content of uploaded file:**\n```\n{decoded_content}\n```\n"

        except (base64.binascii.Error, UnicodeDecodeError):
            output = f"**Content of uploaded file:**\n```\n{file_content}\n```\n"

        return output
