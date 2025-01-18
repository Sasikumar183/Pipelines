from typing import List, Union
import json
import base64

class Pipeline:
    # ... (other methods)

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, None]:
        """Display file content from context (supports various file types)."""

        print(f"Received body in pipe: {json.dumps(body, indent=2)}")

        if not body or not isinstance(body.get("messages"), list) or len(body["messages"]) == 0:
            return "No messages received."

        system_message = body["messages"][0]
        if "content" not in system_message:
            return "No content found in the first message."

        content = system_message["content"]

        try:
            context_start = content.find("<context>") + len("<context>")
            context_end = content.find("</context>")
            context_str = content[context_start:context_end]
            context = {"source": []}
            while True:
                source_start = context_str.find("<source>")
                if source_start == -1:
                    break
                source_end = context_str.find("</source>")
                source_data = context_str[source_start + len("<source>"):source_end]

                id_start = source_data.find("<source_id>") + len("<source_id>")
                id_end = source_data.find("</source_id>")
                source_id = source_data[id_start:id_end]

                context_start = source_data.find("<source_context>") + len("<source_context>")
                context_end = source_data.find("</source_context>")
                source_context = source_data[context_start:context_end]

                context["source"].append({"source_id": source_id, "source_context": source_context})

                context_str = context_str[source_end + len("</source>"):]

        except (ValueError, IndexError):
            return "Could not parse context from message content."

        print(f"Extracted context: {json.dumps(context, indent=2)}")

        output = ""
        for source in context.get("source", []):
            source_id = source.get("source_id")
            source_context = source.get("source_context")

            if source_context:
                try:
                    # Attempt to decode base64 if it looks like encoded data
                    decoded_content = base64.b64decode(source_context).decode('utf-8')
                    output += f"**Content of {source_id}:**\n```\n{decoded_content}\n```\n"

                except (base64.binascii.Error, UnicodeDecodeError):
                    # If not base64 or decoding fails, treat as plain text
                    output += f"**Content of {source_id}:**\n```\n{source_context}\n```\n"
            else:
                output += f"No content found for {source_id}.\n"

        if not output:
            return "No content found in the provided sources."

        return output