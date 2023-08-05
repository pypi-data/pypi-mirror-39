# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azureml._cli_common.ml_cli_error import MlCliError
from azureml._cli_common.cli_workspace import get_workspace
from azureml.core.image import Image
from .iot_image import IotContainerImage
import json


def _parse_kv_list(kv_list, name):
    if not kv_list:
        return None

    kv_dict = dict()
    for kv in kv_list:
        if '=' not in kv:
            raise MlCliError('Error, %s must be entered in the following format: key=value' % name)
        key, value = kv.partition("=")[::2]
        key = key.strip()
        value = value.strip()
        if not key:
            raise MlCliError('Error, %s must be entered in the following format: key=value' % name)
        kv_dict[key] = value

    return kv_dict


def image_create_container(image_name, image_description, execution_script, architecture, dependencies, requirements,
                           docker_file, models, tags, properties, workspace_name, resource_group, verbose,
                           output_metadata_path):
    workspace = get_workspace(workspace_name, resource_group)

    tags_dict = _parse_kv_list(tags, "tags")
    properties_dict = _parse_kv_list(properties, "properties")

    image_config = IotContainerImage.image_configuration(execution_script, architecture, requirements, docker_file,
                                                         dependencies, tags_dict, properties_dict,
                                                         image_description)
    image = Image.create(workspace, image_name, models, image_config)
    image.wait_for_creation(verbose)

    if output_metadata_path:
        image_metadata = {'imageId': image.id, 'workspaceName': workspace_name, 'resourceGroupName': resource_group}

        with open(output_metadata_path, 'w') as outfile:
            json.dump(image_metadata, outfile)

        print("Wrote JSON metadata to {}".format(output_metadata_path))

    print('Image ID: {}'.format(image.id))
    print('More details: \'az ml image show -i {}\''.format(image.id))
    print('Usage information: \'az ml image usage -i {}\''.format(image.id))

    return image.serialize(), verbose
