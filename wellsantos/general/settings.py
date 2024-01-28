import os
from typing import Dict, List, Optional, Type

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..dependency.factory import use
from ..dependency.subclass import Subclass
from .model import Model, ModelConfig


class SettingsModelConfig(ModelConfig, SettingsConfigDict, total=False):  # type: ignore
    pass


class Settings(Model, BaseSettings):
    model_config = SettingsModelConfig(**(BaseSettings.model_config | Model.model_config))

    def __init__(self, *args, **kwargs):
        BaseSettings.__init__(self, *args, **kwargs)
        env_prefix = self.model_config['env_prefix']
        # TODO: move this 2 IFs below to a unit-test assert
        if env_prefix.find('{') >= 0:
            raise RuntimeError(
                f"env_prefix has unresolved placeholders: {self.__class__}: {self.model_config['env_prefix']}"
            )
        if not env_prefix.endswith('_'):
            raise RuntimeError(
                f"env_prefix is missing the ending underscore: {self.__class__}: {self.model_config['env_prefix']}"
            )

    def settings_customise_sources(cls, settings_cls, **kwargs):
        result = {}
        sources = list(x() for x in kwargs.values())
        cls._model_inherit_env(sources)

        for source in reversed(sources):
            for k, v in source.items():
                if v in (None, ''):
                    continue
                result[k] = v

        for k in cls.__annotations__:
            if k not in result:
                if os.getenv(f'DEFAULT_NONE_{cls.model_config["env_prefix"]}{k}'.upper(), '').lower() == 'true':
                    result[k] = None
                elif os.getenv(f'DEFAULT_EMPTY_{cls.model_config["env_prefix"]}{k}'.upper(), '').lower() == 'true':
                    result[k] = ''

        return [lambda: result]

    @classmethod
    def _model_inherit_env(cls, sources: List[Dict]):
        done_env = {'', cls.model_config['env_prefix']}
        target = Subclass.root(cls)
        bases: List[Type] = list(target.__bases__)
        while bases:
            parent = bases.pop(0)
            if not issubclass(parent, Settings):
                continue
            env_prefix = parent.model_config['env_prefix']
            if env_prefix in done_env:
                continue
            try:
                ancestor = use(parent._as_ancestor_of(cls))
            except ValidationError:
                # TODO: we need to give support to have "required" fields in parent Settings
                #  bases.extend(parent.__bases__)
                #  continue
                raise
            sources.append(ancestor.model_dump(exclude_unset=True))

    @classmethod
    def _as_ancestor_of(cls, descendant: Type['Settings']):
        outer_prefix = descendant._outer_prefix
        env_prefix = cls.model_config['env_prefix'].format(outer_prefix=outer_prefix())
        return Subclass.of(cls, model_config=SettingsConfigDict(env_prefix=env_prefix), _outer_prefix=outer_prefix)

    @classmethod
    def as_subconfig_of(cls, outer: Type['Settings']):
        outer_prefix = outer.model_config['env_prefix']
        env_prefix = cls.model_config['env_prefix'].format(outer_prefix=outer_prefix)
        return Subclass.of(
            cls, model_config=SettingsConfigDict(env_prefix=env_prefix), _outer_prefix=lambda: outer_prefix
        )

    @classmethod
    def with_env_prefix(cls, env_prefix: Optional[str]):
        return cls if env_prefix is None else Subclass.of(cls, model_config=SettingsConfigDict(env_prefix=env_prefix))

    @classmethod
    def _outer_prefix(cls):
        return ''
