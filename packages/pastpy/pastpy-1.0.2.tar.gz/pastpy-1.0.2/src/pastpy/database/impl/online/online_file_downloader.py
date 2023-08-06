import http.client
import logging
import os.path
from time import sleep


class OnlineFileDownloader(object):
    def __init__(self, *, file_paths, host):
        self.__http_client_connection = None
        self.__file_paths = file_paths
        self.__host = host
        self.__logger = logging.getLogger(self.__class__.__name__)

    def download_object_detail(self, *, guid):
        object_detail_file_path = self.__file_paths.object_detail_file_path(guid)
        if os.path.isfile(object_detail_file_path):
            self.__logger.debug("object detail file %s already exists, skipping", object_detail_file_path)
            return

        object_details_dir_path = self.__file_paths.object_details_dir_path
        self.__makedirs(object_details_dir_path)

        object_detail_html = self.__download("/webobject/" + guid)
        self.__write_file(object_detail_html, object_detail_file_path)

    def download_objects_list(self):
        objects_list_dir_path = self.__file_paths.objects_list_dir_path
        self.__makedirs(objects_list_dir_path)
        page_i = 1
        while self.__download_objects_list_page(page_i):
            page_i = page_i + 1

    def __download_objects_list_page(self, page_i):
        page_file_path = self.__file_paths.objects_list_page_file_path(page_i)
        if os.path.isfile(page_file_path):
            self.__logger.debug("objects list page file %s already exists, skipping", page_file_path)
            return True
        page_contents = self.__download("/webobject?page=" + str(page_i))
        if "No results found" in str(page_contents):
            self.__logger.debug("objects list page %d was the last, stopping", page_i)
            return False
        self.__write_file(page_contents, page_file_path)
        return True

    def __download(self, url_path):
        self.__logger.debug("retrieving %s", url_path)
        self.__http_client_connection.request("GET", url_path)
        response = self.__http_client_connection.getresponse()
        html = response.read()
        self.__logger.debug("retrieved %s", url_path)
        sleep(1)
        return html

    def __enter__(self):
        if not os.path.isdir(self.__file_paths.root_dir_path):
            os.makedirs(self.__file_paths.root_dir_path)

        self.__http_client_connection = http.client.HTTPConnection(self.__host)

        return self

    def __exit__(self, *args, **kwds):
        self.__http_client_connection.close()

    def __makedirs(self, dir_path):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
            self.__logger.info("created directory %s", dir_path)

    def __write_file(self, file_contents, file_path):
        with open(file_path, "w+b") as file_:
            file_.write(file_contents)
            self.__logger.info("wrote %s", file_path)
