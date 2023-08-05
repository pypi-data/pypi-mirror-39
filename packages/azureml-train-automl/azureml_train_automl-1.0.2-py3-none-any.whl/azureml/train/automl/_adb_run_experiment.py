# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import hashlib
import importlib
import json
import os
import pytz
import time
import datetime

from azureml._async.daemon import Daemon
from azureml._restclient import JasmineClient
from azureml.core import Run
from azureml.core.authentication import AzureMlTokenAuthentication
from azureml.core.experiment import Experiment
from azureml.core.workspace import Workspace
from azureml.telemetry import set_diagnostics_collection
from azureml.train.automl import extract_user_data, fit_pipeline
from azureml._restclient.run_history_client import RunHistoryClient
from automl.client.core.common import metrics, pipeline_spec, utilities

from . import _dataprep_utilities, automl, constants
from ._automl_settings import _AutoMLSettings
from . import _logging
from ._adb_get_data import get_input_datamodel_from_dataprep_json
from .automl import set_problem_info
from .run import AutoMLRun

MAX_RETRY_COUNT = 5
SLEEP_TIME = 10
AML_TOKEN_REFRESH_TIME = 1800
JASMINE_CLIENT = "JasmineClient"
RUNHISTORY_CLIENT = "RunHistoryClient"


def adb_run_experiment(input_params):
    """
    This method is responsible for reading run configuraiton values and call jasmine to get next
    pipeline and call fit iteration.
    """
    worker_id = input_params[0]
    run_context = input_params[1]
    subscription_id = run_context.get('subscription_id', None)
    resource_group = run_context.get('resource_group', None)
    workspace_name = run_context.get('workspace_name', None)
    location = run_context.get('location', None)
    aml_token = run_context.get('aml_token', None)
    experiment_name = run_context.get('experiment_name', None)
    parent_run_id = run_context.get('parent_run_id', None)
    service_url = run_context.get('service_url', None)
    dataprep_json = run_context.get('dataprep_json', None)
    automl_settings_str = run_context.get('automl_settings_str', None)
    _set_env_variables(subscription_id, resource_group,
                       workspace_name, experiment_name, aml_token, service_url)

    adb_experiment = _AdbAutomlExperiment(parent_run_id,
                                          subscription_id,
                                          resource_group,
                                          workspace_name,
                                          experiment_name,
                                          aml_token,
                                          service_url,
                                          location,
                                          automl_settings_str,
                                          dataprep_json,
                                          worker_id)
    adb_experiment.Run()


def _set_env_variables(subscription_id, resource_group, workspace_name, experiment_name, aml_token, service_url):
    df_value_list = [subscription_id, resource_group, workspace_name, experiment_name,
                     aml_token, service_url]
    var = None
    if any(var is not None for var in df_value_list):
        def raise_val_error():
            raise ValueError("{0}: Value can't be None".format(var))
    os.environ["AZUREML_ARM_SUBSCRIPTION"] = subscription_id
    os.environ["AZUREML_ARM_RESOURCEGROUP"] = resource_group
    os.environ["AZUREML_ARM_WORKSPACE_NAME"] = workspace_name
    os.environ["AZUREML_ARM_PROJECT_NAME"] = experiment_name
    os.environ["AZUREML_RUN_TOKEN"] = aml_token
    os.environ["AZUREML_SERVICE_ENDPOINT"] = service_url


def log_message(logger=None, logging_level=_logging.INFO, parent_run_id=None, worker_id=None, message=None):
    print("{0}, {1}, {2}, {3}".format(
        datetime.datetime.utcnow(), parent_run_id, worker_id, message))

    if logger is None:
        return

    if logging_level == _logging.ERROR:
        logger.error("{0}, {1}, {2}".format(parent_run_id, worker_id, message))
    elif logging_level == _logging.DEBUG:
        logger.debug("{0}, {1}, {2}".format(parent_run_id, worker_id, message))
    elif logging_level == _logging.WARNING:
        logger.warning("{0}, {1}, {2}".format(
            parent_run_id, worker_id, message))
    else:
        logger.info("{0}, {1}, {2}".format(parent_run_id, worker_id, message))


