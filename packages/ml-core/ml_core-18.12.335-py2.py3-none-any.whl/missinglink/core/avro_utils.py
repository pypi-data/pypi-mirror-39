# -*- coding: utf8 -*-
import json
import six
from missinglink.core.json_utils import clean_system_keys, get_json_items


class AvroWriter(object):
    def __init__(self, write_to=None, key_name=None):
        self.__key_name = key_name
        self.__write_to = write_to or six.BytesIO()
        self.__writer = None

    @property
    def stream(self):
        return self.__write_to

    @classmethod
    def __get_schema_from_item(cls, schema_so_far, item):
        type_convert = {'str': 'string', 'bool': 'boolean', 'unicode': 'string', 'int': 'long'}

        has_nulls = False
        for key, val in item.items():
            if key in schema_so_far:
                continue

            if val is None:
                has_nulls = True
                continue

            t = type(val).__name__
            t = type_convert.get(t, t)
            schema_so_far[key] = t

        return has_nulls

    @classmethod
    def __create_schema_for_fields(cls, schema_fields):
        import avro

        schema_data = {
            "namespace": "ml.data",
            "type": "record",
            "name": "Data",
            "fields": [],
        }

        for key, t in schema_fields.items():
            field_data = {'name': key, 'type': [t, 'null']}
            schema_data['fields'].append(field_data)

        parse_method = getattr(avro.schema, 'parse', None) or getattr(avro.schema, 'Parse')
        data = json.dumps(schema_data)
        return parse_method(data)

    def close(self):
        if self.__writer is None:
            return

        self.__writer.flush()

    def append_data(self, data):
        from avro.datafile import DataFileWriter
        from avro.io import DatumWriter

        schema_so_far = {}
        for i, item in enumerate(get_json_items(data, key_name=self.__key_name)):
            has_null = self.__get_schema_from_item(schema_so_far, item)

            if not has_null:
                break

        avro_schema = self.__create_schema_for_fields(schema_so_far)

        for i, item in enumerate(get_json_items(data, key_name=self.__key_name)):
            item = clean_system_keys(item)

            if self.__writer is None:
                self.__writer = DataFileWriter(self.__write_to, DatumWriter(), avro_schema)

            self.__writer.append(item)
