from glob import glob
import os


def get_secrets(path='/run/secrets/*'):
    """
    return secrets, if any, as dict
    """
    secrets = {}
    for var in glob(path):
        k = var.split('/')[-1]
        v = open(var).read().rstrip('\n')
        secrets[k] = v
    return secrets


def load_secrets(secrets=get_secrets()):
    """
    loads secrets on env
    """
    os.environ.update(secrets)
