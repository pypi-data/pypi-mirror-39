from pastpy.database.impl.dbf._dbf_table import _DbfTable
from pastpy.gen.database.impl.dbf.objects_dbf_record import ObjectsDbfRecord


class ObjectsDbfTable(_DbfTable):
    def _map_record(self, record):
        object_record_builder = ObjectsDbfRecord.Builder()
        for field_name in self.field_names:
            self._map_record_field(
                field_name=field_name,
                field_value=record[field_name],
                struct_builder=object_record_builder,
                struct_type=ObjectsDbfRecord
            )
        return object_record_builder.build()
