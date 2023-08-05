import copy
import hashlib
import json
import time
import uuid
from collections import OrderedDict, namedtuple
from pprint import pprint
from typing import List, Callable, Optional, TypeVar

import arrow
import attr
import pandas as pd
from pygments import highlight, lexers, formatters
from six import string_types


def _drop_from_dict(d: dict, skip: List[object]) -> dict:
    if d is None:
        d = None
    if isinstance(d, list):
        return [drop_from_dict(e, skip) for e in d]
    if isinstance(d, dict):
        return {
            k: drop_from_dict(v, skip) for k, v in d.items() if k not in skip
        }
    return d


def drop_from_dict(d: dict, skip: List[object]) -> dict:
    return _drop_from_dict(d, skip)


def modify_named_tuple(nt: namedtuple, modifications:dict) -> namedtuple:
    attr_dict = namedtuple_asdict(nt)
    attr_dict.update(modifications)
    return type(nt)(**attr_dict)


def modify_attr_class(attrClass: type, modifications:dict) -> namedtuple:
    return attr.evolve(attrClass, **modifications)


def utc_timestamp() -> str:
    return str(arrow.utcnow())


def unique_id() -> str:
    return str(uuid.uuid4())


def flatten_list_recursively(l: list):
    if not isinstance(l, list):
        return [l]
    returnVal = []
    for x in l:
        returnVal = returnVal + flatten_list_recursively(x)
    return returnVal


def flatmap(listToItterate: List, inputToAppendTo: List, function: Callable) -> List :
    if not listToItterate:
        return []
    head = listToItterate[0]
    tail = listToItterate[1:]
    return flatmap(tail, function(inputToAppendTo, head), function)


def hash_query(query):
    return hashlib.md5("".join(query.lower().split()).encode('utf-8')).hexdigest()


def invert_dict_lookup(d):
    return {v: k for k, v in d.items()}


def value_joiner(inner_df):
    return ",".join(map(lambda x: str(x), inner_df['equity_id'])) if hasattr(inner_df, 'columns') else ",".join(
        map(lambda x: str(x), inner_df))


def pluck(path, d, default={}):
    split_path = [x for x in path.split('.') if x]
    if len(split_path) > 0:
        return pluck('.'.join(split_path[1:]), d.get(split_path[0], default))
    return d


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        return ('%2.2f' % (te - ts), result)

    return timed


def remap_date_formats(date_dict, date_formats, original_format):
    return {
        k: arrow.get(v, original_format).format(date_formats.get(k, original_format))
        for (k, v) in date_dict.items()
    }


def join_inner_arrays(_dict, caster=lambda x: x):
    return {
        k: ",".join(map(caster, v)) if isinstance(v, list) else v
        for (k, v) in _dict.items()
    }


def de_whitespate_dict(_dict):
    return {
        k: v.replace(" ", "") if isinstance(v, str) else v
        for (k, v) in _dict.items()
    }


def pprint_with_header(header, obj):
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(header)
    pprint(obj)
    print("__________________________________________________")
    print("")


def print_json_with_header(header, obj):
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(header)
    print(json_makeup(obj))
    print("__________________________________________________")
    print("")


def print_attr_class_with_header(header, obj):
    if isinstance(obj, list):
        obj = list(map(attr.asdict, obj))
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(header)
    print(json_makeup(attr.asdict(obj)))
    print("__________________________________________________")
    print("")


def print_with_header(header, obj):
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(header)
    print(obj)
    print("__________________________________________________")
    print("")


def namedtuple_asdict(obj):
    """
    Turns a named tuple into a dict recursively
    From: https://stackoverflow.com/questions/16938456/serializing-a-nested-namedtuple-into-json-with-python-2-7
    """
    if hasattr(obj, "_asdict"): # detect namedtuple
        return OrderedDict(zip(obj._fields, (attr.asdict(item) for item in obj)))
    elif isinstance(obj, string_types): # iterables - strings
        return obj
    elif hasattr(obj, "keys"): # iterables - mapping
        return OrderedDict(zip(obj.keys(), (attr.asdict(item) for item in obj.values())))
    elif hasattr(obj, "__iter__"): # iterables - sequence
        return type(obj)((attr.asdict(item) for item in obj))
    else: # non-iterable cannot contain namedtuples
        return obj


def json_makeup(json_object):
    formatted_json = json.dumps(json_object, sort_keys=True, indent=4)
    colorful_json = highlight(
        formatted_json.encode('UTF-8'),
        lexers.JsonLexer(), formatters.TerminalFormatter()
    )
    return colorful_json


def filter_empty_records(l:List) -> List:
    return [x for x in l if x]


def is_not_none_or_nan(v:object) -> bool:
    return (True if v else False) if not isinstance(v,float) else (not pd.isna(v) if v else False)


def all_values_in_list_are_not_nones_or_nans(l:List) -> bool:
    return all_values_in_list_pass(l, is_not_none_or_nan)


def all_values_in_list_pass(l:List, validity_filter:callable) -> bool:
    return all(map(validity_filter, l))


def tuples_with_nans_to_tuples_with_nones(iter:List) -> List:
    # - [x] TODO: Dont like the instance check here ... python has no way of saying "isPrimitive"
        # ... I only want to check for NaNs on primitives... and replace them with None ... not Lists ...
        # Realization: NaNs are floats ...!
    return (
        tuple(map(lambda x: None if isinstance(x, float) and pd.isna(x) else x, list(tup)))
        for tup in iter
    )


def append_to_list(l:List, thing_to_append:Optional[object]) -> List:
    return l + [thing_to_append] if thing_to_append else l


def merge_dicts(a:dict, b:dict) -> dict:
    c = copy.deepcopy(a)
    c.update(b)
    return c


def derive_hour_from_date(iso_timestamp:str):
    d = arrow.get(iso_timestamp)
    return {
        "hour_number": int(d.format("H")),
        "hour": d.format("hhA"),
        "timezone": d.format("ZZ")
    }


def derive_day_from_date(iso_timestamp):
    return str(arrow.get(iso_timestamp).date())


def first_arg_is_type_wrapper(_callable, tuple_of_types):
    return lambda x: x if not isinstance(x, tuple_of_types) else _callable(x)


def field_names_of_attr_class(attr_class:type) -> List[str]:
    return list(map(lambda x: x.name, attr.fields(attr_class)))


# def list_of_dicts_to_list_of_classes(l:List[dict], cls:T) -> List[T]:
#     return list(map(lambda d: cls(**d), l))
# T = TypeVar("T")
# TypeVars and isinstnace does weird stuf ... https://github.com/python/typing/issues/62


def converter_for_list_of_classes(l:List[object], cls) -> List:
    if not l:
        return []

    invalid_types_in_list = list(map(
        lambda x: type(x),
        filter(
            lambda x: not isinstance(x, (cls, dict)),
            l
        )
    ))

    if invalid_types_in_list:
        raise Exception("Invalid type(s) {} in list".format(invalid_types_in_list))

    return list(map(
        lambda y: y if isinstance(y, cls) else cls(**y),
        l
    ))


def converter_for_classes(data:object, cls:type, dict_constructor:Optional[callable]=None) -> List[type]:
    if not data:
        return None
    if not isinstance(data, (cls, dict)):
        raise Exception("Invalid type {} of data.".format(type(data)))
    return data if isinstance(data, cls) else (
        cls(**data) if not dict_constructor else dict_constructor(data)
    )


