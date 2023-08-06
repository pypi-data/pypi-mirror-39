# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2017, 2018
# --------------------------------------------------------------------------

import json


class NotBoundException(Exception):
    '''The exception raised when a method that needs the object to be bound
    to a :class:`~dd_scenario.Client` is called, but the object is not bound.

    An object is bound to a :class:`~dd_scenario.Client` when it has been
    created with its ``client`` property set.
    '''
    pass


class DDObject(object):
    '''Base object for Decision service.
    '''
    def __init__(self, json=None, client=None, **kwargs):
        '''
        Constructor
        '''
        d = dict()
        # set values from ``json`` then apply kwargs
        if json:
            d.update(json)
        d.update(**kwargs)
        super(DDObject, self).__setattr__('json', d)
        super(DDObject, self).__setattr__('_client', client)

    @property
    def client(self):
        if self._client:
            return self._client
        else:
            raise NotBoundException("%s not bound to a dd_scenario.Client. Please make an instance of %s from appropriate client API." % (type(self), type(self)))

    def __setattr__(self, name, value):
        self.json[name] = value

    def __getattr__(self, name):
        try:
            return self.json[name]
        except KeyError:
            return None

    def __getitem__(self, name):
        if isinstance(name, int):
            return getattr(json, name)
        else:
            return getattr(self, name)

    def to_json(self, **kwargs):
        '''Returns a string with the json for this object, using fields
        and value types that the API service understands.

        This is used to serialize the ``Scenario`` before a query to the REST
        API.
        '''
        return json.dumps(self.json, **kwargs)
