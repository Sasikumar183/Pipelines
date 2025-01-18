from typing import List, Union
import asyncio

class Pipeline:
    def __init__(self):
        self.name = "Display Uploaded File Content Pipeline"
        self.inlet_details = []
        print(f"Pipeline {self.name} initialized.")

    async def on_startup(self):
        print(f"Pipeline {self.name} starting up...")

    async def on_shutdown(self):
        print(f"Pipeline {self.name} shutting down...")

    async def inlet(self, body: dict, user: dict) -> dict:
        print(f"Received body: {body}")
        files = body.get("files", [])
        for file in files:
            self.inlet_details.append({
                "filename": file.get("filename", "unknown"),
                "url": file.get("url", "unknown"),
            })
        return body

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, None]:
        """Generates output based on the passed body."""
        if not body:
            return "No data provided to pipe."
        
        return f"**Processed Data:Welcome**\n{self.inlet_details}"
