from datetime import datetime, date
import logging


class _DbfTable(object):
    def __init__(self, table):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.__table = table

    def _coerce_record_date_time_field(self, field_value):
        print('Coercing', field_value)
        if isinstance(field_value, str):
            for strptime_format in ('%m/%d/%Y', '%Y'):
                try:
                    return datetime.strptime(field_value, strptime_format)
                except ValueError:
                    pass
            self._logger.warn(
                "unable to parse %s (basestring)", field_value)
            return
        elif isinstance(field_value, int):
            if field_value == 0:
                return
        raise NotImplementedError(
            "%(field_name)s: %(field_value)s" % locals())

    def _coerce_record_field(
        self,
        field_metadata,
        field_value,
        existing_field_value=None
    ):
        field_name = field_metadata.name
        if field_metadata.type == date:
            if isinstance(field_value, date):
                return field_value
            date_time = self._coerce_record_date_time_field(
                field_value=field_value)
            if date_time is not None:
                return date_time.date()
        elif field_metadata.type == datetime:
            if isinstance(field_value, datetime):
                return field_value
            return self._coerce_record_date_time_field(
                field_value=field_value)
        elif field_metadata.type == str:
            if not isinstance(field_value, str):
                self._logger.debug("converting %s=%s (%s) to string",
                              field_name, field_value, type(field_value))
                return str(field_value)
            return field_value
        else:
            try:
                return field_metadata.type(field_value)
            except (TypeError, ValueError) as e:
                raise TypeError("unable to coerce %s=%s (%s) to a %s: %s" % (
                    field_name, field_value, type(field_value), field_metadata.type, e))

    def _map_record(self, record):
        raise NotImplementedError

    def _map_record_field(self, field_name, field_value, struct_builder, struct_type):
        if field_value is None:
            return
        elif isinstance(field_value, str):
            field_value = field_value.strip()
            if len(field_value) == 0:
                return

        field_metadata = getattr(
            getattr(struct_type, 'FieldMetadata'), field_name.upper())

        existing_field_value = getattr(struct_builder, field_name)

        new_field_value = \
            self._coerce_record_field(
                existing_field_value=existing_field_value,
                field_metadata=field_metadata,
                field_value=field_value,
            )
        if new_field_value is None:
            return

        try:
            getattr(struct_builder, 'set_' + field_name)(new_field_value)
        except TypeError as e:
            raise TypeError("%(new_field_value)s: %(e)s" % locals())
        except ValueError as e:
            if field_metadata.validation is not None:
                return
            raise ValueError("%(new_field_value)s: %(e)s" % locals())

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwds):
        self.__table.close()

    @property
    def field_names(self):
        return self.__table.field_names

    @classmethod
    def open(cls, dbf_file_path):
        if dbf_file_path.endswith('.dbf'):
            dbf_file_path = dbf_file_path[:-len('.dbf')]

        import dbf
        table = dbf.Table(dbf_file_path)
        table.open()
        return cls(table)

    def records(self):
        for record in self.__table:
            yield self._map_record(record)
        raise StopIteration

    def thrift_field_names(self):
        for field_name in self.field_names:
            yield "    // @validation {\"minLength\": 1}\n    optional string %s;\n" % field_name
