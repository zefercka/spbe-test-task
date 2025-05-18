
class UnsupportedMethodError(Exception):
    def __init__(self):
        super().__init__(
            "Only POST and GET methods are supported"
        )
        

class FileNotFoundError(Exception):
    def __init__(self, filename: str, path_to_file: str):
        super().__init__(
            f"File '{filename}' not found. \n Expected path is '{path_to_file}'"
        )


class InvalidRequestError(Exception):
    def __init__(self, message: str):
        super().__init__(message)