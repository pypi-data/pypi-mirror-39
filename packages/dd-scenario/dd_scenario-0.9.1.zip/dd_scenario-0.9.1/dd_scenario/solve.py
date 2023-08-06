# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2017, 2018
# --------------------------------------------------------------------------

import json

from six import string_types

from .base_resource import DDObject


class SolveStatus(DDObject):
    '''The class representing solve status.

    Json definition::

        {
          "jobId" : "aeiou",
          "lastModificationTime" : "2000-01-23T04:56:07.000+00:00",
          "solveConfig" : {
            "applicationVersion" : "aeiou",
            "solveParameters" : {
              "key" : "aeiou"
            },
            "collectEngineLog" : true,
            "containerId" : "aeiou"
          },
          "taskUsername" : "aeiou",
          "state" : "aeiou",
          "error" : "aeiou",
          "jobDetails" : {
            "interruptedAt" : 123456789,
            "interruptionStatus" : "aeiou",
            "executionStatus" : "aeiou",
            "startedAt" : 123456789,
            "failureInfo" : {
              "type" : "aeiou",
              "message" : "aeiou"
            },
            "createdAt" : 123456789,
            "applicationVersionUsed" : "aeiou",
            "solveStatus" : "aeiou",
            "endedAt" : 123456789,
            "details" : {
              "key" : "aeiou"
            },
            "id" : "aeiou",
            "submittedAt" : 123456789,
            "updatedAt" : 123456789
          },
          "containerId" : "aeiou",
          "projectId" : "aeiou",
          "taskToken" : "aeiou"
        }
    ```

    Attributes:
        json: The json fragment used to build this Table.
    '''
    def __init__(self, json=None,
                 **kwargs):
        '''Creates a Table.

        Args:
            name (:obj:`string`): The name of the asset.
            json (:obj:`dict`): The dict describing the asset.
            **kwargs (optional): kwargs to override container attributes.
                Attributes specified here will override those of ``json``.
        '''
        super(SolveStatus, self).__init__(json=json, **kwargs)

    def __repr__(self):
        d = {}
        d.update(self.json)
        return json.dumps(d, indent=3)

    def _repr_html_(self):
        from IPython.display import HTML
        try:
            import pandas
            if self.jobDetails is not None:
                elapsed = self.jobDetails['endedAt'] - self.jobDetails['startedAt']
                exec_status = self.jobDetails['executionStatus']
            else:
                elapsed = '-'
                exec_status = '-'
            df = pandas.DataFrame([[self.state, exec_status, elapsed]],
                                    columns=["State", "Execution status", "Elapsed"])
            return df.to_html(index=False)
        except ImportError:
            return repr(self)



class SolveConfig(DDObject):
    '''The class representing solve configuration.

    Attributes:
        containerId: The container name.
        collectEngineLog: The collect engine log flag.
        applicationVersion: The application version.
        solveParameters: A dict with { name: value } for solve parameters
    ```

    Attributes:
        json: The json fragment used to build this Table.
    '''
    def __init__(self, json=None,
                 **kwargs):
        '''Creates a Table.

        Args:
            name (:obj:`string`): The name of the asset.
            json (:obj:`dict`): The dict describing the asset.
            **kwargs (optional): kwargs to override container attributes.
                Attributes specified here will override those of ``json``.
        '''
        super(SolveConfig, self).__init__(json=json, **kwargs)

    def __repr__(self):
        d = {}
        d.update(self.json)
        return json.dumps(d, indent=3)