class _AdbAutomlExperiment():
    def __init__(self,
                 parent_run_id,
                 subscription_id,
                 resource_group,
                 workspace_name,
                 experiment_name,
                 aml_token,
                 service_url,
                 location,
                 automl_settings_str,
                 dataprep_json,
                 worker_id):
        self.parent_run_id = parent_run_id
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name
        self.experiment_name = experiment_name
        self.aml_token = aml_token
        self.service_url = service_url
        self.location = location
        self.worker_id = worker_id
        self._auto_refresh_daemon = None
        self._refresh_time = None
        self.automl_settings_str = automl_settings_str

        os.environ["AZUREML_RUN_TOKEN"] = self.aml_token

        self.run_history_client = self._create_client(RUNHISTORY_CLIENT)
        self.automl_settings = _AutoMLSettings(
            self._rehydrate_experiment(), **json.loads(self.automl_settings_str))
        print("{0}, {1}, {2}, Enabling telemetry with verbosity {3}".format(datetime.datetime.utcnow(),
                                                                            self.parent_run_id,
                                                                            self.worker_id,
                                                                            self.automl_settings.telemetry_verbosity))
        set_diagnostics_collection(send_diagnostics=self.automl_settings.send_telemetry,
                                   verbosity=self.automl_settings.telemetry_verbosity)
        self.logger = _logging.get_logger(
            self.automl_settings.debug_log, self.automl_settings.verbosity)

        self._refresh_aml_token()

        self.input_data = get_input_datamodel_from_dataprep_json(dataprep_json)

    def Run(self):

        parent_run_id = self.parent_run_id
        worker_id = self.worker_id
        logger = self.logger
        self._start_aml_token_refresh_daemon(AML_TOKEN_REFRESH_TIME)
        log_message(logger=logger, parent_run_id=parent_run_id, worker_id=worker_id,
                    message="Starting experiment run on worker node...")

        retry_count = 0
        while (True):
            try:
                # Jasmine client is created everytime to avoid unauthorized error due to expired token.
                aml_token = os.environ["AZUREML_RUN_TOKEN"]
                log_message(logger=logger,
                            parent_run_id=parent_run_id,
                            worker_id=worker_id,
                            message="Creating new jasmine client using amltoken(hash): '{}'".format(
                                hashlib.sha1(aml_token.encode()).hexdigest()))
                jasmine_client = self._create_client(JASMINE_CLIENT)
                pipeline_dto = jasmine_client.get_next_pipeline(
                    parent_run_id, worker_id)
                if pipeline_dto.is_experiment_over:
                    log_message(logger=logger, parent_run_id=parent_run_id, worker_id=worker_id,
                                message="Experiment already finished.")
                    break
                if pipeline_dto.pipeline_spec == "":
                    if pipeline_dto.retry_after > 0:
                        log_message(logger=logger, logging_level=_logging.DEBUG,
                                    parent_run_id=parent_run_id, worker_id=worker_id,
                                    message="Waiting for pipelines wait for {0} seconds".format(
                                        pipeline_dto.retry_after))
                        time.sleep(pipeline_dto.retry_after)
                    continue

                child_run_id = pipeline_dto.childrun_id
                os.environ["AZUREML_RUN_ID"] = child_run_id
                self.fit_iteration(pipeline_dto, child_run_id)
                retry_count = 0
            except Exception as e:
                log_message(logger=logger, logging_level=_logging.WARNING, parent_run_id=parent_run_id,
                            worker_id=worker_id, message=e)
                retry_count += 1
                if retry_count <= MAX_RETRY_COUNT:
                    log_message(logger=logger, logging_level=_logging.WARNING,
                                parent_run_id=parent_run_id, worker_id=worker_id,
                                message="retry count:{0}, sleeping for {1} sec".format(retry_count, SLEEP_TIME))
                    time.sleep(SLEEP_TIME)
                else:
                    log_message(logger=logger, logging_level=_logging.ERROR,
                                parent_run_id=parent_run_id, worker_id=worker_id,
                                message="retry count:{0}, sleeping for {1} sec".format(retry_count, SLEEP_TIME))
                    break

        log_message(logger=logger, parent_run_id=parent_run_id, worker_id=worker_id,
                    message="Finished experiment run on worker node.")

    def _rehydrate_experiment(self):
        auth = AzureMlTokenAuthentication(self.aml_token)
        workspace = Workspace(self.subscription_id,
                              self.resource_group, self.workspace_name,
                              auth=auth,
                              _location=self.location,
                              _disable_service_check=True)
        experiment = Experiment(workspace, self.experiment_name)
        return experiment

    def _rehydrate_run(self, run_id):
        return Run(self._rehydrate_experiment(), run_id)

    def fit_iteration(self, pipeline_dto, run_id):
        """
        Fit iteration method.

        :param pipeline_dto: Pipeline details to fit.
        :type pipeline_dto: PipelineDto
        :param run_id: run id.
        :type run_id: string
        """
        run_id = pipeline_dto.childrun_id
        pipeline_id = pipeline_dto.pipeline_id
        parent_run_id = self.parent_run_id
        worker_id = self.worker_id
        logger = self.logger
        log_message(logger=logger, parent_run_id=parent_run_id, worker_id=worker_id,
                    message="Received pipeline: {0} for run id '{1}'".format(pipeline_dto.pipeline_spec, run_id))

        # This is due to toke expiry issue
        current_run = self._rehydrate_run(run_id)
        try:
            current_run.start()
            log_message(logger=logger, parent_run_id=parent_run_id, worker_id=worker_id,
                        message="{0}: Starting childrun...".format(run_id))

            if (run_id.endswith("setup")):
                set_problem_info(X=self.input_data.X,
                                 y=self.input_data.y,
                                 task_type=self.automl_settings.task_type,
                                 current_run=current_run,
                                 preprocess=self.automl_settings.preprocess,
                                 is_adb_run=True
                                 )
            else:
                result = fit_pipeline(
                    pipeline_script=pipeline_dto.pipeline_spec,
                    automl_settings=self.automl_settings,
                    run_id=run_id,
                    X=self.input_data.X,
                    y=self.input_data.y,
                    sample_weight=self.input_data.sample_weight,
                    X_valid=self.input_data.X_valid,
                    y_valid=self.input_data.y_valid,
                    sample_weight_valid=self.input_data.sample_weight_valid,
                    cv_splits_indices=self.input_data.cv_splits_indices,
                    experiment=self._rehydrate_experiment(),
                    pipeline_id=pipeline_id,
                    remote=True,
                    logger=logger,
                    is_adb_run=True)

                log_message(logger=logger, parent_run_id=parent_run_id, worker_id=worker_id,
                            message="result : {0}".format(result))
                if len(result['errors']) > 0:
                    err_type = next(iter(result['errors']))
                    inner_ex = result['errors'][err_type]['exception']
                    log_message(logger=logger, logging_level=_logging.ERROR,
                                parent_run_id=parent_run_id, worker_id=worker_id,
                                message="exception : Type {0} InnerException {1}".format(err_type, inner_ex))
                    raise RuntimeError(inner_ex) from inner_ex

                score = result[self.automl_settings.primary_metric]
                duration = result['fit_time']
                log_message(logger=logger, parent_run_id=parent_run_id,
                            worker_id=worker_id, message="Score: {0}".format(score))
                log_message(logger=logger, parent_run_id=parent_run_id,
                            worker_id=worker_id, message="Duration: {0}".format(duration))

            # This is due to toke expiry issue
            current_run = self._rehydrate_run(run_id)
            current_run.complete()
            log_message(logger=logger, parent_run_id=parent_run_id, worker_id=worker_id,
                        message="{0}: Childrun completed successfully.".format(run_id))

        except Exception as e:
            log_message(logger=logger, logging_level=_logging.ERROR, parent_run_id=parent_run_id,
                        worker_id=worker_id, message=e)
            # This is due to toke expiry issue
            current_run = self._rehydrate_run(run_id)
            if current_run:
                current_run.fail()

    def _create_client(self, client_type):
        if(client_type == JASMINE_CLIENT):
            return JasmineClient(self.service_url, AzureMlTokenAuthentication(
                self.aml_token),
                self.subscription_id,
                self.resource_group,
                self.workspace_name,
                self.experiment_name,
                workspace_id=None,
                user_agent=client_type)
        if(client_type == RUNHISTORY_CLIENT):
            return RunHistoryClient(self.service_url, AzureMlTokenAuthentication(
                self.aml_token),
                self.subscription_id,
                self.resource_group,
                self.workspace_name,
                self.experiment_name,
                workspace_id=None,
                user_agent=client_type)

    def _refresh_aml_token(self):
        # Disabling service check, as this is in remote context and we don't have an arm token
        # we only have aml token.
        # to check arm if the workspace exists or not.
        # refresh all objects with a non expired token.
        # Below code is because aml_token can expire in an hour.
        try:
            token_obj = self.run_history_client._client.run.get_token(experiment_name=self.automl_settings.name,
                                                                      resource_group_name=self.resource_group,
                                                                      subscription_id=self.subscription_id,
                                                                      workspace_name=self.workspace_name,
                                                                      run_id=self.parent_run_id)
            self._validate_token_expiry(token_obj)
            self.aml_token = token_obj.token
            os.environ["AZUREML_RUN_TOKEN"] = self.aml_token
            self.run_history_client = self._create_client(RUNHISTORY_CLIENT)
            log_message(logger=self.logger,
                        logging_level=_logging.INFO,
                        parent_run_id=self.parent_run_id,
                        worker_id=self.worker_id,
                        message="Refreshed amltoken(hash): '{}'".format(hashlib.sha1(
                            self.aml_token.encode()).hexdigest()))
            self._refresh_time = time.time()
        except Exception as e:
            log_message(logger=self.logger, logging_level=_logging.ERROR, parent_run_id=self.parent_run_id,
                        worker_id=self.worker_id, message=e)

    def _validate_token_expiry(self, token):
        expiry_time_utc = token.expiry_time_utc.replace(tzinfo=pytz.utc)

        current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        time_delta = expiry_time_utc - current_time
        time_difference = time_delta
        time_to_expire = time_difference / datetime.timedelta(seconds=1)
        log_message(logger=self.logger, parent_run_id=self.parent_run_id,
                    worker_id=self.worker_id, message="Token expiration time(utc): {}".format(expiry_time_utc))
        if time_to_expire <= 0:
            raise Exception("Received already expired token.")

    def _start_aml_token_refresh_daemon(self, time_in_sec):
        self._auto_refresh_daemon = Daemon(
            self._refresh_aml_token, time_in_sec)
        self._auto_refresh_daemon.start()

    def _stop_aml_token_refresh_daemon(self):
        if self._auto_refresh_daemon:
            self._auto_refresh_daemon.stop()

    def __del__(self):
        self._stop_aml_token_refresh_daemon()

        """
        Clean up AutoML loggers and close files.
        """
        _logging.cleanup_log_map(
            self.automl_settings.debug_log, self.automl_settings.verbosity)
