__all__ = "Swagger"
__version__ = "0.0.1"
__author__ = "Valetov Konstantin"

import functools
import typing
import enum
import operator
from collections import defaultdict

import yaml
import attr
import jinja2
from aiohttp import web, hdrs
from openapi_spec_validator import validate_v3_spec


# TODO parameter as $ref inside
# $ref in $ref?


class _MissingType:
    pass


MISSING = _MissingType()

_SWAGGER_INDEX_HTML = "SWAGGER_INDEX_HTML"
_SWAGGER_SPECIFICATION = "SWAGGER_SPECIFICATION"


async def application_json(request: web.Request) -> typing.Dict:
    return await request.json()


async def _swagger_home(request):
    return web.Response(text=request.app[_SWAGGER_INDEX_HTML], content_type="text/html")


async def _swagger_spec(request):
    return web.json_response(request.app[_SWAGGER_SPECIFICATION])


async def _redirect(request: web.Request):
    return web.HTTPMovedPermanently(f'{request.path}/')


def str_to_int(value: str) -> int:
    return int(value)


def str_to_float(value: str) -> float:
    return float(value)


@attr.attrs(slots=True, auto_attribs=True)
class ValidatorError(Exception):
    error: typing.Union[str, typing.Dict]


@attr.attrs(slots=True, frozen=True, auto_attribs=True)
class Validator:
    def validate(self, value: typing.Any, raw: bool) -> typing.Any:
        raise NotImplementedError


class IntegerFormat(enum.Enum):
    Int32 = 'int32'
    Int64 = 'int64'


class NumberFormat(enum.Enum):
    Float = 'float'
    Double = 'double'


@attr.attrs(slots=True, frozen=True, cmp=False, kw_only=True, auto_attribs=True)
class Integer(Validator):
    format: IntegerFormat = attr.attrib(converter=IntegerFormat)
    minimum: typing.Optional[int] = None
    maximum: typing.Optional[int] = None
    exclusiveMinimum: bool = False
    exclusiveMaximum: bool = False
    enum: typing.Optional[typing.List[int]] = None
    nullable: bool = False
    default: typing.Optional[int] = None

    def validate(self, raw_value: typing.Union[None, int, str, _MissingType], raw: bool) -> typing.Optional[int]:
        if isinstance(raw_value, str):
            if not raw:
                raise ValidatorError("value should be type of int")
            try:
                value = int(raw_value)
            except ValueError:
                raise ValidatorError("value should be type of int")
        elif isinstance(raw_value, int) and not isinstance(raw_value, bool):
            value = raw_value
        elif raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of int")
        elif isinstance(raw_value, _MissingType):
            if self.default is None:
                return raw_value
            value = self.default
        else:
            raise ValidatorError("value should be type of int")
        if self.format == IntegerFormat.Int32 and not -2_147_483_648 <= value <= 2_147_483_647:
            raise ValidatorError("value out of bounds int32")

        if self.minimum is not None:
            op = operator.le if self.exclusiveMinimum else operator.lt
            if op(value, self.minimum):
                raise ValidatorError(
                    f"value should be more than{'' if self.exclusiveMinimum else ' or equal to'} {self.minimum}")
        if self.maximum is not None:
            op = operator.ge if self.exclusiveMaximum else operator.gt
            if op(value, self.maximum):
                raise ValidatorError(
                    f"value should be less than{'' if self.exclusiveMaximum else ' or equal to'} {self.maximum}")
        if self.enum is not None and value not in self.enum:
            raise ValidatorError(f"value should be one of {self.enum}")
        return value


@attr.attrs(slots=True, frozen=True, cmp=False, kw_only=True, auto_attribs=True)
class Number(Validator):
    format: NumberFormat = attr.attrib(converter=NumberFormat)
    minimum: typing.Optional[float] = None
    maximum: typing.Optional[float] = None
    exclusiveMinimum: bool = False
    exclusiveMaximum: bool = False
    enum: typing.Optional[typing.List[float]] = None
    nullable: bool = False
    default: typing.Optional[float] = None

    def validate(self, raw_value: typing.Union[None, int, float, str], raw: bool) -> typing.Optional[float]:
        if isinstance(raw_value, str):
            if not raw:
                raise ValidatorError("value should be type of float")
            try:
                value = float(raw_value)
            except ValueError:
                raise ValidatorError("value should be type of float")
        elif isinstance(raw_value, float):
            value = raw_value
        elif isinstance(raw_value, int) and not isinstance(raw_value, bool):
            value = float(raw_value)
        elif raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of float")
        elif isinstance(raw_value, _MissingType):
            if self.default is None:
                return raw_value
            value = self.default
        else:
            raise ValidatorError("value should be type of float")

        if self.minimum is not None:
            op = operator.le if self.exclusiveMinimum else operator.lt
            if op(value, self.minimum):
                raise ValidatorError(
                    f"value should be more than{'' if self.exclusiveMinimum else ' or equal to'} {self.minimum}")
        if self.maximum is not None:
            op = operator.ge if self.exclusiveMaximum else operator.gt
            if op(value, self.maximum):
                raise ValidatorError(
                    f"value should be less than{'' if self.exclusiveMaximum else ' or equal to'} {self.maximum}")
        if self.enum is not None and value not in self.enum:
            raise ValidatorError(f"value should be one of {self.enum}")
        return value


