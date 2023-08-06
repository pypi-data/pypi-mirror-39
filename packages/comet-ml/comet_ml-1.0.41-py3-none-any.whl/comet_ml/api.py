# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2019 Comet ML INC
#  This file can not be copied and/or distributed
#  without the express permission of Comet ML Inc.
# *******************************************************

import requests
import logging
import copy
import re

from .config import get_config
from .comet import get_rest_api_key, get_api_key
from .experiment import BaseExperiment
from .connection import get_backend_session

LOGGER = logging.getLogger(__name__)


class MetricsList(list):
    def __getitem__(self, item):
        if isinstance(item, int):
            return super(MetricsList, self).__getitem__(item)
        else:
            return [
                (x["step"], float(x["metricValue"]))
                for x in self
                if x["metricName"] == item
            ]


class APIExperiment(object):
    def __init__(self, api, workspace, project, experiment_key):
        """
        REST API Experiment interface.
        """
        self._api = api
        self.workspace = workspace
        self.project = project
        self._api._build_cache(self.workspace, self.project, experiment_key)
        self.experiment_key = self._api._get(
            self.workspace, self.project, experiment_key
        )["experiment_key"]

    def _get_experiment_url(self):
        return "%s/%s/%s/%s" % (
            self._api.get_url_server(),
            self.workspace,
            self.project,
            self.experiment_key,
        )

    ## Just steal these two methods for now:
    _in_jupyter_environment = BaseExperiment._in_jupyter_environment
    display = BaseExperiment.display

    @property
    def data(self):
        """
        The experiment data in JSON-like format.
        """
        data = self._api._get(self.workspace, self.project, self.experiment_key)
        if "metrics" not in data:
            data["metrics"] = [x["name"] for x in self.metrics]
        if "_other" not in data:
            data["_other"] = self._api.get_experiment_other(self.experiment_key)
            data["other"] = [x["name"] for x in data["_other"]]
            names = [x["valueCurrent"] for x in data["_other"] if x["name"] == "Name"]
            if len(names) > 0:
                new_data = copy.deepcopy(data)
                new_data["is_key"] = False
                self._api._set(self.workspace, self.project, names[0], new_data)
                data["_name"] = names[0]
        if "parameters" not in data:
            data["parameters"] = [x["name"] for x in self.parameters]
        return data

    def __repr__(self):
        data = self._api._get(self.workspace, self.project, self.experiment_key)
        return "<APIExperiment '%s/%s/%s'>" % (
            self.workspace,
            self.project,
            data["_name"] if "_name" in data else self.experiment_key,
        )

    @property
    def existing_experiment(self):
        """
        Get an ExistingExperiment() object for this
        experiment.
        """
        ee = self._api.get_experiment(self.experiment_key)
        if not ee.alive:
            raise ValueError(
                "invalid access: you can't make " + "an existing experiment"
            )
        return ee

    @property
    def html(self):
        """
        Get the HTML associated with this experiment. Not cached.
        """
        return self._api.get_experiment_html(self.experiment_key)

    @property
    def code(self):
        """
        Get the associated source code for this experiment. Not cached.
        """
        return self._api.get_experiment_code(self.experiment_key)

    @property
    def stdout(self):
        """
        Get the associated standard output for this experiment. Not cached.
        """
        return self._api.get_experiment_stdout(self.experiment_key)

    @property
    def installed_packages(self):
        """
        Get the associated installed packages for this experiment. Not cached.
        """
        return self._api.get_experiment_installed_packages(self.experiment_key)

    @property
    def os_packages(self):
        """
        Get the associated installed packages for this experiment. Not cached.
        """
        return self._api.get_experiment_os_packages(self.experiment_key)

    @property
    def graph(self):
        """
        Get the associated graph/model description for this
        experiment. Not cached.
        """
        return self._api.get_experiment_graph(self.experiment_key)

    @property
    def images(self):
        """
        Get the associated image data for this experiment. Not cached.

        The image data comes as a dictionary with the following
        keys:

            apiKey
            runId
            experimentKey
            projectId
            figCounter
            figName
            step
            runContext
            fileName
            imagePath
        """
        return self._api.get_experiment_images(self.experiment_key)

    @property
    def parameters(self):
        """
        Get the asssociated parameters for this experiment. Not cached.
        """
        return self._api.get_experiment_parameters(self.experiment_key)

    @property
    def metrics(self):
        """
        Get the asssociated metrics for this experiment. Not cached.
        """
        return self._api.get_experiment_metrics(self.experiment_key)

    @property
    def other(self):
        """
        Get the asssociated other items (things logged with `log_other`)
        for this experiment. Cached.
        """
        data = self._api._get(self.workspace, self.project, self.experiment_key)
        if "_other" not in data:
            data["_other"] = self._api.get_experiment_other(self.experiment_key)
            data["other"] = [x["name"] for x in data["_other"]]
            names = [x["valueCurrent"] for x in data["_other"] if x["name"] == "Name"]
            if len(names) > 0:
                new_data = copy.deepcopy(data)
                new_data["is_key"] = False
                self._api._set(self.workspace, self.project, names[0], new_data)
                data["_name"] = names[0]
        return data["_other"]

    @property
    def metrics_raw(self):
        """
        Get the asssociated raw metrics for this experiment. Not cached.
        """
        return MetricsList(self._api.get_experiment_metrics_raw(self.experiment_key))

    @property
    def git_metadata(self):
        """
        Get the asssociated git-metadata for this experiment. Not cached.
        """
        return self._api.get_experiment_git_metadata(self.experiment_key)

    @property
    def git_patch(self):
        """
        Get the asssociated git-patch for this experiment. Not cached.
        """
        return self._api.get_experiment_git_patch(self.experiment_key)

    @property
    def asset_list(self):
        """
        Get the asssociated asset-list for this experiment. Not cached.
        """
        return self._api.get_experiment_asset_list(self.experiment_key)

    def get_asset(self, asset_id):
        """
        Get an asset from this experiment. Not cached.
        """
        return self._api.get_experiment_asset(self.experiment_key, asset_id)


