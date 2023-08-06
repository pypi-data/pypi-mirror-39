import json
import time

from schematics import Model, types


class CustomSchematicsModel(Model):

    def to_json(self, *args, **kwargs):
        json_kwargs = kwargs.pop('json_kwargs', {})
        return json.dumps(self.to_primitive(*args, **kwargs), **json_kwargs)


class BaseMeasurement(CustomSchematicsModel):
    ts = types.IntType(default=lambda: int(time.time()), required=True)