@attr.attrs(slots=True, frozen=True, cmp=False, kw_only=True, auto_attribs=True)
class String(Validator):
    minLength: typing.Optional[int] = None
    maxLength: typing.Optional[int] = None
    enum: typing.Optional[typing.List[str]] = None
    nullable: bool = False
    default: typing.Optional[str] = None

    def validate(self, raw_value: typing.Optional[str], raw: bool) -> typing.Optional[str]:
        if isinstance(raw_value, str):
            value = raw_value
        elif raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of str")
        elif isinstance(raw_value, _MissingType):
            if self.default is None:
                return raw_value
            value = self.default
        else:
            raise ValidatorError("value should be type of str")

        if self.minLength is not None and len(value) < self.minLength:
            raise ValidatorError(f"value length should be more than {self.minLength}")
        if self.maxLength is not None and len(value) > self.maxLength:
            raise ValidatorError(f"value length should be less than {self.maxLength}")
        if self.enum is not None and value not in self.enum:
            raise ValidatorError(f"value should be one of {self.enum}")
        return value


@attr.attrs(slots=True, frozen=True, cmp=False, kw_only=True, auto_attribs=True)
class Boolean(Validator):
    nullable: bool = False
    default: typing.Optional[bool] = None

    def validate(self, raw_value: typing.Union[None, bool, str], raw: bool) -> typing.Optional[bool]:
        if isinstance(raw_value, str):
            if not raw:
                raise ValidatorError("value should be type of bool")
            if raw_value == 'true':
                value = True
            elif raw_value == 'false':
                value = False
            else:
                raise ValidatorError("value should be type of bool")
        elif isinstance(raw_value, bool):
            value = raw_value
        elif raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of bool")
        elif isinstance(raw_value, _MissingType):
            if self.default is None:
                return raw_value
            value = self.default
        else:
            raise ValidatorError("value should be type of bool")
        return value


@attr.attrs(slots=True, frozen=True, cmp=False, kw_only=True, auto_attribs=True)
class Array(Validator):
    validator: Validator
    uniqueItems: bool
    minItems: typing.Optional[int] = None
    maxItems: typing.Optional[int] = None
    nullable: bool = False

    def validate(self, raw_value: typing.Union[None, str, typing.List],
                 raw: bool) -> typing.Optional[typing.List]:
        if isinstance(raw_value, str):
            if not raw:
                raise ValidatorError("value should be type of list")
            items = [self.validator.validate(value, raw) for value in raw_value.split(',')]
        elif isinstance(raw_value, list):
            items = raw_value
        elif raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of list")
        else:
            raise ValidatorError("value should be type of list")

        if self.minItems is not None and len(items) < self.minItems:
            raise ValidatorError(f"number or items must be more than {self.minItems}")
        if self.maxItems is not None and len(items) > self.maxItems:
            raise ValidatorError(f"number or items must be less than {self.maxItems}")
        if self.uniqueItems and len(items) != len(set(items)):
            raise ValidatorError("all items must be unique")
        return items


