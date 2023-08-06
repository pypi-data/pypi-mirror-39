"""Classes for task whitelist model and manager."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from saltant.constants import HTTP_200_OK, HTTP_201_CREATED
from .resource import Model, ModelManager


class TaskWhitelist(Model):
    """Base model for a task whitelist.

    Attributes:
        id (int): The ID of the task whitelist.
        user (str): The user who created the task whitelist.
        name (str): The name of the task whitelist.
        description (str): The description of the task whitelist.
        whitelisted_container_task_types (list): A list of whitelisted
            container task type IDs.
        whitelisted_executable_task_types (list): A list of whitelisted
            executable task type IDs.
        manager (:class:`saltant.models.task_whitelist.TaskWhitelistManager`):
            The task whitelist manager which spawned this task whitelist.
    """

    def __init__(
        self,
        id,
        user,
        name,
        description,
        whitelisted_container_task_types,
        whitelisted_executable_task_types,
        manager,
    ):
        """Initialize a task whitelist.

        Args:
            id (int): The ID of the task whitelist.
            user (str): The user who created the task whitelist.
            name (str): The name of the task whitelist.
            description (str): The description of the task whitelist.
            whitelisted_container_task_types (list): A list of
                whitelisted container task type IDs.
            whitelisted_executable_task_types (list): A list of
                whitelisted executable task type IDs.
            manager (:class:`saltant.models.task_whitelist.TaskWhitelistManager`):
                The task whitelist manager which spawned this task instance.
        """
        # Call the parent constructor
        super(TaskWhitelist, self).__init__(manager)

        # Add in task whitelist stuff
        self.id = id
        self.user = user
        self.name = name
        self.description = description
        self.whitelisted_container_task_types = (
            whitelisted_container_task_types
        )
        self.whitelisted_executable_task_types = (
            whitelisted_executable_task_types
        )

    def __str__(self):
        """String representation of the task whitelist."""
        return self.name

    def sync(self):
        """Sync this model with latest data on the saltant server.

        Note that in addition to returning the updated object, it also
        updates the existing object.

        Returns:
            :class:`saltant.models.task_whitelist.TaskWhitelist`:
                This task whitelist instance after syncing.
        """
        self = self.manager.get(id=self.id)

        return self

    def patch(self):
        """Updates this task whitelist on the saltant server.

        This is an alias for the model's put method. (Both are identical
        operations on the model level.)

        Returns:
            :class:`saltant.models.task_whitelist.TaskWhitelist`:
                A task whitelist model instance representing the task
                whitelist just updated.
        """
        return self.put()

    def put(self):
        """Updates this task whitelist on the saltant server.

        Returns:
            :class:`saltant.models.task_whitelist.TaskWhitelist`:
                A task whitelist model instance representing the task
                whitelist just updated.
        """
        return self.manager.put(
            id=self.id,
            name=self.name,
            description=self.description,
            whitelisted_container_task_types=(
                self.whitelisted_container_task_types
            ),
            whitelisted_executable_task_types=(
                self.whitelisted_executable_task_types
            ),
        )


class TaskWhitelistManager(ModelManager):
    """Manager for task whitelists.

    Attributes:
        _client (:class:`saltant.client.Client`): An authenticated
            saltant client.
        list_url (str): The URL to list task whitelists.
        detail_url (str): The URL format to get specific task
            whitelists.
        model (:class:`saltant.models.task_whitelist.TaskWhitelist`):
            The model of the task whitelist being used.
    """

    list_url = "taskwhitelists/"
    detail_url = "taskwhitelists/{id}/"
    model = TaskWhitelist

    def get(self, id=None, name=None):
        """Get a task whitelist.

        Either the id xor the name of the task type must be specified.

        Args:
            id (int, optional): The id of the task type to get.
            name (str, optional): The name of the task type to get.

        Returns:
            :class:`saltant.models.task_whitelist.TaskWhitelist`:
                A task whitelist model instance representing the task whitelist
                requested.

        Raises:
            ValueError: Neither id nor name were set *or* both id and
                name were set.
        """
        # Validate arguments - use an xor
        if not (id is None) ^ (name is None):
            raise ValueError("Either id or name must be set (but not both!)")

        # If it's just ID provided, call the parent function
        if id is not None:
            return super(TaskWhitelistManager, self).get(id=id)

        # Try getting the task whitelist by name
        return self.list(filters={"name": name})[0]

    def create(
        self,
        name,
        description="",
        whitelisted_container_task_types=None,
        whitelisted_executable_task_types=None,
    ):
        """Create a task whitelist.

        Args:
            name (str): The name of the task whitelist.
            description (str, optional): A description of the task whitelist.
            whitelisted_container_task_types (list, optional): A list of
                whitelisted container task type IDs.
            whitelisted_executable_task_types (list, optional): A list
                of whitelisted executable task type IDs.

        Returns:
            :class:`saltant.models.task_whitelist.TaskWhitelist`:
                A task whitelist model instance representing the task
                whitelist just created.
        """
        # Translate whitelists None to [] if necessary
        if whitelisted_container_task_types is None:
            whitelisted_container_task_types = []

        if whitelisted_executable_task_types is None:
            whitelisted_executable_task_types = []

        # Create the object
        request_url = self._client.base_api_url + self.list_url
        data_to_post = {
            "name": name,
            "description": description,
            "whitelisted_container_task_types": whitelisted_container_task_types,
            "whitelisted_executable_task_types": whitelisted_executable_task_types,
        }

        response = self._client.session.post(request_url, data=data_to_post)

        # Validate that the request was successful
        self.validate_request_success(
            response_text=response.text,
            request_url=request_url,
            status_code=response.status_code,
            expected_status_code=HTTP_201_CREATED,
        )

        # Return a model instance representing the task instance
        return self.response_data_to_model_instance(response.json())

    def patch(
        self,
        id,
        name=None,
        description=None,
        whitelisted_container_task_types=None,
        whitelisted_executable_task_types=None,
    ):
        """Partially updates a task whitelist on the saltant server.

        Args:
            id (int): The ID of the task whitelist.
            name (str, optional): The name of the task whitelist.
            description (str, optional): A description of the task whitelist.
            whitelisted_container_task_types (list, optional): A list of
                whitelisted container task type IDs.
            whitelisted_executable_task_types (list, optional): A list
                of whitelisted executable task type IDs.

        Returns:
            :class:`saltant.models.task_whitelist.TaskWhitelist`:
                A task whitelist model instance representing the task
                whitelist just updated.
        """
        # Update the object
        request_url = self._client.base_api_url + self.detail_url.format(id=id)

        data_to_patch = {}

        if name is not None:
            data_to_patch["name"] = name

        if description is not None:
            data_to_patch["description"] = description

        if whitelisted_container_task_types is not None:
            data_to_patch[
                "whitelisted_container_task_types"
            ] = whitelisted_container_task_types

        if whitelisted_executable_task_types is not None:
            data_to_patch[
                "whitelisted_executable_task_types"
            ] = whitelisted_executable_task_types

        response = self._client.session.patch(request_url, data=data_to_patch)

        # Validate that the request was successful
        self.validate_request_success(
            response_text=response.text,
            request_url=request_url,
            status_code=response.status_code,
            expected_status_code=HTTP_200_OK,
        )

        # Return a model instance representing the task instance
        return self.response_data_to_model_instance(response.json())

    def put(
        self,
        id,
        name,
        description,
        whitelisted_container_task_types,
        whitelisted_executable_task_types,
    ):
        """Updates a task whitelist on the saltant server.

        Args:
            id (int): The ID of the task whitelist.
            name (str): The name of the task whitelist.
            description (str): The description of the task whitelist.
            whitelisted_container_task_types (list): A list of
                whitelisted container task type IDs.
            whitelisted_executable_task_types (list): A list of
                whitelisted executable task type IDs.

        Returns:
            :class:`saltant.models.task_whitelist.TaskWhitelist`:
                A task whitelist model instance representing the task
                whitelist just updated.
        """
        # Update the object
        request_url = self._client.base_api_url + self.detail_url.format(id=id)
        data_to_put = {
            "name": name,
            "description": description,
            "whitelisted_container_task_types": whitelisted_container_task_types,
            "whitelisted_executable_task_types": whitelisted_executable_task_types,
        }

        response = self._client.session.put(request_url, data=data_to_put)

        # Validate that the request was successful
        self.validate_request_success(
            response_text=response.text,
            request_url=request_url,
            status_code=response.status_code,
            expected_status_code=HTTP_200_OK,
        )

        # Return a model instance representing the task instance
        return self.response_data_to_model_instance(response.json())
