from django.conf import settings
from django.utils.module_loading import import_string

KIP_SETTINGS = getattr(settings, 'KIP', {})


def get_setting(setting_name, default):
    return KIP_SETTINGS.get(setting_name) or default


DocumentStorageClass = import_string(get_setting(
    'DOCUMENT_STORAGE_CLASS', 'ipfs_storage.InterPlanetaryFileSystemStorage'
))
