# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------

"""Access RunHistoryClient"""
import six


from azureml.exceptions import AzureMLException
# noinspection PyProtectedMember
from azureml._base_sdk_common import _ClientSessionId

from .contracts.events import (create_heartbeat_event, create_start_event,
                               create_failed_event, create_completed_event,
                               create_canceled_event)
from .contracts.utils import get_run_ids_filter_expression, get_new_id
from .models.create_run_dto import CreateRunDto
from .experiment_client import ExperimentClient
from .constants import (RUN_ID_EXPRESSION, ORDER_BY_STARTTIME_EXPRESSION,
                        ORDER_BY_RUNID_EXPRESSION, DEFAULT_PAGE_SIZE, FILTER_KEY)
from ._odata.expressions import and_join
from ._odata.runs import (get_filter_run_tags, get_filter_run_properties, get_filter_run_type,
                          get_filter_run_created_after, get_filter_run_status, get_filter_include_children)
from ._hierarchy.runs import Tree
from .utils import _generate_client_kwargs


class RunHistoryClient(ExperimentClient):
    """
    Run History APIs

    :param host: The base path for the server to call.
    :type host: str
    :param auth: Authentication for the client
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param subscription_id:
    :type subscription_id: str
    :param resource_group_name:
    :type resource_group_name: str
    :param workspace_name:
    :type workspace_name: str
    :param experiment_name:
    :type experiment_name: str
    """

    @staticmethod
    def create(workspace, experiment_name, _host=None, **kwargs):
        """
        Create a RunHistoryClient for the history
        :param workspace: User's workspace
        :type workspace: azureml.core.workspace.Workspace
        :param experiment_name:
        :type experiment_name: str
        """
        # In remote context, we can't fetch workspace id. It is also not needed.
        try:
            workspace_id = workspace._workspace_id
        except Exception:
            workspace_id = None

        return RunHistoryClient(_host, workspace._auth_object, workspace.subscription_id,
                                workspace.resource_group, workspace.name, experiment_name,
                                workspace_id=workspace_id, **kwargs)

    def get_events(self, run_id, page_size=DEFAULT_PAGE_SIZE, order_by=None,
                   caller=None, custom_headers=None):
        """
        Get events of a run by its run_id
        :param run_id: run id (required)
        :type run_id: str
        :param page_size: number of dto returned by one request (optional)
        :type page_size: int
        :param order_by: keys to sort return values, ('sort_key', 'asc'/'desc')(optional)
        :type order_by: tuple (str, str)
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return: a generator of ~_restclient.models.BaseEvent
        """
        if not run_id:
            raise ValueError('Argument run_id cannot be None or empty.')

        order_by_expression = self._validate_order_by(order_by)
        kwargs = _generate_client_kwargs(run_id=run_id, top=page_size, orderby=order_by_expression,
                                         caller=caller, custom_headers=custom_headers, is_paginated=True)

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_events.list, **kwargs)

        return self._execute_with_experiment_arguments(self._client.events.list, **kwargs)

    def post_event(self, run_id, event, caller=None, custom_headers=None, is_async=False):
        """
        Post an event of a run by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param run_id: run id (required)
        :type run_id: str
        :param event: event to update (required)
        :type event: models.BaseEvent
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :param is_async: execute request asynchronously
        :type is_async: bool
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: None (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        kwargs = _generate_client_kwargs(run_id=run_id, event_message=event,
                                         caller=caller, custom_headers=custom_headers, is_async=is_async)

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_events.post,
                                                           **kwargs)

        return self._execute_with_experiment_arguments(self._client.events.post,
                                                       **kwargs)

    def post_event_run_start(self, run_id, caller=None, custom_headers=None, is_async=False):
        """
        Post run-started-event by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param run_id: run id (required)
        :type run_id: str
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_header: dict
        :param is_async: execute request asynchronously
        :type is_async: bool
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: None (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        event = create_start_event(run_id)
        return self.post_event(run_id, event, is_async=is_async, caller=caller, custom_headers=custom_headers)

    def post_event_run_failed(self, run_id, caller=None, custom_headers=None, is_async=False):
        """
        Post run-failed-event by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param run_id: run id (required)
        :type run_id: str
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_header: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: None (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        event = create_failed_event(run_id)
        return self.post_event(run_id, event, is_async=is_async, caller=caller, custom_headers=custom_headers)

    def post_event_run_completed(self, run_id, caller=None, custom_headers=None, is_async=False):
        """
        Post run-completed-event by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param run_id: run id (required)
        :type run_id: str
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_header: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: None (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        event = create_completed_event(run_id)
        return self.post_event(run_id, event, is_async=is_async, caller=caller, custom_headers=custom_headers)

    def post_event_run_canceled(self, run_id, caller=None, custom_headers=None, is_async=False):
        """
        Post run-canceled-event by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param run_id: run id (required)
        :type run_id: str
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_header: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: None (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        event = create_canceled_event(run_id)
        return self.post_event(run_id, event, is_async=is_async, caller=caller, custom_headers=custom_headers)

    def post_event_run_heartbeat(self, run_id, time, caller=None, custom_headers=None, is_async=False):
        """
        Post run-heartbeat-event by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param run_id: run id (required)
        :type run_id: str
        :param time: timeout in seconds (required)
        :type time: int
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_header: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: None (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        event = create_heartbeat_event(run_id, time)
        return self.post_event(run_id, event, is_async=is_async, caller=caller, custom_headers=custom_headers)

    def create_run(self, run_id=None, script_name=None, target=None,
                   run_name=None, create_run_dto=None, caller=None, custom_headers=None, is_async=False):
        """
        create a run
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param run_id: run id
        :type run_id: str
        :param script_name: script name
        :type script_name: str
        :param target: run target
        :type target: str
        :param run_name: run name
        :type run_name: str
        :param CreateRunDto create_run_dto: run object to create
        :type create_run_dto: CreateRunDto
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_header: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.RunDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        run_id = get_new_id() if run_id is None else run_id
        if not create_run_dto or not isinstance(create_run_dto, CreateRunDto):
            create_run_dto = CreateRunDto(run_id=run_id,
                                          script_name=script_name,
                                          target=target,
                                          name=run_name,
                                          status='NotStarted')

        kwargs = _generate_client_kwargs(create_run_dto=create_run_dto,
                                         is_async=is_async, caller=caller, custom_headers=custom_headers)

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_run.create, **kwargs)

        kwargs['run_id'] = run_id
        return self._execute_with_experiment_arguments(self._client.run.patch, **kwargs)

    def get_child_runs(self, parent_run_id, root_run_id, recursive=False, _filter_on_server=False,
                       page_size=DEFAULT_PAGE_SIZE, order_by=None,
                       caller=None, custom_headers=None, **kwargs):
        """
        Get child runs by parent_run_id
        :param parent_run_id: parent_run_id(required)
        :type parent_run_id: str
        :param root_run_id: optimization id for hierarchy(required)
        :type root_run_id: str
        :param recursive: fetch grandchildren and further descendants(required)
        :type recursive: bool
        :param page_size: number of dto returned by one request (optional)
        :type page_size: int
        :param order_by: keys to sort return values, ('sort_key', 'asc'/'desc')(optional)
        :type order_by: tuple (str, str)
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return: list of dictionary whose keys are property of ~_restclient.models.RunDto
        """
        order_by_expression = self._validate_order_by(order_by) if order_by else [ORDER_BY_STARTTIME_EXPRESSION]
        client_kwargs = _generate_client_kwargs(top=page_size, orderby=order_by_expression, caller=caller,
                                                custom_headers=custom_headers, is_paginated=True)
        client_kwargs.update(kwargs)
        filter_expression = self._get_run_filter_expr(**kwargs) if _filter_on_server else None
        if recursive and _filter_on_server:
            raise AzureMLException("Recursive get_child_runs is not yet supported with service side filtering")
        elif recursive:
            root_filter = 'RootRunId eq {0}'.format(root_run_id)
            full_filter = and_join([root_filter, filter_expression]) if _filter_on_server else root_filter

            client_kwargs[FILTER_KEY] = full_filter
            run_dtos = self._execute_with_experiment_arguments(
                self._client.run.list, **client_kwargs)

            # Filter out nodes outside of the desired sub tree
            run_hierarchy = Tree(run_dtos)
            sub_tree_run_dtos = run_hierarchy.get_subtree_dtos(parent_run_id)

            return self._client_filter(sub_tree_run_dtos, **kwargs)
        else:
            route = (self._client.legacy_run.get_child if self.api_route ==
                     RunHistoryClient.OLD_ROUTE else self._client.run.get_child)
            run_dtos = self._execute_with_experiment_arguments(route,
                                                               run_id=parent_run_id,
                                                               **client_kwargs)
            return run_dtos if _filter_on_server else self._client_filter(run_dtos, **kwargs)

    def create_child_run(self, parent_run_id, run_id, script_name=None,
                         target=None, run_name=None, caller=None, custom_headers=None, is_async=False):
        """
        Create a child run
        :param parent_run_id: parent_run_id(required)
        :type parent_run_id: str
        :param run_id: run_id(required)
        :type run_id: str
        :param script_name: script name
        :type script_name: str
        :param target: run target
        :type target: str
        :param run_name: run_name
        :type run_name: str
        :param is_async: execute request asynchronously
        :type is_async: bool (optional)
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.RunDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        kwargs = _generate_client_kwargs(
            is_async=is_async, caller=caller, custom_headers=custom_headers)

        create_run_dto = CreateRunDto(run_id=run_id,
                                      parent_run_id=parent_run_id,
                                      script_name=script_name,
                                      target=target,
                                      name=run_name,
                                      status='NotStarted')

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_run.create_child,
                                                           run_id=parent_run_id,
                                                           new_child_run=create_run_dto,
                                                           **kwargs)
        else:
            return self._execute_with_experiment_arguments(self._client.run.patch,
                                                           run_id=run_id,
                                                           create_run_dto=create_run_dto,
                                                           **kwargs)

    def get_runstatus(self, run_id, caller=None, custom_headers=None, is_async=False):
        """
        Get status details of a run by its run_id
        :param run_id: run id (required)
        :type run_id: str
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.RunDetailsDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        kwargs = _generate_client_kwargs(
            is_async=is_async, caller=caller, custom_headers=custom_headers)

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            func = self._client.legacy_run.get_status
        else:
            func = self._client.run.get_details
        return self._execute_with_experiment_arguments(func, run_id=run_id, **kwargs)

    def get_run(self, run_id, caller=None, custom_headers=None, is_async=False):
        """
        Get detail of a run by its run_id
        :param run_id: run id (required)
        :type run_id: str
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.RunDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        kwargs = _generate_client_kwargs(
            is_async=is_async, caller=caller, custom_headers=custom_headers)

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(
                self._client.legacy_run.get, run_id=run_id, **kwargs)

        return self._execute_with_experiment_arguments(
            self._client.run.get, run_id=run_id, **kwargs)

    def get_runs(self, last=0, _filter_on_server=False,
                 page_size=DEFAULT_PAGE_SIZE, order_by=None,
                 caller=None, custom_headers=None, **kwargs):
        """
        Get detail of all runs of an experiment
        :param last: the number of latest runs to return (optional)
        :type last: int
        :param page_size: number of dto returned by one request (optional)
        :type page_size: int
        :param order_by: keys to sort return values, ('sort_key', 'asc'/'desc')(optional)
        :type order_by: tuple (str, str)
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return: a generator of ~_restclient.models.RunDto
        """
        order_by_expression = self._validate_order_by(order_by) if order_by else [ORDER_BY_STARTTIME_EXPRESSION]
        client_kwargs = _generate_client_kwargs(orderby=order_by_expression, caller=caller,
                                                custom_headers=custom_headers,
                                                is_paginated=True)
        client_kwargs.update(kwargs)

        pagesize = DEFAULT_PAGE_SIZE if page_size < 1 else page_size
        top = last if last < pagesize and last > 0 else pagesize
        filter_expression = self._get_run_filter_expr(**kwargs) if _filter_on_server else None

        route = (self._client.legacy_run.list if self.api_route ==
                 RunHistoryClient.OLD_ROUTE else self._client.run.list)
        run_dtos = self._execute_with_experiment_arguments(route,
                                                           total_count=last,
                                                           top=top,
                                                           filter=filter_expression,
                                                           **client_kwargs)

        return run_dtos if _filter_on_server else self._client_filter(run_dtos, **kwargs)

    def get_runs_by_run_ids(self, run_ids=None, page_size=DEFAULT_PAGE_SIZE, order_by=None,
                            caller=None, custom_headers=None):
        """
        Get detail of all runs of an experiment
        :param run_ids: list of run ids
        :type run_ids: [str]
        :param page_size: number of dto returned by one request (optional)
        :type page_size: int
        :param order_by: keys to sort return values, ('sort_key', 'asc'/'desc')(optional)
        :type order_by: tuple (str, str)
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return: a generator of ~_restclient.models.RunDto
        """
        order_by_expression = self._validate_order_by(order_by) if order_by else [ORDER_BY_RUNID_EXPRESSION]
        kwargs = _generate_client_kwargs(top=page_size, orderby=order_by_expression, caller=caller,
                                         custom_headers=custom_headers, is_paginated=True)

        if run_ids is not None:
            kwargs[FILTER_KEY] = get_run_ids_filter_expression(run_ids)

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_run.list, **kwargs)

        return self._execute_with_experiment_arguments(self._client.run.list, **kwargs)

    def get_metrics_by_run_ids(self, run_ids=None, page_size=DEFAULT_PAGE_SIZE, order_by=None,
                               merge_strategy_type=None, caller=None, custom_headers=None):
        """
        Get run_metrics of multiple runs
        :param run_ids: run ids(optional)
        :type run_ids: [str]
        :param page_size: number of dto returned by one request (optional)
        :type page_size: int
        :param order_by: keys to sort return values, ('sort_key', 'asc'/'desc')(optional)
        :type order_by: tuple (str, str)
        :param mergestrategytype: Possible values include: 'Default', 'None', 'MergeToVector'
        :type mergestrategytype: str
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return: a generator of ~_restclient.models.RunMetricDto
        """
        order_by_expression = self._validate_order_by(order_by) if order_by else [ORDER_BY_RUNID_EXPRESSION]
        kwargs = _generate_client_kwargs(top=page_size, orderby=order_by_expression, caller=caller,
                                         mergestrategytype=merge_strategy_type,
                                         custom_headers=custom_headers, is_paginated=True)

        if run_ids is not None:
            kwargs[FILTER_KEY] = get_run_ids_filter_expression(run_ids)

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_runmetric.list, **kwargs)

        return self._execute_with_experiment_arguments(self._client.run_metric.list, **kwargs)

    def get_metrics(self, run_id=None, page_size=DEFAULT_PAGE_SIZE, order_by=None,
                    merge_strategy_type=None, caller=None, custom_headers=None):
        """
        Get run_metrics of an experiment
        :param run_id: run id (optional)
        :type run_id: str
        :param page_size: number of dto returned by one request (optional)
        :type page_size: int
        :param order_by: keys to sort return values, ('sort_key', 'asc'/'desc')(optional)
        :type order_by: tuple (str, str)
        :param mergestrategytype: Possible values include: 'Default', 'None',
         'MergeToVector'
        :type mergestrategytype: str
        :param caller: caller function name (optional)
        :type caller: str
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return: a generator of ~_restclient.models.RunMetricDto
        """
        order_by_expression = self._validate_order_by(order_by)
        kwargs = _generate_client_kwargs(top=page_size, orderby=order_by_expression, caller=caller,
                                         mergestrategytype=merge_strategy_type,
                                         custom_headers=custom_headers, is_paginated=True)

        if run_id is not None:
            kwargs[FILTER_KEY] = '{}{}'.format(RUN_ID_EXPRESSION, run_id)

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_runmetric.list, **kwargs)

        return self._execute_with_experiment_arguments(self._client.run_metric.list, **kwargs)

    def get_metrics_by_runs(self, run_ids=None):
        """
        Get run_metrics of multiple runs
        :param run_ids: run ids(optional)
        :type run_ids: [str]
        :return: list of dictionary whose keys are property of ~_restclient.models.RunMetricDto
        """
        self._logger.warning(
            "get_metrics_by_runs is deprecated, please use get_metrics_by_run_ids")
        if isinstance(run_ids, list):
            filter = get_run_ids_filter_expression(run_ids)
            order_expression = [ORDER_BY_RUNID_EXPRESSION]
            return self._combine_with_experiment_paginated_dto(self._client.legacy_runmetric.list,
                                                               filter=filter, orderby=order_expression)

        return self._combine_with_experimentt_paginated_dto(self._client.legacy_runmetric.list)

    def post_runmetrics(self, run_id, run_metric_dto, caller=None, custom_headers=None, is_async=False):
        """
        Post run_metrics of one run
        :param run_id: run id
        :type run_id: str
        :param run_metric_dto run_metric_dto: a ~_restclient.models.RunMetricDto object
        :type run_metric_dto:~_restclient.models.RunMetricDto
        :param is_async: execute request asynchronously
        :type is_async: bool (optional)
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: None (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        kwargs = _generate_client_kwargs(
            is_async=is_async, caller=caller, custom_headers=custom_headers)
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_runmetric.post,
                                                           run_id=run_id,
                                                           run_metric_dto=run_metric_dto,
                                                           **kwargs)

        return self._execute_with_experiment_arguments(self._client.run_metric.post,
                                                       run_id=run_id,
                                                       run_metric_dto=run_metric_dto,
                                                       **kwargs)

    def update_run(self, run_id, modify_run_dto, caller=None, custom_headers=None, is_async=False):
        """
        Update a run to the run history client
        :param run_id: run id (required)
        :type run_id: str
        :param modify_run_dto: modified run object(required)
        :type modify_run_dto: ~_restclient.models.ModifyRunDto
        :param is_async: execute request asynchronously
        :type is_async: bool (optional)
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.RunDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        kwargs = _generate_client_kwargs(
            is_async=is_async, caller=caller, custom_headers=custom_headers)
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_run.update,
                                                           run_id=run_id,
                                                           modify_run_dto=modify_run_dto,
                                                           **kwargs)

        return self._execute_with_experiment_arguments(self._client.run.update,
                                                       run_id=run_id,
                                                       modify_run_dto=modify_run_dto,
                                                       **kwargs)

    def patch_run(self, run_id, create_run_dto, caller=None, custom_headers=None, is_async=False):
        """
        Patch a run to the run history client
        :param run_id: run id (required)
        :type run_id: str
        :param create_run_dto: a new run object(required)
        :type ~_restclient.models.CreateRunDto
        :param is_async: execute request asynchronously
        :type is_async: bool (optional)
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.RunDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        kwargs = _generate_client_kwargs(
            is_async=is_async, caller=caller, custom_headers=custom_headers)
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_run.patch,
                                                           run_id=run_id,
                                                           modify_run_dto=create_run_dto,
                                                           **kwargs)

        return self._execute_with_experiment_arguments(self._client.run.patch,
                                                       run_id=run_id,
                                                       create_run_dto=create_run_dto,
                                                       **kwargs)

    def modify_run(self, create_run_dto, caller=None, custom_headers=None, is_async=False):
        """
        Patch or create a run to the run history client,
        :param create_run_dto: a new run object(required)
        :type ~_restclient.models.CreateRunDto
        :param is_async: execute request asynchronously
        :type is_async: bool (optional)
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: dict
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.RunDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        kwargs = _generate_client_kwargs(
            is_async=is_async, caller=caller, custom_headers=custom_headers)
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_experiment_arguments(self._client.legacy_run.add_or_modify,
                                                           create_run_dto=create_run_dto,
                                                           **kwargs)

        return self._execute_with_experiment_arguments(self._client.run.patch,
                                                       run_id=create_run_dto.run_id,
                                                       create_run_dto=create_run_dto,
                                                       **kwargs)

    _run_filter_mapping = {
        'tags': get_filter_run_tags,
        'properties': get_filter_run_properties,
        'runtype': get_filter_run_type,
        'created_after': get_filter_run_created_after,
        "status": get_filter_run_status,
        "include_children": get_filter_include_children
    }

    def _get_run_filter_expr(self, **kwargs):
        exprs = []
        for filter_type, filter_val in kwargs.items():
            if filter_val is None:
                self._logger.debug("Skipping filter %s for None val", filter_type)
                continue
            filter_func = RunHistoryClient._run_filter_mapping.get(filter_type, None)
            if filter_func is None:
                self._logger.warning(
                    "Received unknown filter type: {0} on {1}".format(filter_type, filter_val))
            else:
                self._logger.debug("Getting filter %s for %s", filter_func, filter_val)
                filter_query = filter_func(filter_val)
                if filter_query is not None:
                    exprs.append(filter_query)
        return None if len(exprs) < 1 else and_join(exprs)

    def _filter_run_on_created_after(run_dto, created_after):
        return run_dto.created_utc >= created_after

    def _filter_run_on_status(run_dto, status):
        return run_dto.status == status

    def _filter_run_on_type(run_dto, type):
        return run_dto.run_type == type

    def _filter_run_on_tags(run_dto, tags):
        if isinstance(tags, six.text_type) and tags in run_dto.tags.keys():
            return True
        elif isinstance(tags, dict):
            if set(tags.items()).issubset(run_dto.tags.items()):
                return True
        return False

    def _filter_run_on_props(run_dto, props):
        if isinstance(props, six.text_type) and props in run_dto.properties.keys():
            return True
        elif isinstance(props, dict):
            if set(props.items()).issubset(run_dto.properties.items()):
                return True
        return False

    def _filter_run_on_include_children(run_dto, include_children):
        is_parent = run_dto.parent_run_id
        return is_parent is None or include_children

    _run_client_filter_mapping = {
        "tags": _filter_run_on_tags,
        "properties": _filter_run_on_props,
        "runtype": _filter_run_on_type,
        "created_after": _filter_run_on_created_after,
        "status": _filter_run_on_status,
        "include_children": _filter_run_on_include_children
    }

    def _client_filter(self, run_dtos, **kwargs):
        filter_funcs = {}
        for filter_type, filter_val in kwargs.items():
            if filter_val is None:
                self._logger.debug("Skipping filter %s for None val", filter_type)
                continue

            filter_func = RunHistoryClient._run_client_filter_mapping.get(filter_type, None)
            if filter_func is None:
                self._logger.warning(
                    "Received unknown filter type: {0} on {1}".format(filter_type, filter_val))
            else:
                self._logger.debug("Getting filter %s for %s", filter_func, filter_val)
                filter_funcs[filter_func] = filter_val

        for run_dto in run_dtos:
            skip = False
            for func, val in filter_funcs.items():
                self._logger.debug("client filtering %s on %s", run_dto, val)
                if not func(run_dto, val):
                    skip = True
            if not skip:
                yield run_dto

    def _prepare_experiment(self):
        run_id = get_new_id()
        create_run_dto = CreateRunDto(run_id=run_id,
                                      hidden=True)
        self.create_run(run_id=run_id, create_run_dto=create_run_dto)
        self._logger.debug("Created run  with id {} to prepare experiment".format(run_id))

    def _validate_order_by(self, order_by):
        if not order_by:
            return None
        if not isinstance(order_by, tuple) or len(order_by) != 2:
            raise TypeError("order_by should be two-elements tuple type.")
        if not isinstance(order_by[0], str) or not isinstance(order_by[1], str):
            raise TypeError("expecting string value in order_by elements.")
        order = ['asc', 'desc']
        lowerCase = order_by[1].lower()
        if lowerCase not in order:
            raise ValueError("The second element in order_by should be 'asc' or 'desc'.")
        return ["{} {}".format(order_by[0], lowerCase)]

    def _get_metrics_by_run_ids(self, run_ids):
        """Get multiple metrics by run history run ids.

        :param run_ids: Run Ids for the metrics to fetch. *Note* Best Metric value is retrieved
        and updated for these runs
        :type run_ids:
        :param custom_headers: Additional headers sent in the request.
        :type custom_headers: dict
        :return: Transformed metric data in a friendly format.
        :rtype: dict
        """

        # Short-circuit if there's no work to do
        if not run_ids:
            return {}

        def _batches(items, size):
            """Convert a list into batches of the specified size.

            :param items: The list of items to split into batches.
            :type items: list
            :param size: The number of items in each batch.
            :type size: int
            """
            for i in range(0, len(items), size):
                yield items[i:i + size]

        # Number of run ids per batch
        batch_size = 20

        # With hyperdrive/automl scenarios count of runs can get quite large and GET request limit may be reached
        # easily. We will need to group runs into batches and fetch the metrics based on defined degree
        # of parallelism.
        _batches = list(_batches(sorted(run_ids), batch_size))
        trans_metrics = {}
        tasks = []

        common_headers = {'x-ms-client-session-id': _ClientSessionId}

        for batch in _batches:
            result_as_generator = self.get_metrics_by_run_ids(
                run_ids=batch, custom_headers=common_headers,
                order_by=('RunId', 'asc'))
            tasks.append(result_as_generator)

        for task in tasks:
            # create friendly view of metrics; similar to what get_metrics returns for a single run
            for metric in task:
                if metric.run_id not in trans_metrics:
                    trans_metrics[metric.run_id] = {}
                run_metrics = trans_metrics[metric.run_id]
                if metric.cells:
                    metric_name = metric.name
                    metric_type = metric.metric_type
                    for cell in metric.cells:
                        if metric_type == 'azureml.v1.scalar':
                            if metric_name in run_metrics:
                                run_metrics[metric_name].append(cell[metric_name])
                            else:
                                run_metrics[metric_name] = [cell[metric_name]]
                        elif metric_type == 'azureml.v1.table':
                            if metric_name not in run_metrics:
                                run_metrics[metric_name] = {}
                            table_metrics = run_metrics[metric_name]
                            for metric_key, metric_value in cell.items():
                                if metric_key in table_metrics:
                                    table_metrics[metric_key].append(metric_value)
                                else:
                                    table_metrics[metric_key] = [metric_value]
        return trans_metrics