class APIExperiments(object):
    def __init__(self, api, workspace, project):
        self._api = api
        self.workspace = workspace
        self.project = project
        self._api._build_cache(self.workspace, self.project)

    @property
    def data(self):
        """
        The project data in JSON format.
        """
        return self._api._get(self.workspace, self.project)

    def __getitem__(self, item):
        if isinstance(item, int):
            return APIExperiment(self._api, self.workspace, self.project, list(self)[item])
        try:
            return APIExperiment(self._api, self.workspace, self.project, item)
        except Exception:  # regular expression, perhaps
            return [
                APIExperiment(self._api, self.workspace, self.project, exp)
                for exp in self
                if re.match(item, exp)
            ]

    def __repr__(self):
        return str([key for key in self])

    def __len__(self):
        return len(
            [
                x
                for x in self._api._get(self.workspace, self.project, include=True)
                if self._api._get(self.workspace, self.project, x)["is_key"]
            ]
        )

    def __iter__(self):
        return iter(
            [
                (
                    self._api._get(self.workspace, self.project, x)["_name"]
                    if "_name" in self._api._get(self.workspace, self.project, x)
                    else x
                )
                for x in self._api._get(self.workspace, self.project, include=True)
                if self._api._get(self.workspace, self.project, x)["is_key"]
            ]
        )


class Projects(object):
    def __init__(self, api, workspace):
        """
        The REST API object for accessing the projects.
        """
        self._api = api
        self.workspace = workspace
        self._api._build_cache(workspace)

    @property
    def data(self):
        """
        Return info on workspace.
        """
        return {
            "workspace": self.workspace,
            "projects": list(self._api._get(self.workspace, include=True).keys()),
        }

    def __getitem__(self, item):
        if isinstance(item, int):
            return APIExperiments(self._api, self.workspace, list(self)[item])
        return APIExperiments(self._api, self.workspace, item)

    def __repr__(self):
        return str([key for key in self])

    def __len__(self):
        return len(self._api._get(self.workspace, include=True).keys())

    def __iter__(self):
        return iter(self._api._get(self.workspace, include=True).keys())


