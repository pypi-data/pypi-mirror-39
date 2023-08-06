import json
from collections import Callable
from dataclasses import dataclass, field
from typing import Union, List, Any

from validate_it import Schema, Validator

from perestroika.db_layers import DbLayer, DjangoDbLayer
from perestroika.deserializers import Deserializer, DjangoDeserializer
from perestroika.exceptions import RestException, ValidationException, BadRequest
from perestroika.serializers import Serializer, DjangoSerializer


class DenyAll(Schema):
    pass


@dataclass
class Method:
    mode: str = 'django'

    query: Any = None
    queryset: Any = None
    db_layer: Union[DbLayer, None] = None

    serializer: Union[Serializer, None] = None
    deserializer: Union[Deserializer, None] = None

    skip_query_db: bool = False

    input_validator: Validator = field(default_factory=DenyAll)
    output_validator: Validator = field(default_factory=DenyAll)

    pre_query_hooks: List[Callable] = field(default_factory=list)
    post_query_hooks: List[Callable] = field(default_factory=list)

    request_hooks: List[Callable] = field(default_factory=list)
    response_hooks: List[Callable] = field(default_factory=list)

    def __post_init__(self):
        if self.mode == 'django':
            query_field_name = 'queryset'

            # allow custom db layers
            if not isinstance(self.db_layer, DjangoDbLayer):
                self.db_layer = DjangoDbLayer()

            # allow custom serializers
            if not isinstance(self.serializer, DjangoSerializer):
                self.serializer = DjangoSerializer()

            # allow custom deserializers
            if not isinstance(self.deserializer, DjangoDeserializer):
                self.deserializer = DjangoDeserializer()

        if getattr(self, query_field_name) is None and not self.skip_query_db:
            raise ValueError(f"Empty `{query_field_name}` is allowed only for resources with `skip_query_db` == True")

    def __set_name__(self, owner, name):
        if not owner.methods:
            owner.methods = {}

        if self.__class__.__name__.lower() != name.lower():
            raise ValueError("Wrong name for method: method name must be equal with `Method` instance class name")

        owner.methods[name.lower()] = self

    def schema(self):
        return {
            "output_schema": self.output_validator.representation()
        }

    def get_client_data(self, request):
        return self.deserializer.deserialize(request, self)

    def query_db(self, bundle):
        raise NotImplementedError()

    @staticmethod
    def validate(validator: Schema, bundle, strip_unknown=False):
        _errors = []
        _objects = []

        for _object in bundle["items"]:
            _error, _object = validator.validate_it(_object, convert=True, strip_unknown=strip_unknown)

            if _error:
                _errors.append(_error)
            else:
                _objects.append(_object)

        if _errors:
            raise ValidationException(message=json.dumps({"errors": _errors, "items": bundle["items"]}))

        bundle["items"] = _objects

    def validate_input(self, bundle):
        self.validate(self.input_validator, bundle, strip_unknown=False)

    def validate_output(self, bundle):
        self.validate(self.output_validator, bundle, strip_unknown=True)

    @staticmethod
    def apply_hooks(hooks, request, bundle):
        for hook in hooks:
            hook(request, bundle)

    def apply_pre_query_hooks(self, request, bundle):
        self.apply_hooks(self.pre_query_hooks, request, bundle)

    def apply_post_query_hooks(self, request, bundle):
        self.apply_hooks(self.post_query_hooks, request, bundle)

    def set_default_success_code(self, bundle):
        raise NotImplementedError()

    def apply_request_hooks(self, request, bundle):
        self.apply_hooks(self.request_hooks, request, bundle)

    def apply_response_hooks(self, request, bundle):
        self.apply_hooks(self.response_hooks, request, bundle)

    def handle(self, request):
        try:
            bundle = self.get_client_data(request)
        except BadRequest as e:
            bundle = {
                'error_code': -1,
                'error_message': e.message,
                'status_code': e.status_code
            }
            return self.serializer.serialize(request, bundle)

        self.set_default_success_code(bundle)
        self.apply_request_hooks(request, bundle)

        try:
            try:
                self.validate_input(bundle)
            except ValidationException as e:
                raise RestException(message=e.message)

            self.apply_pre_query_hooks(request, bundle)

            if not self.skip_query_db:
                self.query_db(bundle)

            self.apply_post_query_hooks(request, bundle)

            try:
                self.validate_output(bundle)
            except ValidationException as e:
                raise RestException(message=e.message)

        except RestException as e:
            bundle['error_code'] = -1
            bundle['error_message'] = e.message
            bundle['status_code'] = e.status_code

        self.apply_response_hooks(request, bundle)

        return self.serializer.serialize(request, bundle)


@dataclass
class CanFilterAndExclude(Method):
    filter_validator: Validator = field(default_factory=DenyAll)
    exclude_validator: Validator = field(default_factory=DenyAll)

    def set_default_success_code(self, bundle):
        raise NotImplementedError()

    def query_db(self, bundle):
        raise NotImplementedError()

    def schema(self):
        _schema = super().schema()
        _schema["filter_schema"] = self.filter_validator.representation()
        _schema["exclude_schema"] = self.exclude_validator.representation()
        return _schema


@dataclass
class NoBodyNoObjectsNoInput(CanFilterAndExclude):
    def set_default_success_code(self, bundle):
        raise NotImplementedError()

    def validate_input(self, bundle):
        """ Void validation because no input data"""
        pass

    def query_db(self, bundle):
        raise NotImplementedError()


@dataclass
class Get(NoBodyNoObjectsNoInput):
    def query_db(self, bundle):
        self.db_layer.get(bundle, self)

    def set_default_success_code(self, bundle):
        bundle["status_code"] = 200


@dataclass
class Post(Method):
    input_validator: Validator = field(default_factory=DenyAll)

    def query_db(self, bundle):
        self.db_layer.post(bundle, self)

    def schema(self):
        _schema = super().schema()
        _schema["input_schema"] = self.input_validator.representation()
        return _schema

    def set_default_success_code(self, bundle):
        bundle["status_code"] = 201


@dataclass
class Put(CanFilterAndExclude):
    def query_db(self, bundle):
        raise NotImplementedError()

    input_validator: Validator = field(default_factory=DenyAll)

    def set_default_success_code(self, bundle):
        raise NotImplementedError()

    def schema(self):
        _schema = super().schema()
        _schema["input_schema"] = self.input_validator.representation()
        return _schema


@dataclass
class Patch(CanFilterAndExclude):
    input_validator: Validator = field(default_factory=DenyAll)

    def query_db(self, bundle):
        raise NotImplementedError()

    def set_default_success_code(self, bundle):
        raise NotImplementedError()

    def schema(self):
        _schema = super().schema()
        _schema["input_schema"] = self.input_validator.representation()
        return _schema


@dataclass
class Delete(NoBodyNoObjectsNoInput):
    def query_db(self, bundle):
        raise NotImplementedError()

    def set_default_success_code(self, bundle):
        raise NotImplementedError()
