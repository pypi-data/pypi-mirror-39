# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
    azureml/contrib/brainwave/_cli/cmd_brainwave_webservice.py,
    A file for handling BrainwaveWebservice CLI commands.
"""

import json
import os

from azureml._cli_common.cli_workspace import get_workspace
from azureml._cli_common.ml_cli_error import MlCliError
from azureml.core.webservice.webservice import Webservice
from azureml.core.model import Model
from azureml.core.image.image import Image
from azureml.contrib.brainwave.brainwave_image import BrainwaveImage
from azureml.contrib.brainwave.brainwave_webservice import BrainwaveWebservice
from azureml.exceptions import WebserviceException


def service_create_brainwavepackage(service_name, num_replicas, tags, properties, description,
                                    image_metadata_path, image_id, models, ssl_enabled,
                                    ssl_cert_pem_file, ssl_key_pem_file, workspace_name,
                                    resource_group, verbose, open_fn=open):
    if image_metadata_path:
        if image_id:
            raise MlCliError('Error, cannot specify both image_id and image_metadata_path.')

        with open_fn(image_metadata_path) as infile:
            json_metadata = json.load(infile)

        image_id = json_metadata['imageId']
        workspace_name = json_metadata['workspaceName']
        resource_group = json_metadata['resourceGroupName']

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

    workspace = get_workspace(workspace_name, resource_group)
    deployment_config = BrainwaveWebservice.deploy_configuration(num_replicas=num_replicas,
                                                                 tags=tags_dict,
                                                                 properties=properties_dict,
                                                                 description=description,
                                                                 ssl_enabled=ssl_enabled,
                                                                 ssl_certificate=ssl_cert_pem_file,
                                                                 ssl_key=ssl_key_pem_file)
    image = None
    if image_id:
        image = Image(workspace, id=image_id)
        service = Webservice.deploy_from_image(workspace, service_name, image, deployment_config)
    else:
        model_objs = []
        for model in models:
            try:
                registered_model = Model(workspace, id=model)
                model_objs.append(registered_model)
            except WebserviceException as e:
                if 'ModelNotFound' in e.message:
                    model_name = os.path.basename(model.rstrip(os.sep))[:30]
                    model_objs.append(Model.register(workspace, model, model_name))
                else:
                    raise e

        image_config = BrainwaveImage.image_configuration(tags=tags_dict,
                                                          properties=properties_dict,
                                                          description=description)

        service = Webservice.deploy_from_model(workspace, service_name, model_objs, image_config, deployment_config)
    service.wait_for_deployment(verbose)

    if service.state == 'Healthy':
        print('Service Name: {}'.format(service.name))
        print('View your service details "az ml service show -n {}'.format(service.name))
    elif service.state == 'Unhealthy':
        print('Service Name: {}'.format(service.name))
        print('Get service logs using "az ml service logs -n {}'.format(service.name))

    return service.serialize(), verbose
