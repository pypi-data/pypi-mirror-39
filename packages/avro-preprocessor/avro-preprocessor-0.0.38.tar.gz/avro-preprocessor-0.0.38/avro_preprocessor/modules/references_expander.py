"""
A module to expand references of types in schemas using a Depth First strategy.
"""

import copy
from collections import OrderedDict
from typing import Set, Union, cast

from avro_preprocessor.avro_domain import Avro
from avro_preprocessor.preprocessor_module import PreprocessorModule
from avro_preprocessor.schemas_container import SchemasContainer

__author__ = "Nicola Bova"
__copyright__ = "Copyright 2018, Jaumo GmbH"
__email__ = "nicola.bova@jaumo.com"


class ReferencesExpander(PreprocessorModule):
    """
    Expands References in all schemas.
    """
    def __init__(self, schemas: SchemasContainer):
        super().__init__(schemas)

        self.per_schema_already_expanded_records: Set = set()

    def process(self) -> None:
        """Process all schemas."""

        # we first expand the event resources
        for _, schema in self.processed_schemas_iter():
            self.expand_references_in_schema(schema)

    def expand_references_in_schema(self, schema: OrderedDict) -> None:
        """
        Expands references in a schema using a Depth First approach.
        Schemas are expanded only once.
        :param schema: The schema
        """
        self.per_schema_already_expanded_records = set()
        self.traverse_schema(schema, self.expand_references_in_record)

    def expand_references_in_record(self, record: OrderedDict) -> None:
        """
        Expands references in a record.
        :param record: The record
        :return: True if schema was expanded, False otherwise
        """
        if isinstance(record, str):
            return

        if isinstance(record[Avro.Type], str):
            record[Avro.Type] = self.do_expand(record[Avro.Type])
            self.traverse_schema(record[Avro.Type], self.expand_references_in_record)

        elif isinstance(record[Avro.Type], OrderedDict):
            if Avro.Items in record[Avro.Type]:
                record[Avro.Type][Avro.Items] = self.do_expand(record[Avro.Type][Avro.Items])
                self.traverse_schema(
                    record[Avro.Type][Avro.Items], self.expand_references_in_record)

        # Let's check if the JSON type of this record is list:
        # in this case, it will contain strings and/or OrderedDicts
        if isinstance(record[Avro.Type], list):
            # for union, e.g. record['type'] = ["null", "com.example.event.type.Gender"]
            for idx, sub_type in enumerate(record[Avro.Type]):
                if isinstance(sub_type, str):
                    record[Avro.Type][idx] = self.do_expand(sub_type)
                    self.traverse_schema(record[Avro.Type][idx], self.expand_references_in_record)
                if isinstance(sub_type, OrderedDict):
                    if Avro.Items in sub_type:
                        sub_type[Avro.Items] = self.do_expand(sub_type[Avro.Items])
                        self.traverse_schema(sub_type[Avro.Items], self.expand_references_in_record)

    def do_expand(self, resource_to_expand: str) -> Union[str, OrderedDict]:
        """
        Here we do_expand a resource (e.g. com.example.event.type.Gender) if it complies with
        certain criteria (they are in the "if").

        :param resource_to_expand: the resource
        :return: Whether the criteria were met or not
        """
        if '.' in resource_to_expand \
                and resource_to_expand not in self.per_schema_already_expanded_records \
                and resource_to_expand in self.schemas.original:

            self.per_schema_already_expanded_records.add(resource_to_expand)
            return cast(OrderedDict, copy.deepcopy(self.schemas.original[resource_to_expand]))

        return resource_to_expand
