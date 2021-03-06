"""JSON implementations of authentication objects."""

# pylint: disable=no-init
#     Numerous classes don't require __init__.
# pylint: disable=too-many-public-methods,too-few-public-methods
#     Number of methods are defined in specification
# pylint: disable=protected-access
#     Access to protected methods allowed in package json package scope
# pylint: disable=too-many-ancestors
#     Inheritance defined in specification


import importlib


from . import default_mdata
from .. import utilities
from ..osid import objects as osid_objects
from ..osid.metadata import Metadata
from ..primitives import Id
from ..utilities import get_registry
from ..utilities import update_display_text_defaults
from dlkit.abstract_osid.authentication import objects as abc_authentication_objects
from dlkit.abstract_osid.osid import errors


class Agent(abc_authentication_objects.Agent, osid_objects.OsidObject):
    """An ``Agent`` represents an authenticatable identity.

    Like all OSID objects, an ``Agent`` is identified by its ``Id`` and
    any persisted references should use the ``Id``.

    """
    _authority = 'Django_user_service'
    _namespace = 'authentication.Agent'

    def __init__(self, user):
        self.my_user = user

    # Override get_id method to return an id related to Django'
    # native user model
    def get_id(self):
        from django.contrib.auth.models import AnonymousUser
        # identifier = self.my_user.username  # Which one should we use?
        identifier = self.my_user.id       # Which one should we use?
        if isinstance(self.my_user, AnonymousUser):
            identifier = long(0)
            try:
                from ..id.primitives import Id
            except:
                from ..osid.common import Id
        return Id(identifier=identifier,
                  namespace=self._namespace,
                  authority=self._authority)

    # Override get_display_name method to return username
    def get_display_name(self):
        from django.contrib.auth.models import AnonymousUser
        from ..locale.primitives import DisplayText
        if isinstance(self.my_user, AnonymousUser):
            return DisplayText('anonymous_user')
        else:
            return DisplayText(self.my_user.username)

    # Override get_description method to return something
    def get_description(self):
        from ..locale.primitives import DisplayText
        return DisplayText('the agent Id for ' + self.get_display_name().get_text())

    @utilities.arguments_not_none
    def get_agent_record(self, agent_record_type):
        """Gets the agent record corresponding to the given ``Agent`` record ``Type``.

        This method is used to retrieve an object implementing the
        requested record. The ``agent_record_type`` may be the ``Type``
        returned in ``get_record_types()`` or any of its parents in a
        ``Type`` hierarchy where ``has_record_type(agent_record_type)``
        is ``true`` .

        arg:    agent_record_type (osid.type.Type): the type of the
                record to retrieve
        return: (osid.authentication.records.AgentRecord) - the agent
                record
        raise:  NullArgument - ``agent_record_type`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unsupported - ``has_record_type(agent_record_type)`` is
                ``false``
        *compliance: mandatory -- This method must be implemented.*

        """
        return self._get_record(agent_record_type)


class AgentForm(abc_authentication_objects.AgentForm, osid_objects.OsidObjectForm):
    """This is the form for creating and updating ``Agents``.

    Like all ``OsidForm`` objects, various data elements may be set here
    for use in the create and update methods in the
    ``AgentAdminSession``. For each data element that may be set,
    metadata may be examined to provide display hints or data
    constraints.

    """
    _namespace = 'authentication.Agent'

    def __init__(self, **kwargs):
        osid_objects.OsidObjectForm.__init__(self, object_name='AGENT', **kwargs)
        self._mdata = default_mdata.get_agent_mdata()
        self._init_metadata(**kwargs)
        if not self.is_for_update():
            self._init_map(**kwargs)

    def _init_metadata(self, **kwargs):
        """Initialize form metadata"""
        osid_objects.OsidObjectForm._init_metadata(self, **kwargs)

    def _init_map(self, record_types=None, **kwargs):
        """Initialize form map"""
        osid_objects.OsidObjectForm._init_map(self, record_types=record_types)
        self._my_map['assignedAgencyIds'] = [str(kwargs['agency_id'])]

    @utilities.arguments_not_none
    def get_agent_form_record(self, agent_record_type):
        """Gets the ``AgentFormRecord`` corresponding to the given agent record ``Type``.

        arg:    agent_record_type (osid.type.Type): the agent record
                type
        return: (osid.authentication.records.AgentFormRecord) - the
                agent form record
        raise:  NullArgument - ``agent_record_type`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unsupported - ``has_record_type(agent_record_type)`` is
                ``false``
        *compliance: mandatory -- This method must be implemented.*

        """
        return self._get_record(agent_record_type)


class AgentList(abc_authentication_objects.AgentList, osid_objects.OsidList):
    """Like all ``OsidLists,``  ``AgentList`` provides a means for accessing ``Agent`` elements sequentially either one at a time or many at a time.

    Examples: while (al.hasNext()) { Agent agent = al.getNextAgent(); }

    or
      while (al.hasNext()) {
           Agent[] agents = al.getNextAgents(al.available());
      }

    """

    def get_next_agent(self):
        """Gets the next ``Agent`` in this list.

        return: (osid.authentication.Agent) - the next ``Agent`` in this
                list. The ``has_next()`` method should be used to test
                that a next ``Agent`` is available before calling this
                method.
        raise:  IllegalState - no more elements available in this list
        raise:  OperationFailed - unable to complete request
        *compliance: mandatory -- This method must be implemented.*

        """
        # Implemented from template for osid.resource.ResourceList.get_next_resource
        return next(self)

    def next(self):
        return self._get_next_object(Agent)

    __next__ = next

    next_agent = property(fget=get_next_agent)

    @utilities.arguments_not_none
    def get_next_agents(self, n):
        """Gets the next set of ``Agent`` elements in this list which must be less than or equal to the number returned from ``available()``.

        arg:    n (cardinal): the number of ``Agent`` elements requested
                which should be less than or equal to ``available()``
        return: (osid.authentication.Agent) - an array of ``Agent``
                elements.The length of the array is less than or equal
                to the number specified.
        raise:  IllegalState - no more elements available in this list
        raise:  OperationFailed - unable to complete request
        *compliance: mandatory -- This method must be implemented.*

        """
        # Implemented from template for osid.resource.ResourceList.get_next_resources
        return self._get_next_n(AgentList, number=n)
