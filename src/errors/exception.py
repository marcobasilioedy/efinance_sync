class EDYException(Exception):
    def __init__(self, title, code, http_status, description, translation):
        self.title = title
        self.code = code
        self.http_status = http_status
        self.description = description
        self.translation = translation
        super().__init__(f"[{code}] {title} - {description} ({translation})")

    def to_dict(self):
        return {
            "code": self.code,
            "title": self.title,
            "http_status": self.http_status,
            "description": self.description,
            "translation": self.translation,
        }