@attr.attrs(slots=True, frozen=True, cmp=False, kw_only=True, auto_attribs=True)
class Object(Validator):
    properties: typing.Dict[str, Validator]
    required: typing.Set[str]
    minProperties: typing.Optional[int] = None
    maxProperties: typing.Optional[int] = None
    additionalProperties: typing.Union[bool, Validator] = True
    nullable: bool = False

    def validate(self, raw_value: typing.Optional[typing.Dict], raw: bool) -> typing.Optional[typing.Dict]:
        if raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of dict")
        elif not isinstance(raw_value, dict):
            raise ValidatorError("value should be type of dict")
        value = {}
        errors = {}
        for name in self.required:
            if name not in raw_value:
                errors[name] = "required property"
        if errors:
            raise ValidatorError(errors)

        for name, validator in self.properties.items():
            prop = raw_value.get(name, MISSING)
            try:
                val = validator.validate(prop, raw)
                if val != MISSING:
                    value[name] = val
            except ValidatorError as e:
                errors[name] = e.error
        if errors:
            raise ValidatorError(errors)

        if isinstance(self.additionalProperties, bool):
            if not self.additionalProperties:
                additional_properties = raw_value.keys() - value.keys()
                if additional_properties:
                    raise ValidatorError({k: "additional property not allowed" for k in additional_properties})
            else:
                for key in raw_value.keys() - value.keys():
                    value[key] = raw_value[key]
        else:
            for name in raw_value.keys() - value.keys():
                validator = self.additionalProperties
                value[name] = validator.validate(raw_value[name], raw)
        if self.minProperties is not None and len(value) < self.minProperties:
            raise ValidatorError(f"number or properties must be more than {self.minProperties}")
        if self.maxProperties is not None and len(value) > self.maxProperties:
            raise ValidatorError(f"number or properties must be less than {self.maxProperties}")
        return value


@attr.attrs(slots=True, frozen=True, cmp=False, kw_only=True, auto_attribs=True)
class OneOf(Validator):
    validators: typing.List[Validator]

    def validate(self, raw_value: typing.Any, raw: bool) -> typing.Any:
        found = False
        value = None
        for validator in self.validators:
            try:
                value = validator.validate(raw_value, raw)
            except ValidatorError:
                continue
            if found:
                raise ValidatorError("fail to validate oneOf")
            found = True
        if not found:
            raise ValidatorError("fail to validate oneOf")
        return value


@attr.attrs(slots=True, frozen=True, cmp=False, kw_only=True, auto_attribs=True)
class AnyOf(Validator):
    validators: typing.List[Validator]

    def validate(self, raw_value: typing.Any, raw: bool) -> typing.Any:
        for validator in self.validators:
            try:
                return validator.validate(raw_value, raw)
            except ValidatorError:
                pass
        raise ValidatorError("fail to validate anyOf")


@attr.attrs(slots=True, frozen=True, cmp=False, kw_only=True, auto_attribs=True)
class AllOf(Validator):
    validators: typing.List[Validator]

    def validate(self, raw_value: typing.Any, raw: bool) -> typing.Any:
        value = {}
        for validator in self.validators:
            try:
                value.update(validator.validate(raw_value, raw))
            except ValidatorError:
                raise ValidatorError("fail to validate allOf")
        # for key in raw_value.keys() - value.keys():
        #     value[key] = raw_value[key]
        return value


def _type_to_validator(schema: typing.Dict, components: typing.Dict) -> Validator:
    if 'type' not in schema:
        raise KeyError("type is required")
    if schema['type'] == 'integer':
        return Integer(
            nullable=schema.get('nullable', False),
            minimum=schema.get('minimum'),
            maximum=schema.get('maximum'),
            exclusiveMinimum=schema.get('exclusiveMinimum', False),
            exclusiveMaximum=schema.get('exclusiveMaximum', False),
            enum=schema.get('enum'),
            format=schema.get('format', IntegerFormat.Int64),
            default=schema.get('default'),
        )
    elif schema['type'] == 'number':
        return Number(
            nullable=schema.get('nullable', False),
            minimum=schema.get('minimum'),
            maximum=schema.get('maximum'),
            exclusiveMinimum=schema.get('exclusiveMinimum', False),
            exclusiveMaximum=schema.get('exclusiveMaximum', False),
            enum=schema.get('enum'),
            format=schema.get('format', NumberFormat.Double),
            default=schema.get('default'),
        )
    elif schema['type'] == 'string':
        return String(
            nullable=schema.get('nullable', False),
            minLength=schema.get('minLength'),
            maxLength=schema.get('maxLength'),
            enum=schema.get('enum'),
            default=schema.get('default'),
        )
    elif schema['type'] == 'boolean':
        return Boolean(
            nullable=schema.get('nullable', False),
            default=schema.get('default'),
        )
    elif schema['type'] == 'array':
        return Array(
            nullable=schema.get('nullable', False),
            validator=schema_to_validator(schema['items'], components),
            uniqueItems=schema.get('uniqueItems'),
            minItems=schema.get('minItems'),
            maxItems=schema.get('maxItems')
        )
    elif schema['type'] == 'object':
        # TODO move this logic to class?
        properties = {k: schema_to_validator(v, components) for k, v in schema.get('properties', {}).items()}
        raw_additional_properties = schema.get('additionalProperties', True)
        if isinstance(raw_additional_properties, dict):
            additional_properties = schema_to_validator(raw_additional_properties, components)
        else:
            additional_properties = raw_additional_properties
        return Object(
            nullable=schema.get('nullable', False),
            properties=properties,
            required=set(schema.get('required', [])),
            minProperties=schema.get('minProperties'),
            maxProperties=schema.get('maxProperties'),
            additionalProperties=additional_properties,
        )
    else:
        raise Exception(f"Unknown type '{schema['type']}'")


