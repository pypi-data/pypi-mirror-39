import builtins
import pastpy.gen.non_blank_string


class OnlineDatabaseObjectsListItem(object):
    class Builder(object):
        def __init__(
            self,
            detail_href=None,
            record_type=None,
            title=None,
            thumbnail_url=None,
        ):
            '''
            :type detail_href: str
            :type record_type: str
            :type title: str
            :type thumbnail_url: str or None
            '''

            self.__detail_href = detail_href
            self.__record_type = record_type
            self.__title = title
            self.__thumbnail_url = thumbnail_url

        def build(self):
            return OnlineDatabaseObjectsListItem(detail_href=self.__detail_href, record_type=self.__record_type, title=self.__title, thumbnail_url=self.__thumbnail_url)

        @property
        def detail_href(self):
            '''
            :rtype: str
            '''

            return self.__detail_href

        @classmethod
        def from_template(cls, template):
            '''
            :type template: pastpy.gen.database.impl.online.online_database_objects_list_item.OnlineDatabaseObjectsListItem
            :rtype: pastpy.gen.database.impl.online.online_database_objects_list_item.OnlineDatabaseObjectsListItem
            '''

            builder = cls()
            builder.detail_href = template.detail_href
            builder.record_type = template.record_type
            builder.title = template.title
            builder.thumbnail_url = template.thumbnail_url
            return builder

        @property
        def record_type(self):
            '''
            :rtype: str
            '''

            return self.__record_type

        def set_detail_href(self, detail_href):
            '''
            :type detail_href: str
            '''

            if detail_href is None:
                raise ValueError('detail_href is required')
            if not isinstance(detail_href, str):
                raise TypeError("expected detail_href to be a str but it is a %s" % builtins.type(detail_href))
            self.__detail_href = detail_href
            return self

        def set_record_type(self, record_type):
            '''
            :type record_type: str
            '''

            if record_type is None:
                raise ValueError('record_type is required')
            if not isinstance(record_type, str):
                raise TypeError("expected record_type to be a str but it is a %s" % builtins.type(record_type))
            self.__record_type = record_type
            return self

        def set_thumbnail_url(self, thumbnail_url):
            '''
            :type thumbnail_url: str or None
            '''

            if thumbnail_url is not None:
                if not isinstance(thumbnail_url, str):
                    raise TypeError("expected thumbnail_url to be a str but it is a %s" % builtins.type(thumbnail_url))
            self.__thumbnail_url = thumbnail_url
            return self

        def set_title(self, title):
            '''
            :type title: str
            '''

            if title is None:
                raise ValueError('title is required')
            if not isinstance(title, str):
                raise TypeError("expected title to be a str but it is a %s" % builtins.type(title))
            self.__title = title
            return self

        @property
        def thumbnail_url(self):
            '''
            :rtype: str
            '''

            return self.__thumbnail_url

        @property
        def title(self):
            '''
            :rtype: str
            '''

            return self.__title

        def update(self, online_database_objects_list_item):
            '''
            :type detail_href: str
            :type record_type: str
            :type title: str
            :type thumbnail_url: str or None
            '''

            if isinstance(online_database_objects_list_item, OnlineDatabaseObjectsListItem):
                self.set_detail_href(online_database_objects_list_item.detail_href)
                self.set_record_type(online_database_objects_list_item.record_type)
                self.set_title(online_database_objects_list_item.title)
                self.set_thumbnail_url(online_database_objects_list_item.thumbnail_url)
            elif isinstance(online_database_objects_list_item, dict):
                for key, value in online_database_objects_list_item.items():
                    getattr(self, 'set_' + key)(value)
            else:
                raise TypeError(online_database_objects_list_item)
            return self

        @detail_href.setter
        def detail_href(self, detail_href):
            '''
            :type detail_href: str
            '''

            self.set_detail_href(detail_href)

        @record_type.setter
        def record_type(self, record_type):
            '''
            :type record_type: str
            '''

            self.set_record_type(record_type)

        @thumbnail_url.setter
        def thumbnail_url(self, thumbnail_url):
            '''
            :type thumbnail_url: str or None
            '''

            self.set_thumbnail_url(thumbnail_url)

        @title.setter
        def title(self, title):
            '''
            :type title: str
            '''

            self.set_title(title)

    class FieldMetadata(object):
        DETAIL_HREF = None
        RECORD_TYPE = None
        TITLE = None
        THUMBNAIL_URL = None

        def __init__(self, name, type_, validation):
            object.__init__(self)
            self.__name = name
            self.__type = type_
            self.__validation = validation

        @property
        def name(self):
            return self.__name

        def __repr__(self):
            return self.__name

        def __str__(self):
            return self.__name

        @property
        def type(self):
            return self.__type

        @property
        def validation(self):
            return self.__validation

        @classmethod
        def values(cls):
            return (cls.DETAIL_HREF, cls.RECORD_TYPE, cls.TITLE, cls.THUMBNAIL_URL,)

    FieldMetadata.DETAIL_HREF = FieldMetadata('detail_href', pastpy.gen.non_blank_string.NonBlankString, None)
    FieldMetadata.RECORD_TYPE = FieldMetadata('record_type', pastpy.gen.non_blank_string.NonBlankString, None)
    FieldMetadata.TITLE = FieldMetadata('title', pastpy.gen.non_blank_string.NonBlankString, None)
    FieldMetadata.THUMBNAIL_URL = FieldMetadata('thumbnail_url', str, None)

    def __init__(
        self,
        detail_href,
        record_type,
        title,
        thumbnail_url=None,
    ):
        '''
        :type detail_href: str
        :type record_type: str
        :type title: str
        :type thumbnail_url: str or None
        '''

        if detail_href is None:
            raise ValueError('detail_href is required')
        if not isinstance(detail_href, str):
            raise TypeError("expected detail_href to be a str but it is a %s" % builtins.type(detail_href))
        self.__detail_href = detail_href

        if record_type is None:
            raise ValueError('record_type is required')
        if not isinstance(record_type, str):
            raise TypeError("expected record_type to be a str but it is a %s" % builtins.type(record_type))
        self.__record_type = record_type

        if title is None:
            raise ValueError('title is required')
        if not isinstance(title, str):
            raise TypeError("expected title to be a str but it is a %s" % builtins.type(title))
        self.__title = title

        if thumbnail_url is not None:
            if not isinstance(thumbnail_url, str):
                raise TypeError("expected thumbnail_url to be a str but it is a %s" % builtins.type(thumbnail_url))
        self.__thumbnail_url = thumbnail_url

    def __eq__(self, other):
        if self.detail_href != other.detail_href:
            return False
        if self.record_type != other.record_type:
            return False
        if self.title != other.title:
            return False
        if self.thumbnail_url != other.thumbnail_url:
            return False
        return True

    def __hash__(self):
        return hash((self.detail_href, self.record_type, self.title, self.thumbnail_url,))

    def __iter__(self):
        return iter((self.detail_href, self.record_type, self.title, self.thumbnail_url,))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        field_reprs = []
        field_reprs.append('detail_href=' + "'" + self.detail_href.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('record_type=' + "'" + self.record_type.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('title=' + "'" + self.title.encode('ascii', 'replace').decode('ascii') + "'")
        if self.thumbnail_url is not None:
            field_reprs.append('thumbnail_url=' + "'" + self.thumbnail_url.encode('ascii', 'replace').decode('ascii') + "'")
        return 'OnlineDatabaseObjectsListItem(' + ', '.join(field_reprs) + ')'

    def __str__(self):
        field_reprs = []
        field_reprs.append('detail_href=' + "'" + self.detail_href.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('record_type=' + "'" + self.record_type.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('title=' + "'" + self.title.encode('ascii', 'replace').decode('ascii') + "'")
        if self.thumbnail_url is not None:
            field_reprs.append('thumbnail_url=' + "'" + self.thumbnail_url.encode('ascii', 'replace').decode('ascii') + "'")
        return 'OnlineDatabaseObjectsListItem(' + ', '.join(field_reprs) + ')'

    @classmethod
    def builder(cls):
        return cls.Builder()

    @property
    def detail_href(self):
        '''
        :rtype: str
        '''

        return self.__detail_href

    @classmethod
    def from_builtins(cls, _dict):
        if not isinstance(_dict, dict):
            raise ValueError("expected dict")

        __builder = cls.builder()

        detail_href = _dict.get("detail_href")
        if detail_href is None:
            raise KeyError("detail_href")
        __builder.detail_href = detail_href

        record_type = _dict.get("record_type")
        if record_type is None:
            raise KeyError("record_type")
        __builder.record_type = record_type

        title = _dict.get("title")
        if title is None:
            raise KeyError("title")
        __builder.title = title

        __builder.thumbnail_url = _dict.get("thumbnail_url")

        return __builder.build()

    @classmethod
    def read(cls, iprot):
        '''
        Read a new object from the given input protocol and return the object.

        :type iprot: thryft.protocol._input_protocol._InputProtocol
        :rtype: pastpy.gen.database.impl.online.online_database_objects_list_item.OnlineDatabaseObjectsListItem
        '''

        init_kwds = {}

        iprot.read_struct_begin()
        while True:
            ifield_name, ifield_type, _ifield_id = iprot.read_field_begin()
            if ifield_type == 0:  # STOP
                break
            elif ifield_name == 'detail_href':
                init_kwds['detail_href'] = iprot.read_string()
            elif ifield_name == 'record_type':
                init_kwds['record_type'] = iprot.read_string()
            elif ifield_name == 'title':
                init_kwds['title'] = iprot.read_string()
            elif ifield_name == 'thumbnail_url':
                try:
                    init_kwds['thumbnail_url'] = iprot.read_string()
                except (TypeError, ValueError,):
                    pass
            iprot.read_field_end()
        iprot.read_struct_end()

        return cls(**init_kwds)

    @property
    def record_type(self):
        '''
        :rtype: str
        '''

        return self.__record_type

    def replacer(self):
        return self.Builder.from_template(template=self)

    @property
    def thumbnail_url(self):
        '''
        :rtype: str
        '''

        return self.__thumbnail_url

    @property
    def title(self):
        '''
        :rtype: str
        '''

        return self.__title

    def to_builtins(self):
        dict_ = {}
        dict_["detail_href"] = self.detail_href
        dict_["record_type"] = self.record_type
        dict_["title"] = self.title
        dict_["thumbnail_url"] = self.thumbnail_url
        return dict_

    def write(self, oprot):
        '''
        Write this object to the given output protocol and return self.

        :type oprot: thryft.protocol._output_protocol._OutputProtocol
        :rtype: pastpy.gen.database.impl.online.online_database_objects_list_item.OnlineDatabaseObjectsListItem
        '''

        oprot.write_struct_begin('OnlineDatabaseObjectsListItem')

        oprot.write_field_begin(name='detail_href', type=11, id=None)
        oprot.write_string(self.detail_href)
        oprot.write_field_end()

        oprot.write_field_begin(name='record_type', type=11, id=None)
        oprot.write_string(self.record_type)
        oprot.write_field_end()

        oprot.write_field_begin(name='title', type=11, id=None)
        oprot.write_string(self.title)
        oprot.write_field_end()

        if self.thumbnail_url is not None:
            oprot.write_field_begin(name='thumbnail_url', type=11, id=None)
            oprot.write_string(self.thumbnail_url)
            oprot.write_field_end()

        oprot.write_field_stop()

        oprot.write_struct_end()

        return self
