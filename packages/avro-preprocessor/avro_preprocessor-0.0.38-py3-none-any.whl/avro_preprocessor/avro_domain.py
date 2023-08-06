"""
Module providing a custom order for json-based Avro schemas.
"""

__author__ = "Nicola Bova"
__copyright__ = "Copyright 2018, Jaumo GmbH"
__email__ = "nicola.bova@jaumo.com"

from dataclasses import dataclass


@dataclass
class Avro:
    """
    Helper class to avoid plain strings as dictionary keys.
    """
    Name = 'name'
    Namespace = 'namespace'
    Type = 'type'
    Fields = 'fields'
    Items = 'items'
    Doc = 'doc'
    Record = 'record'
    Enum = 'enum'
    Default = 'default'
    LogicalType = 'logicalType'

    Optional = 'nullable_optional'
    PartitionKey = 'partition_key'

    Null = 'null'
    Value = 'value'