class Workspaces(object):
    def __init__(self, api):
        """
        The REST API object for accessing the workspaces.
        """
        self._api = api

    def __getitem__(self, item):
        if isinstance(item, int):
            return Projects(self._api, list(self)[item])
        if "/" in item:
            workspace, project = item.split("/", 1)
            if "/" in project:
                project, exp = project.split("/", 1)
                return self[workspace][project][exp]
            else:
                return self[workspace][project]
        else:
            return Projects(self._api, item)

    def __repr__(self):
        return str([key for key in self])

    def __len__(self):
        return len(
            [x for x in self._api._get().keys() if self._api._get(x)["is_owner"]]
        )

    def __iter__(self):
        return iter(
            [x for x in self._api._get().keys() if self._api._get(x)["is_owner"]]
        )


class API(object):
    DEFAULT_VERSION = "v1"
    URLS = {"v1": {"SERVER": "https://www.comet.ml", "REST": "/api/rest/v1/"}}
    COMET_HEADER = "Authorization"

    def __init__(self, api_key=None, rest_api_key=None, version=None,
                 persistent=True):
        """
        Application Programming Interface to the Comet REST interface.

        Args:
            api_key: Optional. Your private COMET_API_KEY (or store in
                .env)
            rest_api_key: Optional. Your private COMET_REST_API_KEY
                (or store in .env)
            version: Optional. The version of the REST API to use.
            persistent: Default True. Use a persistent connection?

        Example:
        ```
        >>> from comet_ml import API
        >>> comet_api = API()
        >>> comet_api.get()
        ['project1', 'project2', ...]
        ```
        """
        self._session = None if not persistent else get_backend_session()
        self._version = version if version is not None else self.DEFAULT_VERSION
        self._config = get_config()
        self._rest_api_key = get_rest_api_key(rest_api_key, self._config)
        self._api_key = get_api_key(api_key, self._config)
        self._CACHE = {
            w: {"projects": {}, "is_owner": True} for w in self.get_workspaces()
        }
        self.workspaces = Workspaces(self)

    def get(self,  workspace=None, project=None, experiment=None):
        """
        Get the following items:
            * list of workspace names, given no arguments
            * list of project names, given a workspace name
            * list of experiment names/keys, given workspace and project names
            * an experiment, given workspace, project, and experiemnt name/key

        `workspace`, `project`, and `experiment` can also be given as a single
        string, delimited with a slash.

        Note that `experiment` can also be a regular expression.
        """
        ## First, we check for delimiters:
        if workspace is not None and "/" in workspace:
            if project is not None:
                raise SyntaxError("Can't use slash format in workspace name " +
                                  "and provide project name")
            workspace, project = workspace.split("/", 1)
        if project is not None and "/" in project:
            if experiment is not None:
                raise SyntaxError("Can't use slash format in project name " +
                                  "and provide experiment key/name")
            project, experiment = project.split("/", 1)
        ## Now, return the appropriate item:
        if workspace is None:
            return self.workspaces
        elif project is None:
            return self.workspaces[workspace]
        elif experiment is None:
            return self.workspaces[workspace][project]
        else:
            return self.workspaces[workspace][project][experiment]

    def _get(self, workspace=None, project=None, experiment_key=None, include=False):
        if workspace is None:
            return self._CACHE
        elif project is None:
            if include:
                return self._CACHE[workspace]["projects"]
            else:
                return self._CACHE[workspace]
        elif experiment_key is None:
            if include:
                return self._CACHE[workspace]["projects"][project]["experiments"]
            else:
                return self._CACHE[workspace]["projects"][project]
        else:
            return self._CACHE[workspace]["projects"][project]["experiments"][
                experiment_key
            ]

    def _set(self, workspace, project, experiment_key, data):
        self._CACHE[workspace]["projects"][project]["experiments"][
            experiment_key
        ] = data

    def _build_cache(self, workspace, project=None, experiment_name=None):
        if workspace not in self._CACHE:
            self._CACHE[workspace] = {"projects": {}, "is_owner": False}
        if self._CACHE[workspace]["projects"] == {}:
            self._CACHE[workspace]["projects"] = {
                w["project_name"]: w for w in self.get_projects(workspace)
            }
        if project is not None:
            if "experiments" not in self._CACHE[workspace]["projects"][project]:
                self._CACHE[workspace]["projects"][project]["experiments"] = {}
                project_id = self._CACHE[workspace]["projects"][project]["project_id"]
                for d in self.get_experiment_data(project_id):
                    d["is_key"] = True
                    self._CACHE[workspace]["projects"][project]["experiments"][
                        d["experiment_key"]
                    ] = d
        if project is not None and project not in self._CACHE[workspace]["projects"]:
            raise Exception(
                "no such project '%s' for workspace '%s'" % (project, workspace)
            )
        if experiment_name is not None:
            if (
                experiment_name
                not in self._CACHE[workspace]["projects"][project]["experiments"]
            ):
                ## FIXME: replace with new endpoint
                ## need to go through all the experiments in this project
                retval = None
                for experiment_key in list(
                    self._CACHE[workspace]["projects"][project]["experiments"]
                ):
                    data = self._CACHE[workspace]["projects"][project]["experiments"][
                        experiment_key
                    ]
                    if "_other" not in data:
                        data["_other"] = self.get_experiment_other(experiment_key)
                    data["other"] = [x["name"] for x in data["_other"]]
                    names = [
                        x["valueCurrent"] for x in data["_other"] if x["name"] == "Name"
                    ]
                    if len(names) > 0:
                        data["_name"] = names[0]
                        new_data = copy.deepcopy(data)
                        new_data["is_key"] = False
                        self._CACHE[workspace]["projects"][project]["experiments"][
                            names[0]
                        ] = new_data
                        if data["_name"] == experiment_name:
                            retval = experiment_key
                if retval is None:
                    raise Exception("no such experiment name: '%s'" % experiment_name)

    def get_url(self, version=None):
        """
        Returns the URL for this version of the API.
        """
        version = version if version is not None else self._version
        return self.URLS[version]["SERVER"] + self.URLS[version]["REST"]

    def get_url_server(self, version=None):
        """
        Returns the URL server for this version of the API.
        """
        version = version if version is not None else self._version
        return self.URLS[version]["SERVER"]

    def get_url_end_point(self, end_point, version=None):
        """
        Return the URL + end point.
        """
        return self.get_url(version) + end_point

    def get_request(self, end_point, params):
        """
        Given an end point and a dictionary of params,
        return the results.
        """
        url = self.get_url_end_point(end_point)
        LOGGER.debug("API.get_request: url = %s, params = %s", url, params)
        headers = {self.COMET_HEADER: self._rest_api_key}
        if self._session is not None:
            response = self._session.get(url, params=params, headers=headers)
        else:
            response = requests.get(url, params=params, headers=headers)
        raise_exception = None
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exception:
            if exception.response.status_code == 401:
                raise_exception = ValueError("Invalid COMET_REST_API_KEY")
            else:
                raise
        if raise_exception:
            raise raise_exception
        return response.json()

    def get_version(self):
        """
        Return the default version of the API.
        """
        return self._version

    def get_workspaces(self):
        """
        Return the names of the workspaces for this user.
        """
        params = {}
        results = self.get_request("workspaces", params)
        return results["workspaces"]

    def get_projects(self, workspace):
        """
        Return the ids of the projects in a workspace.
        """
        params = {"workspace": workspace}
        results = self.get_request("projects", params)
        return results["projects"]

    def get_experiment_keys(self, project_id):
        """
        Get the experiment_keys given a project id.
        """
        params = {"projectId": project_id}
        results = self.get_request("experiments", params)
        return [exp["experiment_key"] for exp in results["experiments"]]

    def get_experiment_data(self, project_id):
        """
        Returns the JSON data for all experiments
        in a project.
        """
        params = {"projectId": project_id}
        results = self.get_request("experiments", params)
        return results["experiments"]

    def get_experiment(self, experiment_key):
        """
        Returns an ExistingExperiment() given an
        experiment key.
        """
        from . import ExistingExperiment

        return ExistingExperiment(
            api_key=self._api_key, previous_experiment=experiment_key
        )

    def get_experiment_html(self, experiment_key):
        """
        Returns the HTML data given an experiment key.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/html", params)
        return results["html"]

    def get_experiment_code(self, experiment_key):
        """
        Returns the code associated with an experiment (or None
        if there isn't any code), given an experiment key.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/code", params)
        return results["code"]

    def get_experiment_stdout(self, experiment_key):
        """
        Returns the standard output of an experiment,
        given an experiment key.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/stdout", params)
        return results["output"]

    def get_experiment_installed_packages(self, experiment_key):
        """
        Return the list of installed Python packages at the
        time an experiment was run.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/installed-packages", params)
        return results["packages"]

    def get_experiment_os_packages(self, experiment_key):
        """
        Return the list of installed OS packages at the
        time an experiment was run.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/os-packages", params)
        return results["packages"]

    def get_experiment_graph(self, experiment_key):
        """
        Return the model graph, given an experiment key.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/graph", params)
        return results["graph"]

    def get_experiment_images(self, experiment_key):
        """
        Return the experiment images, given an experiment
        key.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/images", params)
        return results["images"]

    def get_experiment_parameters(self, experiment_key, param=None):
        """
        Return the experiment parameters, given an experiment key.
        Optionally, also if you provide the parameter name, the
        function will only return the value(s) of the
        parameter.

        Examples:
        ```
        >>> from comet_ml import API
        >>> comet_api = API()
        >>> comet_api.get("myworkspace/project1").parameters[0]["valueCurrent"]
        0.1
        >>> [[(exp, "hidden_size", int(param["valueCurrent"]))
        ...   for param in exp.parameters
        ...   if param["name"] == "hidden_size"][0]
        ...  for exp in comet_api.get("dsblank/pytorch/.*")]
        [(<APIExperiment>, 'hidden_size', 128),
         (<APIExperiment>, 'hidden_size', 64)]
        >>> comet_api.get("myworkspace/myproject").parameters
        [{"name": "learning_rate", ...}, {"name": "hidden_layer_size", ...}]
        ```
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/params", params)
        if param is not None:
            retval = [
                p["valueCurrent"] for p in results["results"] if p["name"] == param
            ]
            return retval
        else:
            return results["results"]

    def get_experiment_metrics(self, experiment_key, metric=None):
        """
        Return the experiment metrics, given an experiment key.
        Optionally, also if you provide the metric name, the
        function will only return the value(s) of the
        metric.

        Examples:
        ```
            >>> from comet_ml import API
            >>> comet_api = API()
            >>> comet_api.get_experiment_metrics("accuracy")
            [0.0, 0.1, 0.5, ...]
            >>> comet_api.get_experiment_metrics("loss")
            [1.3, 1.2, 0.9, 0.6, ...]
            >>> comet_api.get_experiment_metrics()
            [{"name": "accuracy", ...}, {"name": "loss", ...}]
        ```
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/metrics", params)
        if metric is not None:
            retval = [
                m["valueCurrent"] for m in results["results"] if m["name"] == metric
            ]
            return retval
        else:
            return results["results"]

    def get_experiment_other(self, experiment_key, other=None, value=None):
        """
        Get the other items logged, given an experiment key.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/log-other", params)
        if other is not None:
            if value is not None:
                retval = [
                    m
                    for m in results["logOtherList"]
                    if m["name"] == other and m["valueCurrent"] == value
                ]
            else:
                retval = [
                    m["valueCurrent"]
                    for m in results["logOtherList"]
                    if m["name"] == other
                ]
            return retval
        else:
            return results["logOtherList"]

    def get_experiment_metrics_raw(self, experiment_key, metric=None):
        """
        Get the other items logged (in raw form), given an experiment key.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/metrics-raw", params)
        if metric is not None:
            retval = [
                m["valueCurrent"] for m in results["metrics"] if m["name"] == metric
            ]
            return retval
        else:
            return results["metrics"]

    def get_experiment_asset_list(self, experiment_key):
        """
        Get a list of assets associated with experiment.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("asset/get-asset-list", params)
        return results

    def get_experiment_asset(self, experiment_key, asset_id):
        """
        Get an asset, given the experiment_key and asset_id.
        """
        params = {"experimentKey": experiment_key, "assetId": asset_id}
        results = self.get_request("asset/get-asset", params)
        return results

    def get_experiment_git_patch(self, experiment_key):
        """
        Get the git-patch associated with this experiment.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("git/get-patch", params)
        return results

    def get_experiment_git_metadata(self, experiment_key):
        """
        Get the git-metadata associated with this experiment.
        """
        params = {"experimentKey": experiment_key}
        results = self.get_request("experiment/git-metadata", params)
        return results
