import sys
from pkg_resources import Requirement
import unittest
import jsonschema
from genson import SchemaNode, SchemaBuilder

PYTHON_VERSION = sys.version[:sys.version.find(' ')]


class SchemaBuilderTestCase(unittest.TestCase):

    def setUp(self):
        self.builder = self.CLASS()
        self._objects = []
        self._schemas = []

    def set_schema_options(self, **options):
        self.builder = SchemaNode(**options)

    def add_object(self, obj):
        self.builder.add_object(obj)
        self._objects.append(obj)

    def add_schema(self, schema):
        self.builder.add_schema(schema)
        self._schemas.append(schema)

    def assertObjectValidates(self, obj):
        jsonschema.Draft4Validator(self.builder.to_schema()).validate(obj)

    def assertObjectDoesNotValidate(self, obj):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.Draft4Validator(self.builder.to_schema()).validate(obj)

    def assertResult(self, expected):
        self.assertEqual(self.builder.to_schema(), expected)
        self.assertUserContract()

    def assertUserContract(self):
        self._assertSchemaIsValid()
        self._assertComponentObjectsValidate()

    def _assertSchemaIsValid(self):
        jsonschema.Draft4Validator.check_schema(self.builder.to_schema())

    def _assertComponentObjectsValidate(self):
        compiled_schema = self.builder.to_schema()
        for obj in self._objects:
            jsonschema.Draft4Validator(compiled_schema).validate(obj)


class SchemaNodeTestCase(SchemaBuilderTestCase):
    CLASS = SchemaNode


class SchemaBuilderTestCase(SchemaBuilderTestCase):
    CLASS = SchemaBuilder


# backwards compatibility

def only_for_python_version(version_specifier):
    req = Requirement.parse('python%s' % version_specifier)
    def handler(func):
        if PYTHON_VERSION in req:
            return func
        else:
            return unittest.skip('Python version %s does not match: %s'
                                 % (PYTHON_VERSION, req))(func)
    return handler
