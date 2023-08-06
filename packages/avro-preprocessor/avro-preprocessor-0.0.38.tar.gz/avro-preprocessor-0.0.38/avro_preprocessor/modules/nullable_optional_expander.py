"""
A module to expand nullable_optional fields.
"""

from collections import OrderedDict
from typing import Any, Set, Optional

from avro_preprocessor.avro_domain import Avro
from avro_preprocessor.preprocessor_module import PreprocessorModule
from avro_preprocessor.schemas_container import SchemasContainer

__author__ = "Nicola Bova"
__copyright__ = "Copyright 2018, Jaumo GmbH"
__email__ = "nicola.bova@jaumo.com"


class NullableOptionalExpander(PreprocessorModule):
    """
    Expand nullable_optional fields in all schemas.
    """
    def __init__(self, schemas: SchemasContainer):
        super().__init__(schemas)

        self.per_schema_nullable_optional_records: Set = set()
        self.current_namespace: Optional[str] = None

    def process(self) -> None:
        """Process all schemas."""
        for _, schema in self.processed_schemas_iter():
            # we keep track of the namespace; used to refer to already substituted custom records
            if Avro.Namespace in schema:
                self.current_namespace = schema[Avro.Namespace]
            self.substitute_nullable_optionals_in_json(schema)

    def substitute_nullable_optionals_in_json(self, schema: OrderedDict) -> None:
        """
        Optionals are expanded in the schema of the json in input.
        A tuple (extended_json_schema, original_json_schema).
        :param schema: The schema in input
        :return tuple
        """
        self.per_schema_nullable_optional_records = set()
        self.traverse_schema(schema, self.substitute_field_type)

    def substitute_field_type(self, record: OrderedDict) -> None:
        """
        Substitutes in place a nullable_optional record with with Optional<Type>
        (e.g. string -> OptionalString).

        Substitutes in place a nullable_optional record with with Optional<Name>
        (e.g. name = address, type = record -> OptionalAddress).
        :param record: The field in input
        """
        def get_subrecord_name(record_name: str, record_type: Any) -> str:
            def capitalize_only_first(word: str) -> str:
                return word[0].upper() + word[1:]

            if isinstance(record_type, str):
                if '.' in record_type:
                    tokens = record_type.split('.')
                    new_record_name = \
                        '.'.join(
                            tokens[:-1] + ['Optional' + capitalize_only_first(tokens[-1])]
                        )
                else:
                    new_record_name = 'Optional' + capitalize_only_first(current_type)
            else:
                new_record_name = 'Optional' + capitalize_only_first(record_name)

            return new_record_name

        if Avro.Optional in record:
            if record[Avro.Optional] is True:
                current_type = record[Avro.Type]

                subrecord_name = get_subrecord_name(record[Avro.Name], current_type)

                if self.current_namespace:
                    fully_qualified_subrecord_name = self.current_namespace + '.' + subrecord_name
                else:
                    raise ValueError("self.current_namespace was not initialized for"
                                     "name {}, type{}".format(record[Avro.Name], current_type))

                if fully_qualified_subrecord_name in self.per_schema_nullable_optional_records:

                    # We cannot define the same record twice in the same file,
                    # so we use a reference here
                    record[Avro.Type] = [Avro.Null, fully_qualified_subrecord_name]
                else:

                    # Saving the reference
                    self.per_schema_nullable_optional_records.add(fully_qualified_subrecord_name)

                    def add_null_type() -> list:
                        if isinstance(current_type, list):
                            # avro type is a union
                            if Avro.Null in current_type:
                                # "null" already in the list
                                return current_type
                            # we add "null" in the first position of the list
                            return [Avro.Null] + current_type
                        return [Avro.Null, current_type]

                    # Substituting the nullable_optional record with a wrapper:
                    # Semantics:
                    # if MyField == null -> not present
                    # if MyField.value == null -> set-to-null
                    # if MyField.value != null -> set-to-value
                    record[Avro.Type] = [
                        Avro.Null,
                        OrderedDict((
                            (Avro.Name, subrecord_name),
                            (Avro.Type, Avro.Record),
                            (Avro.Fields, [
                                OrderedDict((
                                    (Avro.Name, Avro.Value),
                                    (Avro.Doc, "The optional value"),
                                    (Avro.Type, add_null_type())
                                ))
                            ]),
                        ))
                    ]

                    subrecord: OrderedDict = record[Avro.Type][1]

                    if Avro.Doc in record:
                        subrecord[Avro.Doc] = record[Avro.Doc] + ' (Optional Value)'

                    # Avro complex types have additional fields that must be moved to the subrecord
                    additional_fields = \
                        [(field, record[field]) for field in record
                         if field not in ("name", "type", "doc", "default", "nullable_optional")]
                    for key, value in additional_fields:
                        subrecord[key] = value
                        record.pop(key)

                # necessary to allow 'not present' semantics
                record[Avro.Default] = None

            # property 'nullable_optional' is removed from the schema anyway
            record.pop(Avro.Optional)
