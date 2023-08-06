# Copyright (c) Microsoft Corporation. All rights reserved.
from .datasources import DataLakeDataSource
from ... import dataprep
from typing import TypeVar

DEFAULT_SAS_DURATION = 30  # this aligns with our SAS generation in the UI BlobStorageManager.ts
AML_INSTALLED = True
try:
    from azureml.core import Workspace
    from azureml.data.abstract_datastore import AbstractDatastore
    from azureml.data.azure_storage_datastore import AbstractAzureStorageDatastore, AzureFileDatastore, \
                                                     AzureBlobDatastore
    from azureml.data.azure_data_lake_datastore import AzureDataLakeDatastore
    from azureml.data.data_reference import DataReference
except ImportError:
    AML_INSTALLED = False


Datastore = TypeVar('Datastore', 'AbstractDatastore', 'DataReference')


def datastore_to_dataflow(data_source: Datastore) -> 'dataprep.Dataflow':
    from .dataflow import Dataflow
    from .engineapi.api import get_engine_api

    datastore, datastore_value = get_datastore_value(data_source)
    if isinstance(datastore, AzureBlobDatastore):
        df = Dataflow(get_engine_api())
        return df.add_step('Microsoft.DPrep.GetDatastoreFilesBlock', {
                               'datastore': datastore_value._to_pod()
                           })
    if isinstance(datastore, AzureDataLakeDatastore):
        # TODO: VSO #283878 Allow using service principal credentials for ADLS data sources
        access_token = _get_access_token(datastore)
        url = DataLakeDataSource.adl_template.format(datastore.store_name, datastore_value.path)
        return Dataflow.get_files(DataLakeDataSource(url, accessToken=access_token))

    raise NotSupportedDatastoreTypeError(datastore)


def get_datastore_value(data_source: Datastore) -> ('AbstractDatastore', 'dataprep.api.dataflow.DatastoreValue'):
    from .dataflow import DatastoreValue
    _ensure_imported()

    datastore = None
    path_on_storage = ''

    if isinstance(data_source, AbstractDatastore):
        datastore = data_source
    elif isinstance(data_source, DataReference):
        datastore = data_source.datastore
        path_on_storage = data_source.path_on_datastore or path_on_storage

    _ensure_supported(datastore)
    path_on_storage = path_on_storage.lstrip('/')

    workspace = datastore.workspace
    return (datastore, DatastoreValue(
        subscription=workspace.subscription_id,
        resource_group=workspace.resource_group,
        workspace_name=workspace.name,
        datastore_name=datastore.name,
        path=path_on_storage
    ))


def login():
    from azureml.core.authentication import InteractiveLoginAuthentication
    auth = InteractiveLoginAuthentication()
    auth.get_authentication_header()


def _ensure_imported():
    if not AML_INSTALLED:
        raise ImportError('Unable to import Azure Machine Learning SDK. In order to use datastore, please make ' \
                          + 'sure the Azure Machine Learning SDK is installed.')


def _ensure_supported(datastore: 'AbstractDatastore'):
    if isinstance(datastore, AzureFileDatastore):
        raise NotSupportedDatastoreTypeError(datastore)


def _get_access_token(datastore: 'AzureDataLakeDatastore') -> str:
    import adal # adal is a dependency of azureml-sdk not dataprep

    authority_url = '{}/{}'.format(datastore.authority_url, datastore.tenant_id)
    auth_context = adal.AuthenticationContext(authority=authority_url)
    token_obj = auth_context.acquire_token_with_client_credentials(
        resource=datastore.resource_url,
        client_id=datastore.client_id,
        client_secret=datastore.client_secret
    )
    return token_obj['accessToken']


class NotSupportedDatastoreTypeError(Exception):
    def __init__(self, datastore: 'AbstractDatastore'):
        super().__init__('Datastore "{}"\'s type "{}" is not supported.'.format(datastore.name, datastore.datastore_type))
        self.datastore = datastore
