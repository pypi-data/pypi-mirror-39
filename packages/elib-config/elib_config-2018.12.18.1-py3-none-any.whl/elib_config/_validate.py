# coding=utf-8
"""
Verifies that all configuration values have a valid setting
"""

from elib_config._setup import ELIBConfig
# noinspection PyProtectedMember
from elib_config._value._config_value import ConfigValue
# noinspection PyProtectedMember
from elib_config._value._exc import DuplicateConfigValueError, MissingValueError


def validate_config(raise_=True):
    """
    Verifies that all configuration values have a valid setting
    """
    ELIBConfig.check()
    known_paths = set()
    duplicate_values = set()
    missing_values = set()
    for config_value in ConfigValue.config_values:
        if config_value.path not in known_paths:
            known_paths.add(config_value.path)
        else:
            duplicate_values.add(config_value.name)
        try:
            config_value()
        except MissingValueError:
            missing_values.add(config_value.name)

    if raise_ and duplicate_values:
        raise DuplicateConfigValueError(str(duplicate_values))
    if raise_ and missing_values:
        raise MissingValueError(str(missing_values), 'missing config value(s)')
    return duplicate_values, missing_values