def schema_to_validator(schema: typing.Dict, components: typing.Dict) -> Validator:
    if '$ref' in schema:
        if not components:
            raise Exception("file with components definitions is missing")
        # #/components/schemas/Pet
        _, component, section, obj = schema['$ref'].split('/')
        schema = components[component][section][obj]
    if 'oneOf' in schema:
        return OneOf(validators=[_type_to_validator(sch, components) for sch in schema['oneOf']])
    elif 'anyOf' in schema:
        return AnyOf(validators=[_type_to_validator(sch, components) for sch in schema['anyOf']])
    elif 'allOf' in schema:
        return AllOf(validators=[_type_to_validator(sch, components) for sch in schema['allOf']])
    else:
        return _type_to_validator(schema, components)


@attr.attrs(slots=True, auto_attribs=True)
class Parameter:
    name: str
    validator: Validator
    required: bool


TEMPLATE = """openapi: 3.0.0
info:
  title: {{ title }}
  version: {{ version }}
{% if description %}
  description: {{ description }}
{% endif %}"""


class Swagger:
    def __init__(self, app: web.Application, ui_path: str, *, title: str = "OpenAPI3", version: str = "1.0.0",
                 description: typing.Optional[str] = None, components: typing.Optional[str] = None) -> None:
        if not ui_path.startswith('/'):
            raise Exception('ui_path should start with /')
        ui_path = ui_path.rstrip('/')
        self._app = app
        self._spec = yaml.load(jinja2.Template(TEMPLATE).render({
            'title': title,
            'version': version,
            'description': description
        }))
        self._spec['paths'] = defaultdict(dict)
        self._components = {}
        if components:
            with open(components) as f:
                self._components = yaml.load(f)
            self._spec.update(self._components)

        self.handlers: typing.DefaultDict[
            str, typing.Dict[str, typing.Callable[[web.Request], typing.Any]]] = defaultdict(dict)

        self._app.router.add_route('GET', ui_path, _redirect)
        self._app.router.add_route('GET', f'{ui_path}/', _swagger_home)
        self._app.router.add_route('GET', f'{ui_path}/swagger.json', _swagger_spec)

        self._app.router.add_static(f'{ui_path}/static', "swagger_ui")

        with open("swagger_ui/index.html") as f:
            self._app[_SWAGGER_INDEX_HTML] = f.read()

        self.register_media_type_handler('application/json', application_json)

    async def _handle_swagger_call(self, route, request):
        kwargs = await route.parse(request)
        return await route.handler(**kwargs)

    def add_route(self, method, path, handler, **kwargs):
        route = SwaggerRoute(method, path, handler, swagger=self, components=self._components, **kwargs)
        self._spec['paths'][path] = {method.lower(): route.spec}
        validate_v3_spec(self._spec)
        self._app[_SWAGGER_SPECIFICATION] = self._spec
        return self._app.router.add_route(method, path, functools.partial(self._handle_swagger_call, route))

    def add_head(self, path, handler, **kwargs):
        return self.add_route(hdrs.METH_HEAD, path, handler, **kwargs)

    def add_get(self, path, handler, **kwargs):
        return self.add_route(hdrs.METH_GET, path, handler, **kwargs)

    def add_post(self, path, handler, **kwargs):
        return self.add_route(hdrs.METH_POST, path, handler, **kwargs)

    def add_put(self, path, handler, **kwargs):
        return self.add_route(hdrs.METH_PUT, path, handler, **kwargs)

    def add_patch(self, path, handler, **kwargs):
        return self.add_route(hdrs.METH_PATCH, path, handler, **kwargs)

    def add_delete(self, path, handler, **kwargs):
        return self.add_route(hdrs.METH_DELETE, path, handler, **kwargs)

    def add_routes(self, routes):
        for route_obj in routes:
            route_obj.register(self)

    def register_media_type_handler(self, media_type: str, handler: typing.Callable[[web.Request], typing.Any]) -> None:
        typ, subtype = media_type.split('/')
        self.handlers[typ][subtype] = handler

    def get_media_type_handler(self, media_type: str) -> typing.Callable[[web.Request], typing.Any]:
        typ, subtype = media_type.split('/')
        if typ not in self.handlers:
            if '*' not in self.handlers:
                raise Exception(f"register handler for {media_type} first")
            elif '*' not in self.handlers['*']:
                raise Exception("missing handler for media type */*")
            else:
                return self.handlers['*']['*']
        if subtype not in self.handlers[typ]:
            if '*' not in self.handlers[typ]:
                raise Exception(f"register handler for {media_type} first")
            return self.handlers[typ]['*']
        return self.handlers[typ][subtype]


