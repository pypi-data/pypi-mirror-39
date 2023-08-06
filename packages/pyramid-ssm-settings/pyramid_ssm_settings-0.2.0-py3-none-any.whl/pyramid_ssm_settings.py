import os
import boto3


def includeme(config):
    config.add_settings(load_settings(config))
    config.add_settings(interpolate_envvars(config))


def load_settings(config):
    """
    Load settings from AWS Parameter Store.

    """
    path = _get_path(config)
    if not path:
        return
    client = boto3.client('ssm')
    next_token = None
    settings = dict()
    while True:
        kwargs = {
            'Path': path,
            'WithDecryption': True,
        }
        if next_token:
            kwargs['NextToken'] = next_token
        response = client.get_parameters_by_path(**kwargs)
        for param in response['Parameters']:
            key = param['Name'][len(path):]
            settings[key] = param['Value']
        if 'NextToken' in response:
            next_token = response['NextToken']
        else:
            break
    return settings


def _get_path(config):
    settings = config.get_settings()
    if 'ssm.path' in settings:
        return settings['ssm.path']
    elif 'SSM_PATH' in os.environ:
        return os.environ['SSM_PATH']
    else:
        return None


def interpolate_envvars(config):
    """
    Insert environment variables into settings using format minilang.

    """
    settings = config.get_settings()
    new_settings = dict()
    for key, val in settings.items():
        if isinstance(val, str) and '{' in val:
            new_settings[key] = val.format(**os.environ)
    return new_settings
