# pylint: disable=no-self-argument,protected-access,attribute-defined-outside-init

import dataclasses
from typing import Dict, Optional

import log
from classproperties import classproperty

from . import hooks
from .converters import Converter, map_type
from .managers import InstanceManager, ModelManager


FLAG = '_patched_init'


@dataclasses.dataclass
class ModelMeta:
    datafile_attrs: Optional[Dict[str, Converter]] = None
    datafile_pattern: Optional[str] = None

    datafile_manual: bool = False
    datafile_defaults: bool = False


class Model:

    Meta: ModelMeta = ModelMeta()

    def __post_init__(self):
        log.debug(f'Initializing {self.__class__} instance')

        with hooks.disabled():

            self.datafile = get_datafile(self)

            path = self.datafile.path
            exists = self.datafile.exists
            automatic = not self.datafile.manual

            if path:
                log.debug(f'Datafile path: {path}')
                log.debug(f'Datafile exists: {exists}')

                if exists:
                    self.datafile.load(first_load=True)
                elif path:
                    self.datafile.save()

                if automatic:
                    hooks.enable(self, self.datafile, get_datafile)

        log.debug(f'Initialized {self.__class__} instance')

    @classproperty
    def datafiles(cls) -> ModelManager:
        return ModelManager(cls)


def get_datafile(obj) -> InstanceManager:
    log.debug(f"Getting 'datafile' for {obj.__class__} instance")

    m = getattr(obj, 'Meta', None)
    pattern = getattr(m, 'datafile_pattern', None)
    attrs = getattr(m, 'datafile_attrs', None)
    manual = getattr(m, 'datafile_manual', False)
    defaults = getattr(m, 'datafile_defaults', False)

    if attrs is None:
        attrs = {}
        log.debug(f'Mapping attributes for {obj.__class__} instance')
        for field in dataclasses.fields(obj):
            self_name = f'self.{field.name}'
            if pattern is None or self_name not in pattern:
                attrs[field.name] = map_type(field.type)

    return InstanceManager(
        obj, attrs=attrs, pattern=pattern, manual=manual, defaults=defaults
    )


def create_model(cls, *, attrs=None, pattern=None, manual=None, defaults=None):
    """Patch datafile attributes on to an existing dataclass."""

    if getattr(cls, FLAG, False):
        return cls

    log.debug(f'Converting {cls} to a datafile model')

    if not dataclasses.is_dataclass(cls):
        raise ValueError(f'{cls} must be a dataclass')

    # Patch Meta

    m = getattr(cls, 'Meta', ModelMeta())

    if attrs is not None:
        m.datafile_attrs = attrs
    if pattern is not None:
        m.datafile_pattern = pattern

    if not hasattr(cls, 'Meta') and manual is not None:
        m.datafile_manual = manual
    if not hasattr(cls, 'Meta') and defaults is not None:
        m.datafile_defaults = defaults

    cls.Meta = m

    # Patch __init__

    init = cls.__init__

    def modified_init(self, *args, **kwargs):
        with hooks.disabled():
            init(self, *args, **kwargs)
        Model.__post_init__(self)

    cls.__init__ = modified_init
    cls.__init__.__doc__ = init.__doc__

    setattr(cls, FLAG, True)

    return cls
