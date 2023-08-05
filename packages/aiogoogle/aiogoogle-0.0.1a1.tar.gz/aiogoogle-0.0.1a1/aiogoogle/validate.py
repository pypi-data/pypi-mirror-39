'''
A simple instance validation module for Discovery schemas.
Unfrtunately, Google uses a slightly modified version of JSONschema draft3 (mix of jsonschema and protobuff).
As a result, using an external library to validate Discovery schemas will raise lots of errors.
I tried to modify the popular: https://github.com/Julian/jsonschema to make it work with Google's version,
but it was just too complicated for the relatively simple task on our hands.
If you face any problems with aiogoogle's validation, you can always turn it off by either passing: ``method.__call__(validate=False)``
or turning it off for the whole API by passing aiogoogle.discover(validate=False)

This module misses a lot of the features provided with more advanced jsonschema validators e.g.

1. collecting all validation errors and raising them all at once
2. way more descriptive errors with a nice traceback
'''


__all__ = [
    'validate',
]

import datetime
import warnings
import re
import rfc3339

from .excs import ValidationError


#------ Helpers -------#

def remove_microseconds(value):
    # 2014-02-11T14:13:26
    if not isinstance(value, str):
        raise ValidationError("datetime should be a string")
    if '.' in value:
        print(value)
        print(value[:-5])
        return value[:-5] + 'Z'
    else:
        return value

def make_validation_error(checked_value, correct_criteria):
    return f"{checked_value} isn't valid. Expected a value that meets those criteria: {correct_criteria}"

#------- MAPPINGS -------#

JSON_PYTHON_TYPE_MAPPING = {
    'number': (float, int),
    'integer': (int),
    'string': (str),
    'object': (dict),
    'array': (list, set, tuple),
    'boolean': (bool),
    'null': (),  # Not used
    'any': (float, int, str, dict, list, set, tuple, bool)
}

KNOWN_FORMATS = ['int32', 'uint32', 'double', 'float', 'null', 'byte', 'date', 'date-time', 'int64', 'uint64', 'google-fieldmask', 'google-duration', 'google-datetime']

IGNORABLE_FORMATS = ['google-fieldmask', 'google-duration', 'google-datetime']

TYPE_FORMAT_MAPPING = {
    # Given this type, if None then don't check for additional "format" property in the schema, else, format might be any of the mapped values
    # Those are kept here for reference. They aren't used by any of the validators below. Instead validators check directly if there's any format requirements
    'any': [],
    'array': [],
    'boolean': [],
    'integer': ['int32', 'unint32'],
    'number': ['double', 'float'],
    'object': [],
    'string': ['null', 'byte', 'date', 'date-time','int64','uint64']
}

#-------- VALIDATORS ---------#

# Type validators (JSON schema)

def any_validator(value):
    req_types = JSON_PYTHON_TYPE_MAPPING['any']
    if not isinstance(value, req_types):
        raise ValidationError(make_validation_error(value, str(req_types)))

def array_validator(value):
    req_types = JSON_PYTHON_TYPE_MAPPING['array']
    if not isinstance(value, req_types):
        raise ValidationError(make_validation_error(value, str(req_types)))

def boolean_validator(value):
    req_types = JSON_PYTHON_TYPE_MAPPING['boolean']
    if not isinstance(value, req_types):
        raise ValidationError(make_validation_error(value, str(req_types)))

def integer_validator(value):
    req_types = JSON_PYTHON_TYPE_MAPPING['integer']
    if not isinstance(value, req_types):
        raise ValidationError(make_validation_error(value, str(req_types)))

def number_valdator(value):
    req_types = JSON_PYTHON_TYPE_MAPPING['number']
    if not isinstance(value, req_types):
        raise ValidationError(make_validation_error(value, str(req_types)))

def object_validator(value):
    req_types = JSON_PYTHON_TYPE_MAPPING['object']
    if not isinstance(value, req_types):
        raise ValidationError(make_validation_error(value, str(req_types)))

def string_validator(value):
    req_types = JSON_PYTHON_TYPE_MAPPING['string']
    if not isinstance(value, req_types):
        raise ValidationError(make_validation_error(value, str(req_types)))

# Format validators (Discovery Specific)  https://developers.google.com/discovery/v1/type-format

def int32_validator(value):
    if (value > 2147483648) or (value < -2147483648) :
        raise ValidationError(make_validation_error(value, 'Integer between -2147483648 and 2147483648'))

def uint32_validator(value):
    if (value < 0) or (value > 4294967295):
        raise ValidationError(make_validation_error(value, 'Integer between 0 and 4294967295'))

def int64_validator(value):
    if (value > 9223372036854775807) or (value < -9223372036854775807):
        raise ValidationError(make_validation_error(value, 'Integer between -9,223,372,036,854,775,807 and -9,223,372,036,854,775,807'))

def uint64_validator(value):
    if (value > 9223372036854775807*2) or (value < 0):
        raise ValidationError(make_validation_error(value, 'Integer between 0 and 9,223,372,036,854,775,807 * 2'))

def double_validator(value):
    if not isinstance(value, float):
        raise ValidationError(make_validation_error(value, 'Double type'))

def float_validator(value):
    if not isinstance(value, float):
        raise ValidationError(make_validation_error(value, 'Float type'))

def byte_validator(value):
    if not isinstance(value, bytes):
        raise ValidationError(make_validation_error(value, 'Bytes type'))

