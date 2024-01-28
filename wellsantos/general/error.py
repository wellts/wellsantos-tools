class InconsistencyError(RuntimeError):
    pass


class NoneValueIsNotAllowedError(ValueError):
    pass


class ModelSchemaError(ValueError):
    def __init__(self, model: dict, model_id=None):
        self.model = model
        self.model_id = model_id


class SkippedError(RuntimeError):
    pass
