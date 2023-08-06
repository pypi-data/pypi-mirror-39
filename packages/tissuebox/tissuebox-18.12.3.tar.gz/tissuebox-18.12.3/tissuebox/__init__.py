import re

"""
Structure of a schema

{
    'required': [
    ],
    'mappings': {
    },
}

Left side:
    'string' --> Keys for the nested lookup of payload
    (callable, 'string', 'string' ... ) --> First item is a callable and rest of the strings are nested lookup keys

Right side:
    Case 1 - callable --> A type_function which returns boolean by receiving the looked up value as input
    Case 2 - [callable] --> A type_function surrounded by square brackets, means the boolean type_function is verfied to be all() of the
    Case 3 - {item1, item2, item3} --> Set of values, the looked up value is checked against this set similar to enum
    Case 4 - (callable, arg1, arg2) --> A type_funtion, similar to case-1, but accepts additional parameters. First argument is the looked up value

"""

class SchemaError(BaseException):
    pass

def rfc_datetime(x):
    return bool(re.match(r'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})(\.([0-9]+))?(Z|([+-][0-9]{2}):([0-9]{2}))', x))

def numeric_string(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def geolocation(x):
    try:
        if len(x) != 2:
            return False
        return -90 <= x[0] <= 90 and -180 <= x[1] <= 180
    except TypeError:
        return False

def integer_string(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def integer(x):
    if isinstance(x, bool):
        return False
    return isinstance(x, int)

def between(x, a, b, inclusive=False):
    try:
        if inclusive:
            return a <= x <= b
        return a < x < b
    except TypeError:
        return False

def eq(a, b):
    return a == b

def lte(x, n):
    return x <= n

def lt(x, n):
    return x < n

def gte(x, n):
    return x >= n

def gt(x, n):
    return x > n

def divisible(x, n):
    return numeric(x) and numeric(n) and x % n == 0

def negative_integer(x):
    return integer(x) and x < 0

def positive_integer(x):
    return integer(x) and x > 0

def whole_number(x):
    return integer(x) and x >= 0

def decimal(x):
    return isinstance(x, float)

def numeric(x):
    return integer(x) or decimal(x)

def negative(x):
    return numeric(x) and x < 0

def positive(x):
    return numeric(x) and x > 0

def string(x):
    return isinstance(x, str)

def uuid4(x):
    # https://stackoverflow.com/a/18359032/968442
    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    return bool(regex.match(x))

def email(x):
    # https://emailregex.com/
    import re
    return bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", x))

def url(x):
    # https://stackoverflow.com/a/17773849/968442
    import re
    return bool(re.match(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})", x))

def dictionary(x):
    return isinstance(x, dict)

def array(x):
    return isinstance(x, list)

def typed_array(array, type_function):
    return all([type_function(item) for item in array])

def boolean(x):
    return isinstance(x, bool)

def null(x):
    return x is None

def nested_get(d, attrs):
    for at in attrs:
        d = d[at.strip()]
    return d

def nested_get_quite(d, *attrs):
    """
    Similar to nested_get, but swallows the KeyError exception, Instead returns an empty iterable
    :param d:
    :param attrs:
    :return:
    """
    try:
        for at in attrs:
            d = d[at]
        return d
    except KeyError:
        return ''

def validate(schema, payload):
    """
    Receives a schema and validates against the payload

    :param schema:
    :param payload:
    :return: Tuple of (bool, list)
    """

    details = []

    # Initial sanity checks
    for key in schema.keys():
        if key not in ['required', 'types']:
            raise SchemaError

    # Process `exist` option
    for item in nested_get_quite(schema, 'required'):
        if '||' in item:
            found = False
            sub_items = item.strip().split('||')
            for si in sub_items:
                try:
                    nested_get(payload, si.strip().split('.'))
                    found = True
                except KeyError:
                    continue
            if not found:
                details.append("`exist` condition is failing for `{}`".format(item))

            continue

        try:
            nested_get(payload, item.strip().split('.'))
        except KeyError:
            details.append("`exist` condition is failing for `{}`".format(item))

    # Process `types` part
    for key, value in nested_get_quite(schema, 'types').items():
        try:
            elem = nested_get(payload, key.strip().split('.'))
        except KeyError:
            continue  # Simply continue, we only validate data types for values that are found in the payload.

        if isinstance(value, list):
            if not len(value) == 1:
                raise SchemaError
            if not typed_array(elem, value[0]):
                details.append("`types` condition is failing for `{}`".format(key))
            continue

        if isinstance(value, tuple):
            if not value:
                raise SchemaError
            if not elem in value:
                details.append("Enum tuple is failing for `{}`. Double check the schema".format(key))
            continue

        if not value(elem):
            details.append("`types` condition is failing for `{}`".format(key))

    return not details, details
