"""
This module contains utility functions for api_server app
"""

import environ

def get_env(env_var_name):
    """
    If present, returns environment variable value, if not - raises
    'ImproperlyConfigured'
    """

    env = environ.Env()
    environ.Env.read_env()
    return env(env_var_name)
