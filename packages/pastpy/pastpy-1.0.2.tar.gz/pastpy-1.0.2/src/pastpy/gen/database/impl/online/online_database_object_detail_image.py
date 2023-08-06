import builtins
import pastpy.gen.database.impl.online.online_database_object_detail_image_type
import pastpy.gen.non_blank_string


class OnlineDatabaseObjectDetailImage(object):
    class Builder(object):
        def __init__(
            self,
            full_size_url=None,
            mediaid=None,
            objectid=None,
            src=None,
            thumbnail_url=None,
            title=None,
            type=None,  # @ReservedAssignment
        ):
            '''
            :type full_size_url: str
            :type mediaid: str
            :type objectid: str
            :type src: str
            :type thumbnail_url: str
            :type title: str
            :type type: pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType
            '''

            self.__full_size_url = full_size_url
            self.__mediaid = mediaid
            self.__objectid = objectid
            self.__src = src
            self.__thumbnail_url = thumbnail_url
            self.__title = title
            self.__type = type

        def build(self):
            return OnlineDatabaseObjectDetailImage(full_size_url=self.__full_size_url, mediaid=self.__mediaid, objectid=self.__objectid, src=self.__src, thumbnail_url=self.__thumbnail_url, title=self.__title, type=self.__type)

        @classmethod
        def from_template(cls, template):
            '''
            :type template: pastpy.gen.database.impl.online.online_database_object_detail_image.OnlineDatabaseObjectDetailImage
            :rtype: pastpy.gen.database.impl.online.online_database_object_detail_image.OnlineDatabaseObjectDetailImage
            '''

            builder = cls()
            builder.full_size_url = template.full_size_url
            builder.mediaid = template.mediaid
            builder.objectid = template.objectid
            builder.src = template.src
            builder.thumbnail_url = template.thumbnail_url
            builder.title = template.title
            builder.type = template.type
            return builder

        @property
        def full_size_url(self):
            '''
            :rtype: str
            '''

            return self.__full_size_url

        @property
        def mediaid(self):
            '''
            :rtype: str
            '''

            return self.__mediaid

        @property
        def objectid(self):
            '''
            :rtype: str
            '''

            return self.__objectid

        def set_full_size_url(self, full_size_url):
            '''
            :type full_size_url: str
            '''

            if full_size_url is None:
                raise ValueError('full_size_url is required')
            if not isinstance(full_size_url, str):
                raise TypeError("expected full_size_url to be a str but it is a %s" % builtins.type(full_size_url))
            self.__full_size_url = full_size_url
            return self

        def set_mediaid(self, mediaid):
            '''
            :type mediaid: str
            '''

            if mediaid is None:
                raise ValueError('mediaid is required')
            if not isinstance(mediaid, str):
                raise TypeError("expected mediaid to be a str but it is a %s" % builtins.type(mediaid))
            self.__mediaid = mediaid
            return self

        def set_objectid(self, objectid):
            '''
            :type objectid: str
            '''

            if objectid is None:
                raise ValueError('objectid is required')
            if not isinstance(objectid, str):
                raise TypeError("expected objectid to be a str but it is a %s" % builtins.type(objectid))
            self.__objectid = objectid
            return self

        def set_src(self, src):
            '''
            :type src: str
            '''

            if src is None:
                raise ValueError('src is required')
            if not isinstance(src, str):
                raise TypeError("expected src to be a str but it is a %s" % builtins.type(src))
            self.__src = src
            return self

        def set_thumbnail_url(self, thumbnail_url):
            '''
            :type thumbnail_url: str
            '''

            if thumbnail_url is None:
                raise ValueError('thumbnail_url is required')
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

        def set_type(self, type):  # @ReservedAssignment
            '''
            :type type: pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType
            '''

            if type is None:
                raise ValueError('type is required')
            if not isinstance(type, pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType):
                raise TypeError("expected type to be a pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType but it is a %s" % builtins.type(type))
            self.__type = type
            return self

        @property
        def src(self):
            '''
            :rtype: str
            '''

            return self.__src

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

        @property
        def type(self):  # @ReservedAssignment
            '''
            :rtype: pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType
            '''

            return self.__type

        def update(self, online_database_object_detail_image):
            '''
            :type full_size_url: str
            :type mediaid: str
            :type objectid: str
            :type src: str
            :type thumbnail_url: str
            :type title: str
            :type type: pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType
            '''

            if isinstance(online_database_object_detail_image, OnlineDatabaseObjectDetailImage):
                self.set_full_size_url(online_database_object_detail_image.full_size_url)
                self.set_mediaid(online_database_object_detail_image.mediaid)
                self.set_objectid(online_database_object_detail_image.objectid)
                self.set_src(online_database_object_detail_image.src)
                self.set_thumbnail_url(online_database_object_detail_image.thumbnail_url)
                self.set_title(online_database_object_detail_image.title)
                self.set_type(online_database_object_detail_image.type)
            elif isinstance(online_database_object_detail_image, dict):
                for key, value in online_database_object_detail_image.items():
                    getattr(self, 'set_' + key)(value)
            else:
                raise TypeError(online_database_object_detail_image)
            return self

        @full_size_url.setter
        def full_size_url(self, full_size_url):
            '''
            :type full_size_url: str
            '''

            self.set_full_size_url(full_size_url)

        @mediaid.setter
        def mediaid(self, mediaid):
            '''
            :type mediaid: str
            '''

            self.set_mediaid(mediaid)

        @objectid.setter
        def objectid(self, objectid):
            '''
            :type objectid: str
            '''

            self.set_objectid(objectid)

        @src.setter
        def src(self, src):
            '''
            :type src: str
            '''

            self.set_src(src)

        @thumbnail_url.setter
        def thumbnail_url(self, thumbnail_url):
            '''
            :type thumbnail_url: str
            '''

            self.set_thumbnail_url(thumbnail_url)

        @title.setter
        def title(self, title):
            '''
            :type title: str
            '''

            self.set_title(title)

        @type.setter
        def type(self, type):  # @ReservedAssignment
            '''
            :type type: pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType
            '''

            self.set_type(type)

    class FieldMetadata(object):
        FULL_SIZE_URL = None
        MEDIAID = None
        OBJECTID = None
        SRC = None
        THUMBNAIL_URL = None
        TITLE = None
        TYPE = None

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
            return (cls.FULL_SIZE_URL, cls.MEDIAID, cls.OBJECTID, cls.SRC, cls.THUMBNAIL_URL, cls.TITLE, cls.TYPE,)

    FieldMetadata.FULL_SIZE_URL = FieldMetadata('full_size_url', str, None)
    FieldMetadata.MEDIAID = FieldMetadata('mediaid', pastpy.gen.non_blank_string.NonBlankString, None)
    FieldMetadata.OBJECTID = FieldMetadata('objectid', pastpy.gen.non_blank_string.NonBlankString, None)
    FieldMetadata.SRC = FieldMetadata('src', pastpy.gen.non_blank_string.NonBlankString, None)
    FieldMetadata.THUMBNAIL_URL = FieldMetadata('thumbnail_url', str, None)
    FieldMetadata.TITLE = FieldMetadata('title', pastpy.gen.non_blank_string.NonBlankString, None)
    FieldMetadata.TYPE = FieldMetadata('type', pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType, None)

    def __init__(
        self,
        full_size_url,
        mediaid,
        objectid,
        src,
        thumbnail_url,
        title,
        type,  # @ReservedAssignment
    ):
        '''
        :type full_size_url: str
        :type mediaid: str
        :type objectid: str
        :type src: str
        :type thumbnail_url: str
        :type title: str
        :type type: pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType
        '''

        if full_size_url is None:
            raise ValueError('full_size_url is required')
        if not isinstance(full_size_url, str):
            raise TypeError("expected full_size_url to be a str but it is a %s" % builtins.type(full_size_url))
        self.__full_size_url = full_size_url

        if mediaid is None:
            raise ValueError('mediaid is required')
        if not isinstance(mediaid, str):
            raise TypeError("expected mediaid to be a str but it is a %s" % builtins.type(mediaid))
        self.__mediaid = mediaid

        if objectid is None:
            raise ValueError('objectid is required')
        if not isinstance(objectid, str):
            raise TypeError("expected objectid to be a str but it is a %s" % builtins.type(objectid))
        self.__objectid = objectid

        if src is None:
            raise ValueError('src is required')
        if not isinstance(src, str):
            raise TypeError("expected src to be a str but it is a %s" % builtins.type(src))
        self.__src = src

        if thumbnail_url is None:
            raise ValueError('thumbnail_url is required')
        if not isinstance(thumbnail_url, str):
            raise TypeError("expected thumbnail_url to be a str but it is a %s" % builtins.type(thumbnail_url))
        self.__thumbnail_url = thumbnail_url

        if title is None:
            raise ValueError('title is required')
        if not isinstance(title, str):
            raise TypeError("expected title to be a str but it is a %s" % builtins.type(title))
        self.__title = title

        if type is None:
            raise ValueError('type is required')
        if not isinstance(type, pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType):
            raise TypeError("expected type to be a pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType but it is a %s" % builtins.type(type))
        self.__type = type

    def __eq__(self, other):
        if self.full_size_url != other.full_size_url:
            return False
        if self.mediaid != other.mediaid:
            return False
        if self.objectid != other.objectid:
            return False
        if self.src != other.src:
            return False
        if self.thumbnail_url != other.thumbnail_url:
            return False
        if self.title != other.title:
            return False
        if self.type != other.type:
            return False
        return True

    def __hash__(self):
        return hash((self.full_size_url, self.mediaid, self.objectid, self.src, self.thumbnail_url, self.title, self.type,))

    def __iter__(self):
        return iter((self.full_size_url, self.mediaid, self.objectid, self.src, self.thumbnail_url, self.title, self.type,))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        field_reprs = []
        field_reprs.append('full_size_url=' + "'" + self.full_size_url.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('mediaid=' + "'" + self.mediaid.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('objectid=' + "'" + self.objectid.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('src=' + "'" + self.src.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('thumbnail_url=' + "'" + self.thumbnail_url.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('title=' + "'" + self.title.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('type=' + repr(self.type))
        return 'OnlineDatabaseObjectDetailImage(' + ', '.join(field_reprs) + ')'

    def __str__(self):
        field_reprs = []
        field_reprs.append('full_size_url=' + "'" + self.full_size_url.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('mediaid=' + "'" + self.mediaid.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('objectid=' + "'" + self.objectid.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('src=' + "'" + self.src.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('thumbnail_url=' + "'" + self.thumbnail_url.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('title=' + "'" + self.title.encode('ascii', 'replace').decode('ascii') + "'")
        field_reprs.append('type=' + repr(self.type))
        return 'OnlineDatabaseObjectDetailImage(' + ', '.join(field_reprs) + ')'

    @classmethod
    def builder(cls):
        return cls.Builder()

    @classmethod
    def from_builtins(cls, _dict):
        if not isinstance(_dict, dict):
            raise ValueError("expected dict")

        __builder = cls.builder()

        full_size_url = _dict.get("full_size_url")
        if full_size_url is None:
            raise KeyError("full_size_url")
        __builder.full_size_url = full_size_url

        mediaid = _dict.get("mediaid")
        if mediaid is None:
            raise KeyError("mediaid")
        __builder.mediaid = mediaid

        objectid = _dict.get("objectid")
        if objectid is None:
            raise KeyError("objectid")
        __builder.objectid = objectid

        src = _dict.get("src")
        if src is None:
            raise KeyError("src")
        __builder.src = src

        thumbnail_url = _dict.get("thumbnail_url")
        if thumbnail_url is None:
            raise KeyError("thumbnail_url")
        __builder.thumbnail_url = thumbnail_url

        title = _dict.get("title")
        if title is None:
            raise KeyError("title")
        __builder.title = title

        type = _dict.get("type")
        if type is None:
            raise KeyError("type")
        type = pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType.value_of(type)
        __builder.type = type

        return __builder.build()

    @property
    def full_size_url(self):
        '''
        :rtype: str
        '''

        return self.__full_size_url

    @property
    def mediaid(self):
        '''
        :rtype: str
        '''

        return self.__mediaid

    @property
    def objectid(self):
        '''
        :rtype: str
        '''

        return self.__objectid

    @classmethod
    def read(cls, iprot):
        '''
        Read a new object from the given input protocol and return the object.

        :type iprot: thryft.protocol._input_protocol._InputProtocol
        :rtype: pastpy.gen.database.impl.online.online_database_object_detail_image.OnlineDatabaseObjectDetailImage
        '''

        init_kwds = {}

        iprot.read_struct_begin()
        while True:
            ifield_name, ifield_type, _ifield_id = iprot.read_field_begin()
            if ifield_type == 0:  # STOP
                break
            elif ifield_name == 'full_size_url':
                init_kwds['full_size_url'] = iprot.read_string()
            elif ifield_name == 'mediaid':
                init_kwds['mediaid'] = iprot.read_string()
            elif ifield_name == 'objectid':
                init_kwds['objectid'] = iprot.read_string()
            elif ifield_name == 'src':
                init_kwds['src'] = iprot.read_string()
            elif ifield_name == 'thumbnail_url':
                init_kwds['thumbnail_url'] = iprot.read_string()
            elif ifield_name == 'title':
                init_kwds['title'] = iprot.read_string()
            elif ifield_name == 'type':
                init_kwds['type'] = pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType.value_of(iprot.read_string().strip().upper())
            iprot.read_field_end()
        iprot.read_struct_end()

        return cls(**init_kwds)

    def replacer(self):
        return self.Builder.from_template(template=self)

    @property
    def src(self):
        '''
        :rtype: str
        '''

        return self.__src

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
        dict_["full_size_url"] = self.full_size_url
        dict_["mediaid"] = self.mediaid
        dict_["objectid"] = self.objectid
        dict_["src"] = self.src
        dict_["thumbnail_url"] = self.thumbnail_url
        dict_["title"] = self.title
        dict_["type"] = str(self.type)
        return dict_

    @property
    def type(self):  # @ReservedAssignment
        '''
        :rtype: pastpy.gen.database.impl.online.online_database_object_detail_image_type.OnlineDatabaseObjectDetailImageType
        '''

        return self.__type

    def write(self, oprot):
        '''
        Write this object to the given output protocol and return self.

        :type oprot: thryft.protocol._output_protocol._OutputProtocol
        :rtype: pastpy.gen.database.impl.online.online_database_object_detail_image.OnlineDatabaseObjectDetailImage
        '''

        oprot.write_struct_begin('OnlineDatabaseObjectDetailImage')

        oprot.write_field_begin(name='full_size_url', type=11, id=None)
        oprot.write_string(self.full_size_url)
        oprot.write_field_end()

        oprot.write_field_begin(name='mediaid', type=11, id=None)
        oprot.write_string(self.mediaid)
        oprot.write_field_end()

        oprot.write_field_begin(name='objectid', type=11, id=None)
        oprot.write_string(self.objectid)
        oprot.write_field_end()

        oprot.write_field_begin(name='src', type=11, id=None)
        oprot.write_string(self.src)
        oprot.write_field_end()

        oprot.write_field_begin(name='thumbnail_url', type=11, id=None)
        oprot.write_string(self.thumbnail_url)
        oprot.write_field_end()

        oprot.write_field_begin(name='title', type=11, id=None)
        oprot.write_string(self.title)
        oprot.write_field_end()

        oprot.write_field_begin(name='type', type=11, id=None)
        oprot.write_string(str(self.type))
        oprot.write_field_end()

        oprot.write_field_stop()

        oprot.write_struct_end()

        return self
