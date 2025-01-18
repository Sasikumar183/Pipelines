from typing import List, Union, Generator, Iterator

class Pipeline:
    def __init__(self):
        self.name = "00 Repeater Example"

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")

    async def on_shutdown(self):
        # This function is called when the server is shut down.
        print(f"on_shutdown:{__name__}")

    async def inlet(self, body: dict, user: dict) -> dict:
        """
        This function is called to process the incoming body before passing it to the `pipe` method.
        """
        print(f"Received body: {body}")
        # Ensure the body is returned
        return body

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        """
        Process the user's message and print all metadata content.
        """
        print(f"Received message from user: {user_message}")  # Log the user message

        # Extract and print the metadata content
        metadata = body.get("metadata", {})
        if metadata:
            print(f"Metadata content: {metadata}")
            return f"Metadata content: {metadata}"
        else:
            return "No metadata found in the request body."
        