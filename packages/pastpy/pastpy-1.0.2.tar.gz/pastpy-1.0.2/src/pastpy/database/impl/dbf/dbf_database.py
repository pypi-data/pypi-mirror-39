import os.path
from pastpy.database.database import Database
from pastpy.database.impl.dbf.objects_dbf_table import ObjectsDbfTable
from pastpy.database.impl.dbf.dbf_database_object import DbfDatabaseObject
from pastpy.gen.database.impl.dbf.dbf_database_configuration import DbfDatabaseConfiguration


class DbfDatabase(Database):
    def __init__(self, *, configuration):
        Database.__init__(self)
        assert isinstance(configuration, DbfDatabaseConfiguration)

        configuration_builder = configuration.replacer()
        if configuration.pp_images_dir_path is not None and configuration.pp_objects_dbf_file_path is not None:
            self.__configuration = configuration_builder.build()
            return

        pp_install_dir_path = configuration.pp_install_dir_path
        if pp_install_dir_path is None:
            pp_install_dir_path = "C:\\pp5"

        if not os.path.isdir(pp_install_dir_path):
            raise ValueError(
                "PastPerfect installation directory %s does not exist" % pp_install_dir_path)
        if configuration.pp_images_dir_path is None:
            configuration_builder.pp_images_dir_path = os.path.join(
                pp_install_dir_path, 'Images')
        if configuration.pp_objects_dbf_file_path is None:
            configuration_builder.pp_objects_dbf_file_path = os.path.join(
                pp_install_dir_path, 'Data', 'OBJECTS.DBF')

        configuration = configuration_builder.build()

        if not os.path.isdir(configuration.pp_images_dir_path):
            raise ValueError(
                "PastPerfect images directory %s does not exist" % configuration.pp_images_dir_path)
        if not os.path.isfile(configuration.pp_objects_dbf_file_path):
            raise ValueError(
                "PastPerfect objects DBF file %s does not exist" % configuration.pp_objects_dbf_file_path)

        self.__configuration = configuration

    def objects(self):
        with ObjectsDbfTable.open(self.__configuration.pp_objects_dbf_file_path) as table:
            for record in table.records():
                yield DbfDatabaseObject(images_dir_path=self.__configuration.pp_images_dir_path, record=record)
