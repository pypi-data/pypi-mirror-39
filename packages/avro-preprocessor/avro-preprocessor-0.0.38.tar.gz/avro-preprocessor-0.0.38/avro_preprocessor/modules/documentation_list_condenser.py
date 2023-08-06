"""
# Support to use a list for lists as "doc" field to deal with JSON obnoxious lack of
# newline support in strings
"""
from collections import OrderedDict

from avro_preprocessor.avro_domain import Avro
from avro_preprocessor.preprocessor_module import PreprocessorModule

__author__ = "Nicola Bova"
__copyright__ = "Copyright 2018, Jaumo GmbH"
__email__ = "nicola.bova@jaumo.com"


class DocumentationCondenser(PreprocessorModule):
    """
    Condense documentation fields ('doc').
    """

    def process(self) -> None:
        """Process all schemas."""

        # This module has to be applied even to the original schemas
        for _, schema in self.original_schemas_iter():
            self.traverse_schema(schema, self.condense_documentation)

        for _, schema in self.processed_schemas_iter():
            self.traverse_schema(schema, self.condense_documentation)

    @staticmethod
    def condense_documentation(schema: OrderedDict) -> None:
        """
        Condense the "doc" field from list to one string

        :param schema: The (sub) schema
        """

        if Avro.Doc in schema:
            if isinstance(schema[Avro.Doc], list):
                schema[Avro.Doc] = ' '.join(schema[Avro.Doc])
