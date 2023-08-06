from pastpy.database.database_image import DatabaseImage
from urllib.parse import urljoin
from urllib.request import pathname2url


class DbfDatabaseImage(DatabaseImage):
    def __init__(self, file_path):
        self.__file_path = file_path

    @property
    def full_size_url(self):
        return self.__path2url(self.__file_path)

    def __path2url(self, path):
        return urljoin('file:', pathname2url(path))

    @property
    def thumbnail_url(self):
        return None

    @property
    def title(self):
        return None
