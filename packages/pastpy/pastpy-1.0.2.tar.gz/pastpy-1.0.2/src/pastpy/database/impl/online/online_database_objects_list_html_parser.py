from bs4 import BeautifulSoup
from pastpy.gen.database.impl.online.online_database_objects_list_item import OnlineDatabaseObjectsListItem
import logging


class OnlineDatabaseObjectsListHtmlParser(object):
    def __init__(self):
        self.__logger = logging.getLogger(self.__class__.__name__)

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        results = []
        for indvResult in soup.find_all(attrs={"class": "indvResult"}):
            details = indvResult.find(attrs={"class": "indvResultDetails"})
            if not details:
                self.__logger.warn("object has no details: %s", indvResult)
                continue

            result_builder = OnlineDatabaseObjectsListItem.Builder()
            image = indvResult.find(attrs={"class": "indvImage"})
            if image:
                result_builder.thumbnail_src = image.a.img.attrs["src"]
            # else:
            #     self.__logger.debug("object has no image: %s", indvResult)

            result_builder.detail_href = details.h1.a.attrs["href"]
            result_builder.title = str(details.h1.a.contents[0].string).strip()
            result_builder.record_type = str(details.h4.contents[1].string).strip()
            results.append(result_builder.build())
        return tuple(results)
