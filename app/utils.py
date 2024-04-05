from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType

file_storage = FileSystemStorage(path="./app/static/images")


class CustomFileType(FileType):
    """
    Кастомный тип для поля image, чтобы загружать картинки через админку
    """
    def __init__(self, *args, **kwargs):
        super().__init__(storage=file_storage, *args, **kwargs)

    def process_result_value(self, value, dialect):
        if value:
            return f"/images/{value}"
        return value
