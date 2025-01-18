from typing import List, Union, Generator, Iterator

class Pipeline:
    def __init__(self):
        self.name = "File Handler Pipeline II"
        self.file_handler = True
        self.citation = True

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict, __files__: List[dict] = []
    ) -> Union[str, Generator, Iterator]:
        print(f"Processing message: {user_message}")
        print(f"Body: {body}") # print the body for debugging
        if __files__: # check if __files__ is not empty
            return self.get_files(__files__)
        else:
            return "No files provided."
        

    def get_files(self, __files__: List[dict]) -> str:
        """
        Get the files and generate appropriate responses.
        """

        print(f"Files received: {__files__}") # better logging
        file_responses = []
        for file_info in __files__:
            file_id = file_info.get('id')
            file_name = file_info.get('name')
            file_type = file_info.get('type')  # Or infer from name/content
            file_url = file_info.get('url')

            if not file_id:
                file_responses.append(f"Invalid file information: {file_info}")
                continue

            if file_type == 'video' or (file_url and file_url.lower().endswith(('.mp4', '.mov', '.avi'))):
                file_responses.append(f"Render video: {{VIDEO_FILE_ID_{file_id}}}")
            elif file_type == 'html' or (file_url and file_url.lower().endswith('.html')):
                file_responses.append(f"Render HTML: {{HTML_FILE_ID_{file_id}}}")
            elif file_type == 'text' or (file_url and file_url.lower().endswith(('.txt', '.csv', '.json'))):
                file_responses.append(f"Access text content: `/api/v1/files/{file_id}/content`")
            else:
                file_responses.append(f"Access file (type unknown): `/api/v1/files/{file_id}/content`")

        return "\n".join(file_responses) # join to single string