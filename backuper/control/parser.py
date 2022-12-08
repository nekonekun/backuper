from backuper.db.schema import Base, Model, Method, Subnet, DistinctDevice
import yaml
from typing import Type
from backuper.errors import ParseError

models = {
    'method': Method,
    'model': Model,
    'subnet': Subnet,
    'distinct_device': DistinctDevice,
}


def load_one_object(source: dict) -> Base:
    model = source.pop('type')
    if not model:
        raise ParseError('No type provided')
    if model not in models:
        raise ParseError('Unknown config type')
    try:
        obj = models[model](**source)
    except Exception as err:
        raise ParseError(err)
    return obj


def load_config_objects(filename: str) -> list[Base]:
    with open(filename) as source_file:
        try:
            source = yaml.safe_load(source_file)
        except yaml.YAMLError as exc:
            raise ParseError(exc)
    if isinstance(source, list):
        possible_objs = source
    else:
        possible_objs = [source]
    return list(map(load_one_object, possible_objs))
