import builtins
import pastpy.gen.non_blank_string


class DbfDatabaseConfiguration(object):
    class Builder(object):
        def __init__(
            self,
            pp_images_dir_path=None,
            pp_install_dir_path=None,
            pp_objects_dbf_file_path=None,
        ):
            '''
            :type pp_images_dir_path: str or None
            :type pp_install_dir_path: str or None
            :type pp_objects_dbf_file_path: str or None
            '''

            self.__pp_images_dir_path = pp_images_dir_path
            self.__pp_install_dir_path = pp_install_dir_path
            self.__pp_objects_dbf_file_path = pp_objects_dbf_file_path

        def build(self):
            return DbfDatabaseConfiguration(pp_images_dir_path=self.__pp_images_dir_path, pp_install_dir_path=self.__pp_install_dir_path, pp_objects_dbf_file_path=self.__pp_objects_dbf_file_path)

        @classmethod
        def from_template(cls, template):
            '''
            :type template: pastpy.gen.database.impl.dbf.dbf_database_configuration.DbfDatabaseConfiguration
            :rtype: pastpy.gen.database.impl.dbf.dbf_database_configuration.DbfDatabaseConfiguration
            '''

            builder = cls()
            builder.pp_images_dir_path = template.pp_images_dir_path
            builder.pp_install_dir_path = template.pp_install_dir_path
            builder.pp_objects_dbf_file_path = template.pp_objects_dbf_file_path
            return builder

        @property
        def pp_images_dir_path(self):
            '''
            :rtype: str
            '''

            return self.__pp_images_dir_path

        @property
        def pp_install_dir_path(self):
            '''
            :rtype: str
            '''

            return self.__pp_install_dir_path

        @property
        def pp_objects_dbf_file_path(self):
            '''
            :rtype: str
            '''

            return self.__pp_objects_dbf_file_path

        def set_pp_images_dir_path(self, pp_images_dir_path):
            '''
            :type pp_images_dir_path: str or None
            '''

            if pp_images_dir_path is not None:
                if not isinstance(pp_images_dir_path, str):
                    raise TypeError("expected pp_images_dir_path to be a str but it is a %s" % builtins.type(pp_images_dir_path))
            self.__pp_images_dir_path = pp_images_dir_path
            return self

        def set_pp_install_dir_path(self, pp_install_dir_path):
            '''
            :type pp_install_dir_path: str or None
            '''

            if pp_install_dir_path is not None:
                if not isinstance(pp_install_dir_path, str):
                    raise TypeError("expected pp_install_dir_path to be a str but it is a %s" % builtins.type(pp_install_dir_path))
            self.__pp_install_dir_path = pp_install_dir_path
            return self

        def set_pp_objects_dbf_file_path(self, pp_objects_dbf_file_path):
            '''
            :type pp_objects_dbf_file_path: str or None
            '''

            if pp_objects_dbf_file_path is not None:
                if not isinstance(pp_objects_dbf_file_path, str):
                    raise TypeError("expected pp_objects_dbf_file_path to be a str but it is a %s" % builtins.type(pp_objects_dbf_file_path))
            self.__pp_objects_dbf_file_path = pp_objects_dbf_file_path
            return self

        def update(self, dbf_database_configuration):
            '''
            :type pp_images_dir_path: str or None
            :type pp_install_dir_path: str or None
            :type pp_objects_dbf_file_path: str or None
            '''

            if isinstance(dbf_database_configuration, DbfDatabaseConfiguration):
                self.set_pp_images_dir_path(dbf_database_configuration.pp_images_dir_path)
                self.set_pp_install_dir_path(dbf_database_configuration.pp_install_dir_path)
                self.set_pp_objects_dbf_file_path(dbf_database_configuration.pp_objects_dbf_file_path)
            elif isinstance(dbf_database_configuration, dict):
                for key, value in dbf_database_configuration.items():
                    getattr(self, 'set_' + key)(value)
            else:
                raise TypeError(dbf_database_configuration)
            return self

        @pp_images_dir_path.setter
        def pp_images_dir_path(self, pp_images_dir_path):
            '''
            :type pp_images_dir_path: str or None
            '''

            self.set_pp_images_dir_path(pp_images_dir_path)

        @pp_install_dir_path.setter
        def pp_install_dir_path(self, pp_install_dir_path):
            '''
            :type pp_install_dir_path: str or None
            '''

            self.set_pp_install_dir_path(pp_install_dir_path)

        @pp_objects_dbf_file_path.setter
        def pp_objects_dbf_file_path(self, pp_objects_dbf_file_path):
            '''
            :type pp_objects_dbf_file_path: str or None
            '''

            self.set_pp_objects_dbf_file_path(pp_objects_dbf_file_path)

    class FieldMetadata(object):
        PP_IMAGES_DIR_PATH = None
        PP_INSTALL_DIR_PATH = None
        PP_OBJECTS_DBF_FILE_PATH = None

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
            return (cls.PP_IMAGES_DIR_PATH, cls.PP_INSTALL_DIR_PATH, cls.PP_OBJECTS_DBF_FILE_PATH,)

    FieldMetadata.PP_IMAGES_DIR_PATH = FieldMetadata('pp_images_dir_path', pastpy.gen.non_blank_string.NonBlankString, None)
    FieldMetadata.PP_INSTALL_DIR_PATH = FieldMetadata('pp_install_dir_path', pastpy.gen.non_blank_string.NonBlankString, None)
    FieldMetadata.PP_OBJECTS_DBF_FILE_PATH = FieldMetadata('pp_objects_dbf_file_path', pastpy.gen.non_blank_string.NonBlankString, None)

    def __init__(
        self,
        pp_images_dir_path=None,
        pp_install_dir_path=None,
        pp_objects_dbf_file_path=None,
    ):
        '''
        :type pp_images_dir_path: str or None
        :type pp_install_dir_path: str or None
        :type pp_objects_dbf_file_path: str or None
        '''

        if pp_images_dir_path is not None:
            if not isinstance(pp_images_dir_path, str):
                raise TypeError("expected pp_images_dir_path to be a str but it is a %s" % builtins.type(pp_images_dir_path))
        self.__pp_images_dir_path = pp_images_dir_path

        if pp_install_dir_path is not None:
            if not isinstance(pp_install_dir_path, str):
                raise TypeError("expected pp_install_dir_path to be a str but it is a %s" % builtins.type(pp_install_dir_path))
        self.__pp_install_dir_path = pp_install_dir_path

        if pp_objects_dbf_file_path is not None:
            if not isinstance(pp_objects_dbf_file_path, str):
                raise TypeError("expected pp_objects_dbf_file_path to be a str but it is a %s" % builtins.type(pp_objects_dbf_file_path))
        self.__pp_objects_dbf_file_path = pp_objects_dbf_file_path

    def __eq__(self, other):
        if self.pp_images_dir_path != other.pp_images_dir_path:
            return False
        if self.pp_install_dir_path != other.pp_install_dir_path:
            return False
        if self.pp_objects_dbf_file_path != other.pp_objects_dbf_file_path:
            return False
        return True

    def __hash__(self):
        return hash((self.pp_images_dir_path, self.pp_install_dir_path, self.pp_objects_dbf_file_path,))

    def __iter__(self):
        return iter((self.pp_images_dir_path, self.pp_install_dir_path, self.pp_objects_dbf_file_path,))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        field_reprs = []
        if self.pp_images_dir_path is not None:
            field_reprs.append('pp_images_dir_path=' + "'" + self.pp_images_dir_path.encode('ascii', 'replace').decode('ascii') + "'")
        if self.pp_install_dir_path is not None:
            field_reprs.append('pp_install_dir_path=' + "'" + self.pp_install_dir_path.encode('ascii', 'replace').decode('ascii') + "'")
        if self.pp_objects_dbf_file_path is not None:
            field_reprs.append('pp_objects_dbf_file_path=' + "'" + self.pp_objects_dbf_file_path.encode('ascii', 'replace').decode('ascii') + "'")
        return 'DbfDatabaseConfiguration(' + ', '.join(field_reprs) + ')'

    def __str__(self):
        field_reprs = []
        if self.pp_images_dir_path is not None:
            field_reprs.append('pp_images_dir_path=' + "'" + self.pp_images_dir_path.encode('ascii', 'replace').decode('ascii') + "'")
        if self.pp_install_dir_path is not None:
            field_reprs.append('pp_install_dir_path=' + "'" + self.pp_install_dir_path.encode('ascii', 'replace').decode('ascii') + "'")
        if self.pp_objects_dbf_file_path is not None:
            field_reprs.append('pp_objects_dbf_file_path=' + "'" + self.pp_objects_dbf_file_path.encode('ascii', 'replace').decode('ascii') + "'")
        return 'DbfDatabaseConfiguration(' + ', '.join(field_reprs) + ')'

    @classmethod
    def builder(cls):
        return cls.Builder()

    @classmethod
    def from_builtins(cls, _dict):
        if not isinstance(_dict, dict):
            raise ValueError("expected dict")

        __builder = cls.builder()

        __builder.pp_images_dir_path = _dict.get("pp_images_dir_path")

        __builder.pp_install_dir_path = _dict.get("pp_install_dir_path")

        __builder.pp_objects_dbf_file_path = _dict.get("pp_objects_dbf_file_path")

        return __builder.build()

    @property
    def pp_images_dir_path(self):
        '''
        :rtype: str
        '''

        return self.__pp_images_dir_path

    @property
    def pp_install_dir_path(self):
        '''
        :rtype: str
        '''

        return self.__pp_install_dir_path

    @property
    def pp_objects_dbf_file_path(self):
        '''
        :rtype: str
        '''

        return self.__pp_objects_dbf_file_path

    @classmethod
    def read(cls, iprot):
        '''
        Read a new object from the given input protocol and return the object.

        :type iprot: thryft.protocol._input_protocol._InputProtocol
        :rtype: pastpy.gen.database.impl.dbf.dbf_database_configuration.DbfDatabaseConfiguration
        '''

        init_kwds = {}

        iprot.read_struct_begin()
        while True:
            ifield_name, ifield_type, _ifield_id = iprot.read_field_begin()
            if ifield_type == 0:  # STOP
                break
            elif ifield_name == 'pp_images_dir_path':
                try:
                    init_kwds['pp_images_dir_path'] = iprot.read_string()
                except (TypeError, ValueError,):
                    pass
            elif ifield_name == 'pp_install_dir_path':
                try:
                    init_kwds['pp_install_dir_path'] = iprot.read_string()
                except (TypeError, ValueError,):
                    pass
            elif ifield_name == 'pp_objects_dbf_file_path':
                try:
                    init_kwds['pp_objects_dbf_file_path'] = iprot.read_string()
                except (TypeError, ValueError,):
                    pass
            iprot.read_field_end()
        iprot.read_struct_end()

        return cls(**init_kwds)

    def replacer(self):
        return self.Builder.from_template(template=self)

    def to_builtins(self):
        dict_ = {}
        dict_["pp_images_dir_path"] = self.pp_images_dir_path
        dict_["pp_install_dir_path"] = self.pp_install_dir_path
        dict_["pp_objects_dbf_file_path"] = self.pp_objects_dbf_file_path
        return dict_

    def write(self, oprot):
        '''
        Write this object to the given output protocol and return self.

        :type oprot: thryft.protocol._output_protocol._OutputProtocol
        :rtype: pastpy.gen.database.impl.dbf.dbf_database_configuration.DbfDatabaseConfiguration
        '''

        oprot.write_struct_begin('DbfDatabaseConfiguration')

        if self.pp_images_dir_path is not None:
            oprot.write_field_begin(name='pp_images_dir_path', type=11, id=None)
            oprot.write_string(self.pp_images_dir_path)
            oprot.write_field_end()

        if self.pp_install_dir_path is not None:
            oprot.write_field_begin(name='pp_install_dir_path', type=11, id=None)
            oprot.write_string(self.pp_install_dir_path)
            oprot.write_field_end()

        if self.pp_objects_dbf_file_path is not None:
            oprot.write_field_begin(name='pp_objects_dbf_file_path', type=11, id=None)
            oprot.write_string(self.pp_objects_dbf_file_path)
            oprot.write_field_end()

        oprot.write_field_stop()

        oprot.write_struct_end()

        return self
