from typing import Optional


class File:
    def __init__(self, content: bytes, content_type: Optional[str]):
        self.content = content
        self.content_type = content_type
