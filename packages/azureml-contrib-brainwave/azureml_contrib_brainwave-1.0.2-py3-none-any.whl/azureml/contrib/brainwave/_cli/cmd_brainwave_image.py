# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" azureml/contrib/brainwave/_cli/cmd_brainwave_image.py, A file for handling BrainwaveImage CLI commands."""

import json

from azureml._cli_common.cli_workspace import get_workspace
from azureml._cli_common.ml_cli_error import MlCliError
from azureml.core.image import Image
from azureml.contrib.brainwave.brainwave_image import BrainwaveImage


def image_create_brainwavepackage_container(image_name, image_description, models, tags, properties,
                                            output_metadata_path, workspace_name,
                                            resource_group, verbose, open_fn=open):
    workspace = get_workspace(workspace_name, resource_group)
    tags_dict = None
    if tags:
        tags_dict = dict()
        for tag in tags:
            if '=' not in tag:
                raise MlCliError('Error, tags must be entered in the following format: key=value')
            key, value = tag.partition("=")[::2]
            tags_dict[key] = value

    properties_dict = None
    if properties:
        properties_dict = dict()
        for prop in properties:
            if '=' not in prop:
                raise MlCliError('Error, properties must be entered in the following format: key=value')
            key, value = prop.partition("=")[::2]
            properties_dict[key] = value

    image_config = BrainwaveImage.image_configuration(tags_dict, properties_dict, image_description)
    image = Image.create(workspace, image_name, models, image_config)
    image.wait_for_creation(verbose)

    if output_metadata_path:
        image_metadata = {'imageId': image.id, 'workspaceName': workspace_name, 'resourceGroupName': resource_group}

        with open_fn(output_metadata_path, 'w') as outfile:
            json.dump(image_metadata, outfile)

        print("Wrote JSON metadata to {}".format(output_metadata_path))

    print('Image ID: {}'.format(image.id))
    print('More details: \'az ml image show -i {}\''.format(image.id))

    return image.serialize(), verbose
