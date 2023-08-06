'''
.. autoclass:: ContainerSecurity
.. automodule:: tenable.cs.images
.. automodule:: tenable.cs.repository
.. automodule:: tenable.cs.reports
.. automodule:: tenable.cs.usage

Raw HTTP Calls
==============

Even though the ``ContainerSecurity`` object pythonizes the Container
Security API for you, there may still bee the occasional need to make raw HTTP 
calls to the Container Security API.  The methods listed below aren't run 
through any naturalization by the library aside from the response code checking.
These methods effectively route directly into the requests session.  The 
responses will be Response objects from the ``requests`` library.  In all cases, 
the path is appended to the base ``url`` paramater that the 
``ContainerSecurity`` object was instantiated with.

Example:

.. code-block:: python

   resp = cs.get('repositories')

.. py:module:: tenable.cs
.. rst-class:: hide-signature
.. autoclass:: ContainerSecurity

    .. automethod:: get
    .. automethod:: post
    .. automethod:: put
    .. automethod:: delete
'''
from tenable.base import APISession
from .compliance import ComplianceAPI
from .containers import ContainersAPI
from .imports import ImportAPI
from .jobs import JobsAPI
from .registry import RegistryAPI
from .reports import ReportsAPI
from .uploads import UploadAPI

class ContainerSecurity(APISession):
    '''
    The Container Security object is the primary interaction point for users to
    interface with Container Security via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        access_key (str):
            The user's API access key for Tenable.io.
        secret_key (str):
            The user's API secret key for Tenable.io.
        url (str, optional):
            The base URL that the paths will be appended onto.  The default
            is ``https://cloud.tenable.com``.
        registry (str, optional): 
            The registry path to use for docker pushes.  The default is
            ``registry.cloud.tenable.com``.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``3``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``0.1`` seconds.
    '''
    _url = 'https://cloud.tenable.com/container-security/api'
    _registry = 'registry.cloud.tenable.com'

    @property
    def images(self):
        return ImagesAPI(self)

    @property
    def repository(self):
        return RepositoryAPI(self)

    @property
    def reports(self):
        return ReportsAPI(self)

    @property
    def uploads(self):
        return UploadsAPI(self)

    @property
    def usage(self):
        return UsageAPI(self)

    def __init__(self, access_key, secret_key, 
                 url=None, retries=None, backoff=None, registry=None):
        self._access_key = access_key
        self._secret_key = secret_key
        if registry:
            self._registry = registry
        APISession.__init__(self, url, retries, backoff)

    def _build_session(self):
        '''
        Build the session and add the API Keys into the session
        '''
        APISession._build_session(self)
        self._session.headers.update({
            'X-APIKeys': 'accessKey={}; secretKey={};'.format(
                self._access_key, self._secret_key)
        })
