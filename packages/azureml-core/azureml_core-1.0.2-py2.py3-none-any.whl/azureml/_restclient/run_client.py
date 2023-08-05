# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Access a experiment client"""
import copy

from .experiment_client import ExperimentClient
from .clientbase import PAGINATED_KEY


class RunClient(ExperimentClient):
    """
    Experiment APIs

    :param host: The base path for the server to call.
    :type host: str
    :param auth: Client authentication
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param subscription_id:
    :type subscription_id: str
    :param resource_group_name:
    :type resource_group_name: str
    :param workspace_name:
    :type workspace_name: str
    :param experiment_name:
    :type experiment_name: str
    :param run_id:
    :type run_id: str
    """

    def __init__(self,
                 host,
                 auth,
                 subscription_id,
                 resource_group,
                 workspace_name,
                 experiment_name,
                 run_id,
                 **kwargs):
        """
        Constructor of the class.
        """
        super(RunClient, self).__init__(host, auth, subscription_id,
                                        resource_group, workspace_name,
                                        experiment_name,
                                        **kwargs)
        self._run_id = run_id
        self._run_arguments = copy.deepcopy(self._experiment_arguments)
        self._run_arguments.append(self._run_id)

    @classmethod
    def create(cls, workspace, experiment_name, run_id, host=None, auth=None, **kwargs):
        """Create a run client"""
        auth = auth if auth is not None else workspace._auth_object
        # In remote context, we can't fetch workspace id. It is also not needed.
        try:
            workspace_id = workspace._workspace_id
        except Exception:
            workspace_id = None
        return cls(host, auth, workspace.subscription_id,
                   workspace.resource_group, workspace.name, experiment_name,
                   run_id, workspace_id=workspace_id, **kwargs)

    def _execute_with_run_arguments(self, func, *args, **kwargs):
        if not callable(func):
            raise TypeError('Argument is not callable')

        if self._custom_headers:
            kwargs["custom_headers"] = self._custom_headers
        args_list = []
        args_list.extend(self._run_arguments)
        if args:
            args_list.extend(args)
        is_paginated = kwargs.pop(PAGINATED_KEY, False)
        if is_paginated:
            return self._call_paginated_api(func, *args_list, **kwargs)
        else:
            return self._call_api(func, *args_list, **kwargs)

    def _combine_with_run_paginated_dto(self, func, count_to_download=0, *args, **kwargs):
        return self._combine_paginated_base(self._execute_with_run_arguments,
                                            func,
                                            count_to_download,
                                            *args,
                                            **kwargs)
