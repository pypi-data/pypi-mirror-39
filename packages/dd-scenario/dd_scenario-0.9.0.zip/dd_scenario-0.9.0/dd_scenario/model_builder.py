# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2017, 2018
# --------------------------------------------------------------------------

import json

from six import string_types

from .base_resource import DDObject
from .container import Container


def get_model_builder_id(what):
    if hasattr(what, "name"):
        return what.name
    elif isinstance(what, string_types):
        return what
    else:
        raise ValueError("Don't know how to get model builder id from %s" % what)


class ModelBuilder(DDObject):
    '''The Model Builder class.
    '''
    def __init__(self, json=None,**kwargs):
        '''Creates a new Model Builder.

        Examples:

            To create a list of :class:`~ModelBuilder` from model builder metadata of a
            project, for instance, the response.json() from
            :class:`~dd_decisionservice.Client.get_model_builders()`:

                >>> model_builders = [ModelBuilder(json=s) for s in client.get_model_builders()]

            To create a model builder with a given name and projectId:

                >>> model_builder = ModelBuilder(name="foo", projectId="aeiou")

        Args:
           json (:obj:`dict`, optional): The dict describing the container.
           client: The client that this model builder is bound to.
           **kwargs (optional): kwargs to override container attributes.
               Attributes specified here will override those of ``desc``.
        '''
        super(ModelBuilder, self).__init__(json=json, **kwargs)

    def __repr__(self):
        return json.dumps(self.json, indent=3)

    def create_container(self,
                         category=None,
                         **kwargs):
        '''Creates a :class:`~dd_scenario.Container` whose parent is this
        model builder.

        Currently supported categories are:

            * ``'inputset'``
            * ``'scenario'``
            * ``'model'``

        Example:
            This creates an ``inputset`` container with the name 'foo'::

                >>> c = model_builder.create_container(category='inputset', name='foo')

        Args:
            category: The category of the container.
            **kwargs: kwargs passed to the :class:`~dd_scenario.Container`
                constructor. For example, you can pass params such as
                ``name`` etc..
        Returns:
            The created :class:`~dd_scenario.Container`
        '''
        if category is None:
            raise ValueError('parameter \'category\' is mandatory')
        container = Container(parentId=self.name, category=category, **kwargs)
        sc = self.client.create_container(self.name, container)
        return sc

    def get_containers(self, category=None, as_dict=False):
        '''Returns containers of the specified category in this model builder.

        Args:
            category: The category of container. Must be ``'inputset'``,
                ``'scenario'`` or ``'model'``.
            as_dict: If True, the containers are returned as a dict where its keys
                are the container names and its values are containers.
        Returns:
            A list of :class:`~dd_scenario.Container` or a dict mapping
            container names to :class:`~dd_scenario.Container`
        '''
        containers = self.client.get_containers(parent_id=self.name, category=category)
        return {s.name: s for s in containers} if as_dict else containers

    def lookup_container(self, name, category=None):
        containers = self.client.get_containers(parent_id=self.name, category=category)
        target = [x for x in containers if x.name == name]
        return target[0] if target else None

    def delete_container(self, container):
        '''Deletes the specified container

        Args:
            container: The container to be deleted.
        '''
        self.client.delete_container(container)

    def create_scenario(self, name, **kwargs):
        '''Creates a new :class:`~dd_scenario.Container` attached as a
        scenario  of this :class:`~dd_scenario.ModelBuilder`.

        Args:
            name: The name of the container.
            **kwargs: kwargs passed to the :class:`~dd_scenario.Container`
               constructor.
        Returns:
            ~dd_scenario.Container: The scenario as a
            :class:`~dd_scenario.Container`
        Raises:
            ~dd_scenario.NotBoundException: when the Artifact is not bound to
                a client.
        '''
        return self.create_container(category='scenario',
                                           name=name,
                                           **kwargs)

    def get_scenario(self, name):
        '''Returns the scenario for the specified name.

        Args:
            name: The name of the scenario.
        Returns:
            ~dd_scenario.Container: The scenario as a
                :class:`~dd_scenario.Container`
          '''
        return self.lookup_container(name=name, category="scenario")

    def get_scenarios(self, as_dict=False):
        '''Returns scenarios of this model builder.

        Args:
            as_dict: If True, the containers are returned as a dict which keys
                are container names and which values are containers.
        Returns:
            A list of :class:`~dd_scenario.Container` or a dict mapping
            container names to :class:`~dd_scenario.Container`
        '''
        return self.get_containers(category="scenario", as_dict=as_dict)

