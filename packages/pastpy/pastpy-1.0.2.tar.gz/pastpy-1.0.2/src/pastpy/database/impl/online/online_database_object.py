from pastpy.database.database_object import DatabaseObject
from pastpy.database.impl.online.online_database_image import OnlineDatabaseImage


class OnlineDatabaseObject(DatabaseObject):
    def __init__(self, *, detail, list_item):
        self.__detail = detail
        self.__list_item = list_item

    @property
    def date(self):
        return self.__detail.attributes.get("Date")

    @property
    def description(self):
        return self.__detail.attributes.get("Description")

    @property
    def id(self):
        return self.__detail.id

    @property
    def images(self):
        images = []
        if self.__list_item.thumbnail_url:
            images.append(OnlineDatabaseImage(list_item=self.__list_item))
        if self.__detail.related_photos:
            for detail_image in self.__detail.related_photos:
                images.append(OnlineDatabaseImage(detail_image=detail_image))
        return tuple(images)

    @property
    def impl_attributes(self):
        return self.__detail.attributes

    @property
    def name(self):
        return self.__detail.attributes.get("Object Name")

    @property
    def othername(self):
        return self.__detail.attributes.get("Other Name")

    @property
    def title(self):
        return self.__detail.attributes.get("Title")
