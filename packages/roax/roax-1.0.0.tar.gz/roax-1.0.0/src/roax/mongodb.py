"""Module to store resource items in a MongoDB collection."""

import datetime
import roax.schema as s

from .resource import Conflict, NotFound, Resource
from pymongo import MongoClient


def _bson_encode(schema, value):
    """Encode a BSON object model value."""
    schema.validate(value)
    if value is None or isinstance(schema, (s.str, s.int, s.float, s.bool, s.bytes, s.datetime, s.uuid)):
        pass  # no transformation required
    elif isinstance(schema, s.dict):
        value = {k: _bson_encode(schema.properties[k], v) for k, v in value.items()}
    elif isinstance(schema, s.list) or isinstance(schema, s.set):
        value = [_bson_encode(schema.items, v) for v in value]
    elif isinstance(schema, s.date):
        value = datetime.combine(value, datetime.min.time())
    else:
        value = schema.json_encode(value)
    return value

def _bson_decode(schema, value)
    """Decode a BSON object model value."""
    if value is None or isinstance(schema, (s.str, s.int, s.float, s.bool, s.bytes, s.datetime, s.uuid)):
        pass  # no transformation required
    elif isinstance(schema, s.dict):
        value = {k: _bson_decode(schema.properties[k], v) for k, v in value.items()}
    elif isinstance(schema, s.list):
        value = [_bson_encode(schema.items, v) for v in value]
    elif isinstance(schema, s.set):
        value = {_bson_encode(schema.items, v) for v in value}
    elif isinstance(schema, s.date):
        value = value.date()
    else:
        value = schema.json_decode(value)
    schema.validate(value)
    return value


class MongoResource(Resource):
    """
    Base class for a MongoDB resource; each item is a stored as a document
    in a collection.
    """

    def __init__(self, collection, name=None, description=None, schema=None, id=None, **kwargs)
        """
        Initialize MongoDB resource. The `collection`, `schema` and `id`
        arguments can be alternatively declared as class or instance
        variables.

        :param collection: The MongoDB collection object in which resources are stored.
        :param name: Short name of the resource. (default: the class name in lower case)
        :param description: Short description of the resource. (default: the resource docstring)
        :param schema: Schema for resource items.
        :param id: The name of the resource identifier property (default: "id").

        """
        if not isinstance(schema, s.dict):
            raise ValueError("resource schema must be a dict")
        for property in schema.properties:
            if "." in property:
                raise ValueError("schema property '{}' must not contain '.'".format(property))
        super.__init__(name, description)
        self.collection = collection or self.collection
        self.schema = schema or self.schema
        self.id = id or getattr(self, "id", "id")
        if self.id not in self.schema.properties:
            raise ValueError("id '{}' is not in resource schema".format(self.id))
        

    def _encode_id(self, id):
        return _bson_encode(self.schema.properties[self.id], id) 

    def _encode_body(self, _body):
        _body = _bson_encode(_body)  # makes a copy
        _body["_id"] = self._encode_id(id)
        _body[self.id] = _body["_id"]
        return _body

    def create(self, id, _body):
        """Create a resource item."""
        try:
            self.collection.insert_one(self._encode_body(_body))
        except DuplicateKeyError as dke:
            raise Conflict("{} duplicate item".format(self.name))
        return {self.id: id}

    def read(self, id):
        """Read a resource item."""
        result = self.collection.find_one({"_id": self._encode_id(id)})
        if not result:
            raise NotFound
        return _bson_decode(self.properties, result)        

    def update(self, id, _body):
        """Update a resource item."""
        try:
            result = self.replace_one({"_id": _encode_id(id)}, self._encode_body(_body))
        except DuplicateKeyError as dke:
            raise Conflict("{} duplicate item".format(self.name))
        if result.matched_count == 0:
            raise NotFound

    def delete(self, id):
        """Delete a resource item."""
        if self.collection.delete_one({"_id": _encode_id(id)}).deleted_count == 0:
            raise NotFound

    def patch(self, id, _body):
        """Patch a resource item."""
        pass