class SwaggerRoute:
    def __init__(self, method, path, handler, *, components: typing.Dict, swagger: Swagger, **kwargs):
        self.method = method
        self.path = path
        self.handler = handler
        self.kwargs = kwargs
        self.spec = yaml.load(self.handler.__doc__.split("---")[1])
        self.qp: typing.List[Parameter] = []
        self.pp: typing.List[Parameter] = []
        self.hp: typing.List[Parameter] = []
        self.bp: typing.Dict[str, Parameter] = {}
        self._swagger = swagger
        if 'parameters' in self.spec and self.spec['parameters'] is not None:
            for param in self.spec['parameters']:
                if '$ref' in param:
                    if not components:
                        raise Exception("file with components definitions is missing")
                    # '#/components/parameters/Month'
                    _, component, section, obj = param['$ref'].split('/')
                    param = components[component][section][obj]
                parameter = Parameter(
                    param['name'],
                    schema_to_validator(param['schema'], components),
                    param.get('required', False)
                )
                if param['in'] == 'query':
                    self.qp.append(parameter)
                elif param['in'] == 'path':
                    self.pp.append(parameter)
                elif param['in'] == 'header':
                    self.hp.append(parameter)

        if 'requestBody' in self.spec and self.spec['requestBody'] is not None:
            body = self.spec['requestBody']
            for media_type, value in body['content'].items():
                # check that we have handler for media_type
                self._swagger.get_media_type_handler(media_type)
                value = body['content'][media_type]
                self.bp[media_type] = Parameter(
                    'body',
                    schema_to_validator(value['schema'], components),
                    body.get('required', False)
                )
        self.params = handler.__code__.co_varnames

    async def parse(self, request: web.Request):
        params = {'request': request}
        request['data'] = {}
        # query parameters
        errors = {}
        if self.qp:
            for param in self.qp:
                if param.required:
                    v = request.rel_url.query[param.name]
                else:
                    v = request.rel_url.query.get(param.name, MISSING)
                try:
                    value = param.validator.validate(v, True)
                except ValidatorError as e:
                    errors[param.name] = e.error
                    continue
                if value != MISSING:
                    request['data'][param.name] = value
                    if param.name in self.params:
                        params[param.name] = value
        # body parameters
        if self.bp:
            media_type = request.headers['Content-Type']
            if media_type not in self.bp:
                raise Exception("no content-type handler")
            handler = self._swagger.get_media_type_handler(media_type)
            v = await handler(request)
            param = self.bp[media_type]
            try:
                value = param.validator.validate(v, False)
            except ValidatorError as e:
                errors[param.name] = e.error
            else:
                request['data'][param.name] = value
                if param.name in self.params:
                    params[param.name] = value
        # header parameters
        if self.hp:
            for param in self.hp:
                if param.required:
                    v = request.headers.getone(param.name)
                else:
                    v = request.headers.get(param.name, MISSING)
                try:
                    value = param.validator.validate(v, True)
                except ValidatorError as e:
                    errors[param.name] = e.error
                    continue
                if value != MISSING:
                    request['data'][param.name] = value
                    if param.name in self.params:
                        params[param.name] = value
        # path parameters
        if self.pp:
            for param in self.pp:
                v = request.match_info[param.name]
                try:
                    value = param.validator.validate(v, True)
                except ValidatorError as e:
                    errors[param.name] = e.error
                    continue
                request['data'][param.name] = value
                if param.name in self.params:
                    params[param.name] = value
        if errors:
            raise web.HTTPBadRequest(reason=errors)
        return params
