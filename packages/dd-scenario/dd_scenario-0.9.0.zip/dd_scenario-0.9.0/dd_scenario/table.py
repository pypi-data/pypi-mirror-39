# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2017, 2018
# --------------------------------------------------------------------------

import json

from six import string_types

from .base_resource import DDObject


def get_table_name(what):
    if hasattr(what, "name"):
        return what.name
    elif isinstance(what, string_types):
        return what
    else:
        raise ValueError("Don't know how to get asset name from %s" % what)


class Table(DDObject):
    '''The class for container tables.

    Attributes:
        json: The json fragment used to build this Table.
        name: The name of the table.
        container: The container this table is attached to.
        guid: The table name.
        createdAt: The creation date.
        creator: The creator of the table.
    '''
    def __init__(self, json=None, container=None,
                 **kwargs):
        '''Creates a Table.

        Args:
            name (:obj:`string`): The name of the asset.
            json (:obj:`dict`): The dict describing the asset.
            **kwargs (optional): kwargs to override container attributes.
                Attributes specified here will override those of ``json``.
        '''
        super(Table, self).__init__(json=json, **kwargs)
        super(DDObject, self).__setattr__('container', container)

    def __repr__(self):
        d = {}
        d.update(self.json)
        return json.dumps(d, indent=3)


class ColumnType(object):
    def __init__(self, dataType, key):
        self.dataType = dataType
        self.key = key

    def to_json(self):
        return {"dataType": self.dataType, "key": self.key }


class TableType(object):
    '''The class for container table types.

    ``TableType`` stores the types for all the columns of a table.

    Example:

        Displays all data types for each column of a table::

            types = container.get_table_type(table)
            for i,t in enumerate(types):
                print("[%s] type=%s key=%s" % (i, t.dataType, t.key))
    '''
    def __init__(self, json=None, id=None, **kwargs):
        '''Creates a TableType.

        Args:
            id (:obj:`string`): The name of the table.
            json (:obj:`dict`): The dict describing the asset.
            **kwargs (optional): kwargs to override container attributes.
                Attributes specified here will override those of ``json``.
        '''
        self.id = id
        self.columns = [ColumnType(j["dataType"], j["key"])
                        for j in json["columns"]]

    def __repr__(self):
        d = self.to_json()
        d['_id'] = self.id
        return json.dumps(d, indent=3)

    def to_json(self):
        d = {}
        d['columns'] = [x.to_json() for x in self.columns]
        return d

    def __len__(self):
        return len(self.columns)

    def __iter__(self):
        return iter(self.columns)

    def __getitem__(self, index):
        return self.columns[index]
