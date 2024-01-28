import json
from dataclasses import dataclass
from typing import Any, Callable, Optional

from pydantic import BaseModel, ConfigDict, model_serializer
from pydantic_core.core_schema import SerializationInfo


class ModelConfig(ConfigDict, total=False):
    dump_exclude_none: Optional[bool]


class Model(BaseModel):
    model_config = ModelConfig(extra='allow', validate_assignment=True, validate_default=True, populate_by_name=True)

    def _model_copy(self, *, update: dict[str, Any] = {}):
        data = self.model_dump(exclude_unset=True)
        data.update(update)
        return self.__class__(**data)

    @model_serializer(mode="wrap")
    def _model_serializer(self, wrap: Callable[[Any], dict[str, Any]], info: SerializationInfo) -> dict[str, Any]:
        values = wrap(self)
        if self.model_config.get('dump_exclude_none'):
            values = {k: v for k, v in values.items() if v is not None}
        return values

    def _model_dump(self, **kwargs):
        self._model_dump_kwargs_defaults(kwargs)
        return super().model_dump(**kwargs)

    def _model_dump_json(self, **kwargs):
        self._model_dump_kwargs_defaults(kwargs)
        return super().model_dump_json(**kwargs)

    def _model_dump_kwargs_defaults(self, kwargs: dict):
        kwargs['by_alias'] = kwargs.get('by_alias', True)


Model.model_copy = Model._model_copy  # type: ignore
Model.model_dump = Model._model_dump  # type: ignore
Model.model_dump_json = Model._model_dump_json  # type: ignore


class JsonTypeError(TypeError):
    @classmethod
    def raise_error(cls, element):
        raise cls(f'Object of type {type(element)} is not JSON serializable')


def json_dump(value, *, default=JsonTypeError.raise_error, **_):
    if isinstance(value, BaseModel):
        return value.model_dump_json()
    model = Model(x=value)
    data = model.__pydantic_serializer__.to_python(model, mode='json', fallback=default)
    return json.dumps(data['x'])


def json_dump_default_str(value, **_):
    return json_dump(value, default=str)


def json_load(text):
    return json.loads(text)


@dataclass
class BusinessOut:
    reason: str
