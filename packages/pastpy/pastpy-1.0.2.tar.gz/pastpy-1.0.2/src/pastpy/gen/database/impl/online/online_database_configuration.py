import builtins
import pastpy.gen.non_blank_string


class OnlineDatabaseConfiguration(object):
    class Builder(object):
        def __init__(
            self,
            collection_name=None,
            download_dir_path=None,
        ):
            '''
            :type collection_name: str
            :type download_dir_path: str or None
            '''

            self.__collection_name = collection_name
            self.__download_dir_path = download_dir_path

        def build(self):
            return OnlineDatabaseConfiguration(collection_name=self.__collection_name, download_dir_path=self.__download_dir_path)

        @property
        def collection_name(self):
            '''
            :rtype: str
            '''

            return self.__collection_name

        @property
        def download_dir_path(self):
            '''
            :rtype: str
            '''

            return self.__download_dir_path

        @classmethod
        def from_template(cls, template):
            '''
            :type template: pastpy.gen.database.impl.online.online_database_configuration.OnlineDatabaseConfiguration
            :rtype: pastpy.gen.database.impl.online.online_database_configuration.OnlineDatabaseConfiguration
            '''

            builder = cls()
            builder.collection_name = template.collection_name
            builder.download_dir_path = template.download_dir_path
            return builder

        def set_collection_name(self, collection_name):
            '''
            :type collection_name: str
            '''

            if collection_name is None:
                raise ValueError('collection_name is required')
            if not isinstance(collection_name, str):
                raise TypeError("expected collection_name to be a str but it is a %s" % builtins.type(collection_name))
            self.__collection_name = collection_name
            return self

        def set_download_dir_path(self, download_dir_path):
            '''
            :type download_dir_path: str or None
            '''

            if download_dir_path is not None:
                if not isinstance(download_dir_path, str):
                    raise TypeError("expected download_dir_path to be a str but it is a %s" % builtins.type(download_dir_path))
            self.__download_dir_path = download_dir_path
            return self

        def update(self, online_database_configuration):
            '''
            :type collection_name: str
            :type download_dir_path: str or None
            '''

            if isinstance(online_database_configuration, OnlineDatabaseConfiguration):
                self.set_collection_name(online_database_configuration.collection_name)
                self.set_download_dir_path(online_database_configuration.download_dir_path)
            elif isinstance(online_database_configuration, dict):
                for key, value in online_database_configuration.items():
                    getattr(self, 'set_' + key)(value)
            else:
                raise TypeError(online_database_configuration)
            return self

        @collection_name.setter
        def collection_name(self, collection_name):
            '''
            :type collection_name: str
            '''

            self.set_collection_name(collection_name)

        @download_dir_path.setter
        def download_dir_path(self, download_dir_path):
            '''
            :type download_dir_path: str or None
            '''

            self.set_download_dir_path(download_dir_path)

    class FieldMetadata(object):
        COLLECTION_NAME = None
        DOWNLOAD_DIR_PATH = None

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
            return (cls.COLLECTION_NAME, cls.DOWNLOAD_DIR_PATH,)

    FieldMetadata.COLLECTION_NAME = FieldMetadata('collection_name', pastpy.gen.non_blank_string.NonBlankString, None)
    FieldMetadata.DOWNLOAD_DIR_PATH = FieldMetadata('download_dir_path', pastpy.gen.non_blank_string.NonBlankString, None)

    def __init__(
        self,
        collection_name,
        download_dir_path=None,
    ):
        '''
        :type collection_name: str
        :type download_dir_path: str or None
        '''

        if collection_name is None:
            raise ValueError('collection_name is required')
        if not isinstance(collection_name, str):
            raise TypeError("expected collection_name to be a str but it is a %s" % builtins.type(collection_name))
        self.__collection_name = collection_name

        if download_dir_path is not None:
            if not isinstance(download_dir_path, str):
                raise TypeError("expected download_dir_path to be a str but it is a %s" % builtins.type(download_dir_path))
        self.__download_dir_path = download_dir_path

    def __eq__(self, other):
        if self.collection_name != other.collection_name:
            return False
        if self.download_dir_path != other.download_dir_path:
            return False
        return True

    def __hash__(self):
        return hash((self.collection_name, self.download_dir_path,))

    def __iter__(self):
        return iter((self.collection_name, self.download_dir_path,))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        field_reprs = []
        field_reprs.append('collection_name=' + "'" + self.collection_name.encode('ascii', 'replace').decode('ascii') + "'")
        if self.download_dir_path is not None:
            field_reprs.append('download_dir_path=' + "'" + self.download_dir_path.encode('ascii', 'replace').decode('ascii') + "'")
        return 'OnlineDatabaseConfiguration(' + ', '.join(field_reprs) + ')'

    def __str__(self):
        field_reprs = []
        field_reprs.append('collection_name=' + "'" + self.collection_name.encode('ascii', 'replace').decode('ascii') + "'")
        if self.download_dir_path is not None:
            field_reprs.append('download_dir_path=' + "'" + self.download_dir_path.encode('ascii', 'replace').decode('ascii') + "'")
        return 'OnlineDatabaseConfiguration(' + ', '.join(field_reprs) + ')'

    @classmethod
    def builder(cls):
        return cls.Builder()

    @property
    def collection_name(self):
        '''
        :rtype: str
        '''

        return self.__collection_name

    @property
    def download_dir_path(self):
        '''
        :rtype: str
        '''

        return self.__download_dir_path

    @classmethod
    def from_builtins(cls, _dict):
        if not isinstance(_dict, dict):
            raise ValueError("expected dict")

        __builder = cls.builder()

        collection_name = _dict.get("collection_name")
        if collection_name is None:
            raise KeyError("collection_name")
        __builder.collection_name = collection_name

        __builder.download_dir_path = _dict.get("download_dir_path")

        return __builder.build()

    @classmethod
    def read(cls, iprot):
        '''
        Read a new object from the given input protocol and return the object.

        :type iprot: thryft.protocol._input_protocol._InputProtocol
        :rtype: pastpy.gen.database.impl.online.online_database_configuration.OnlineDatabaseConfiguration
        '''

        init_kwds = {}

        iprot.read_struct_begin()
        while True:
            ifield_name, ifield_type, _ifield_id = iprot.read_field_begin()
            if ifield_type == 0:  # STOP
                break
            elif ifield_name == 'collection_name':
                init_kwds['collection_name'] = iprot.read_string()
            elif ifield_name == 'download_dir_path':
                try:
                    init_kwds['download_dir_path'] = iprot.read_string()
                except (TypeError, ValueError,):
                    pass
            iprot.read_field_end()
        iprot.read_struct_end()

        return cls(**init_kwds)

    def replacer(self):
        return self.Builder.from_template(template=self)

    def to_builtins(self):
        dict_ = {}
        dict_["collection_name"] = self.collection_name
        dict_["download_dir_path"] = self.download_dir_path
        return dict_

    def write(self, oprot):
        '''
        Write this object to the given output protocol and return self.

        :type oprot: thryft.protocol._output_protocol._OutputProtocol
        :rtype: pastpy.gen.database.impl.online.online_database_configuration.OnlineDatabaseConfiguration
        '''

        oprot.write_struct_begin('OnlineDatabaseConfiguration')

        oprot.write_field_begin(name='collection_name', type=11, id=None)
        oprot.write_string(self.collection_name)
        oprot.write_field_end()

        if self.download_dir_path is not None:
            oprot.write_field_begin(name='download_dir_path', type=11, id=None)
            oprot.write_string(self.download_dir_path)
            oprot.write_field_end()

        oprot.write_field_stop()

        oprot.write_struct_end()

        return self