def date_validator(value):
    msg = make_validation_error(value, 'JSON date value. Hint: use datetime.date.isoformat(), instead of datetime.date')
    try:
        pvalue = rfc3339.parse_date(value)
        #pvalue = datetime.date.fromisoformat(value)
    except Exception as e:
        raise ValidationError(str(e) + msg)
    if not isinstance(pvalue, datetime.date):
        raise ValidationError(msg)

def datetime_validator(value):
    msg = make_validation_error(value, 'JSON datetime value. Hint: use datetime.datetime.isoformat(), instead of datetime.datetime')
    try:
        pvalue = rfc3339.parse_datetime(value)
        #pvalue = datetime.datetime.fromisoformat(value)
    except Exception as e:
        raise ValidationError(str(e), msg)
    if not isinstance(pvalue, datetime.datetime):
        raise ValidationError(msg)

def null_validator(value):
    if value != 'null':
        raise ValidationError(make_validation_error(value, "'null' NOT None"))

# Other Validators

def minimum_validator(value, minimum):
    if value < int(minimum):
        raise ValidationError(make_validation_error(value, f'Not less than {minimum}'))

def maximum_validator(value, maximum):
    if value > int(maximum):
        raise ValidationError(make_validation_error(value, f'Not less than {maximum}'))

#-- Sub validators ---------------------------

def validate_type(instance, schema):
    type_validator_name = schema['type']
    # Check if type in list of possible types to avoid calling globals() maliciously
    if type_validator_name not in JSON_PYTHON_TYPE_MAPPING:
        warnings.warn(
            f"""\n\nUnknown type: {type_validator_name} found.\n\nSkipping type checks for {instance}
            against this schema:\n\n{schema}\n\nPlease create an 
            issue @ https://github.com/omarryhan/aiogoogle and report this warning msg.""")
        return
    type_validator = globals()[type_validator_name + '_validator']
    type_validator(instance)

def validate_format(instance, schema):
    if schema.get('format'):
        # Exception for format: mostly protobuf formats
        if schema['format'] in IGNORABLE_FORMATS:
            return
        # /Exception
        format_validator_name = schema['format']
        # Check if type in list of possible types to avoid calling globals() maliciously
        if format_validator_name not in KNOWN_FORMATS:
            warnings.warn(
            f"""\n\nUnknown format: {format_validator_name} found.\n\nSkipping format checks for {instance}
            against this schema:\n\n{schema}\n\nPlease create an 
            issue @ https://github.com/omarryhan/aiogoogle and report this warning msg.""")
            return
        if format_validator_name == 'date-time':
            format_validator_name = 'datetime'
        format_validator = globals()[format_validator_name + '_validator']
        format_validator(instance)

def validate_range(instance, schema):
    if schema.get('minimum'):
        minimum_validator(instance, schema['minimum'])
    elif schema.get('maximum'):
        maximum_validator(instance, schema['maximum'])

def validate_pattern(instance, schema):
    pattern = schema.get('pattern')
    if pattern is not None:
        match = re.match(pattern, instance)
        if match is None:
            raise ValidationError(instance, f'Match this pattern: {pattern}')

#-- Main Validator ---------------

def validate_all(instance, schema):
    validate_type(instance, schema)
    validate_format(instance, schema)
    validate_range(instance, schema)
    validate_pattern(instance, schema)

#-- API --------------------

def validate(instance, schema, schemas=None):
    '''
    Arguments:

        Instance: Instance to validate

        schema: schema to validate instance against

        schemas: Full schamas dict to resolve refs if any
    '''

    def resolve(schema):
        '''
        Resolves schema from schemas
        if no $ref was found, returns original schema
        '''
        if '$ref' in schema:
            if schemas is None:
                raise ValidationError(f"Attempted to resolve a {str(schema)}, but no schemas ref were found to resolve from")
            try:
                schema = schemas[schema['$ref']]
            except KeyError:
                raise ValidationError(f"Attempted to resolve {schema['$ref']}, but no results found.")
        return schema

    def validate_object():
        # Validate instance is an object
        object_validator(instance)

        # Objects sometimes do not have a properties item?? weird. 
        # e.g. https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest schemas['Event']['extendedProperties']
        # Not sure whether or not this should raise a validation error.
        if 'properties' not in schema:
            return

        # Raise warnings on passed dict keys that aren't mentioned in the schema
        for k, _ in instance.items():
            if k not in schema['properties']:
                warnings.warn(f"Item {k} was passed, but not mentioned in the following schema {schema.get('id')}.\n\n It will probably be discarded by the API you're using")
        # Validate
        for k,v in schema['properties'].items():
            # Check if there's a ref to resolve
            v = resolve(v)
            # Check if instance has the property, if not, check if it's required
            if k not in instance:
                if v.get('required') is True:
                    raise ValidationError(f"Instance {k} is required")
            else:
                validate(instance[k], v, schemas)

    def validate_array():
        array_validator(instance)
        schema_ = resolve(schema['items'])
        # Check if instance has the property, if not, check if it's required
        for item in instance:
            validate(item, schema_, schemas)

    # Check schema and schemas are dicts. 
    # These errors shouldn't normally be raised, unless there's some messed up schema(s) being passed
    if not isinstance(schema, dict):
        raise TypeError('Schema must be a dict')
    if schemas is not None:
        if not isinstance(schemas, dict):
            raise TypeError('Schemas must be a dict')
    # Preliminary resolvement. 
    schema = resolve(schema)
    # If object (Dict): iterate over each entry and recursively validate
    if schema['type'] == 'object':
        validate_object()
    # If array (list or tuple) iterate over each item and recursively validate
    elif schema['type'] == 'array':
        # Validate instance is an array
        validate_array()
    # Else we reached the lowest level of a schema, validate
    else:
        validate_all(instance, schema)
