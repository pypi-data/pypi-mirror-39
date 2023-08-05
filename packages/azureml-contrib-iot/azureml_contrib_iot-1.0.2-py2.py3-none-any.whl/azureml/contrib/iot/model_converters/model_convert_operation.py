# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Waits on model convert operation for set time and retrieve the converted model
"""

import sys
import time
from requests import Session
from requests.adapters import HTTPAdapter
from azureml.exceptions import WebserviceException
from azureml.core.model import Model
from ._model_convert_client import ModelConvertClient


class ModelConvertOperation(object):
    """
    Class for tracking model convert operation and retrieve converted model.
    """

    def __init__(self, workspace, operation_id):
        """
        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param operation_id:
        :type operation_id: operation tracking model conversion
        :return:
        :rtype: None
        """

        self._workspace = None
        self._operation_id = None

        if workspace:
            self._workspace = workspace
        else:
            raise Exception('Workspace must be provided.')

        self._client = ModelConvertClient(workspace)

        if operation_id:
            self._operation_id = operation_id
        else:
            raise Exception('Operation id must be provided.')

    def _is_terminal_state(self, operation_state):
        """
        Helper method to check the operation state.

        :param operation_state: convert model operation state
        :type operation_state: str
        :return: true if terminal state otherwise false
        :rtype: bool
        """

        is_terminated = False
        if operation_state == 'Cancelled' or operation_state == 'Succeeded' or operation_state == 'Failed' \
                or operation_state == 'TimedOut':
            is_terminated = True

        return is_terminated

    def _write_operation_log(self, operation_state, content):
        """
        Helper method to write operation log.

        :param operation_state: convert model operation state
        :type operation_state: str
        :param content: convert model operation result
        :type content: object
        :return:
        :rtype: None
        """

        sys.stdout.write('\nOperation {} completed, operation state "{}"'
                         .format(self._operation_id, operation_state))

        log_location = content['operationLog'] if 'operationLog' in content else None
        if log_location:
            sys.stdout.write('\nsas url to download model conversion logs {}\n'.format(log_location))
            with Session() as session:
                session.mount('https://', HTTPAdapter(max_retries=0))
                response = session.get(log_location, stream=True)
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        sys.stdout.write(chunk)

        if operation_state == 'Failed':
            error = content['error'] if 'error' in content else None
            if error and 'statusCode' in error and 'message' in error:
                sys.stdout.write('\nModel convert failed with\n'
                                 'StatusCode: {}\n'
                                 'Message: {}\n'.format(error['statusCode'], error['message']))
            else:
                sys.stdout.write('\nModel convert failed, unexpected error response:\n'
                                 '{}'.format(error))

        sys.stdout.flush()

    def wait_for_completion(self, show_output=False, timeout=None):
        """
        Wait for the model to be converted to the requested flavor.

        :param show_output: Boolean option to print more verbose output
        :type show_output: bool
        :param timeout: If None wait until operation is done
        :type timeout: int
        :return: True if operation completed and succeeded.
        :rtype: bool
        """

        start_time = time.monotonic()
        operation_state, content = self._client.get_operation_state(self._operation_id)
        current_state = operation_state
        if show_output:
            sys.stdout.write('{}'.format(current_state))
            sys.stdout.flush()

        # check operation progress until the operation terminated or timeout
        while not self._is_terminal_state(operation_state):
            if timeout is not None:
                if time.monotonic() - start_time > timeout:
                    break

            time.sleep(5)
            operation_state, content = self._client.get_operation_state(self._operation_id)
            if show_output:
                sys.stdout.write('.')
                if operation_state != current_state:
                    sys.stdout.write('\n{}'.format(operation_state))
                    current_state = operation_state
                sys.stdout.flush()

        # if operation state terminated show operation details
        if self._is_terminal_state(operation_state):
            self._write_operation_log(operation_state, content)

        if operation_state == 'Succeeded':
            return True

        return False

    @property
    def result(self):
        """
        If the model conversion completed return the converted model.

        :return: converted model if convert model operation succeeded.
        :rtype: azureml.core.model
        """
        operation_state, content = self._client.get_operation_state(self._operation_id)

        if operation_state == 'Succeeded':
            if 'resourceLocation' in content:
                resource_location = content['resourceLocation']
                model_id = resource_location.split('/')[-1]
                return Model(self._workspace, id=model_id)
            else:
                raise WebserviceException('Invalid operation payload, missing resourceLocation:\n'
                                          '{}'.format(resource_location))
        elif operation_state == 'Cancelled' or operation_state == 'Failed' or operation_state == 'TimedOut':
            raise ValueError("Model conversion is not successful")
        else:
            raise ValueError("Model conversion is not complete")

    @property
    def get_status(self):
        """
        Get the status of the convert model operation.

        :return: Status of the convert model operation.
        :rtype: str
        """
        operation_state = self._client.get_operation_state(self._operation_id)

        if operation_state == 'Succeeded':
            return "Succeeded"
        elif operation_state == 'Cancelled' or operation_state == 'Failed' or operation_state == 'TimedOut':
            return "Failed"

        return "InProgess"
