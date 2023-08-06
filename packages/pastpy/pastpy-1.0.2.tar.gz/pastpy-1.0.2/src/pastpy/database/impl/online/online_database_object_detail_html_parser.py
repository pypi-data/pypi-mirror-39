from bs4 import BeautifulSoup

from pastpy.gen.database.impl.online.online_database_object_detail import OnlineDatabaseObjectDetail
from pastpy.gen.database.impl.online.online_database_object_detail_image import OnlineDatabaseObjectDetailImage
from pastpy.gen.database.impl.online.online_database_object_detail_image_type import OnlineDatabaseObjectDetailImageType


class OnlineDatabaseObjectDetailHtmlParser(object):
    def parse(self, *, guid, html):
        soup = BeautifulSoup(html, "html.parser")
        result_builder = OnlineDatabaseObjectDetail.Builder()

        result_builder.guid = guid

        attributes = {}
        for category_element in soup.find(attrs={"class": "recordData"}).find_all(attrs={"class": "category"}):
            category_string = ''.join(category_element.stripped_strings).strip()
            display_element = category_element.parent.find(attrs={"class": "display"})
            if not display_element:
                continue
            display_string = ''.join(display_element.stripped_strings).replace("\\n", '').replace("\\'", "'").strip()
            if not category_string or not display_string:
                continue
            if category_string == "Object ID":
                assert result_builder.id is None
                result_builder.id = display_string
            else:
                assert category_string not in attributes
                attributes[category_string] = display_string
        result_builder.attributes = attributes

        related_photos_element = soup.find(attrs={"class": "relatedPhotos"})
        related_photos = []
        if related_photos_element:
            for td in related_photos_element.find_all("td"):
                related_photos.append(self.__parse_image(td.div))
        result_builder.related_photos = tuple(related_photos)

        return result_builder.build()

    def __parse_image(self, image_div_element):
        result_builder = OnlineDatabaseObjectDetailImage.Builder()

        for class_ in image_div_element["class"]:
            if class_ == "indvImage":
                result_builder.type = OnlineDatabaseObjectDetailImageType.INDIVIDUAL
                break
            elif class_ == "largeImage":
                result_builder.type = OnlineDatabaseObjectDetailImageType.LARGE
                break
            else:
                continue

        a = image_div_element.a

        result_builder.full_size_url = self.__strip_attr(a.attrs["href"])
        result_builder.src = self.__strip_attr(a.attrs["image_src"])
        result_builder.objectid = self.__strip_attr(a.attrs["objectid"])
        result_builder.mediaid = self.__strip_attr(a.attrs["mediaid"])
        result_builder.thumbnail_url = self.__strip_attr(a.figure.img.attrs["src"])
        result_builder.title = self.__strip_attr(a.attrs["linktitle"])

        return result_builder.build()

    def __strip_attr(self, value):
        old_value = value
        while True:
            for char in "'\\":
                new_value = old_value.strip(char)
                if new_value == old_value:
                    return new_value
                else:
                    old_value = new_value
