from itertools import chain

import sqlalchemy as sa
from sqlalchemy.orm.attributes import InstrumentedAttribute, QueryableAttribute
from sqlalchemy.sql.util import ClauseAdapter


def adapt(adapt_with, expression):
    if isinstance(expression.expression, sa.Column):
        cols = get_attrs(adapt_with)
        return getattr(cols, expression.name)
    if not hasattr(adapt_with, 'is_derived_from'):
        adapt_with = sa.inspect(adapt_with).selectable
    return ClauseAdapter(adapt_with).traverse(expression.expression)


def get_attrs(obj):
    if isinstance(obj, sa.orm.Mapper):
        return obj.class_
    elif isinstance(obj, (sa.orm.util.AliasedClass, sa.orm.util.AliasedInsp)):
        return obj
    elif isinstance(obj, sa.sql.selectable.Selectable):
        return obj.c
    return obj


def get_selectable(obj):
    if isinstance(obj, sa.sql.selectable.Selectable):
        return obj
    return sa.inspect(obj).selectable


def subpaths(path):
    return [
        '.'.join(path.split('.')[0:i + 1])
        for i in range(len(path.split('.')))
    ]


def s(value):
    return sa.text("'{0}'".format(value))


def get_descriptor_columns(model, descriptor):
    if isinstance(descriptor, InstrumentedAttribute):
        return descriptor.property.columns
    elif isinstance(descriptor, sa.orm.ColumnProperty):
        return descriptor.columns
    elif isinstance(descriptor, sa.Column):
        return [descriptor]
    elif isinstance(descriptor, sa.sql.expression.ClauseElement):
        return []
    elif isinstance(descriptor, sa.ext.hybrid.hybrid_property):
        expr = descriptor.expr(model)
        try:
            return get_descriptor_columns(model, expr)
        except TypeError:
            return []
    elif (
        isinstance(descriptor, QueryableAttribute) and
        hasattr(descriptor, 'original_property')
    ):
        return get_descriptor_columns(model, descriptor.property)
    raise TypeError(
        'Given descriptor is not of type InstrumentedAttribute, '
        'ColumnProperty or Column.'
    )


def chain_if(*args):
    if args:
        return chain(*args)
    return []


def _included_sort_key(value):
    return (value['type'], value['id'])


def assert_json_document(value, expected):
    assert value.keys() == expected.keys()
    for key in expected.keys():
        if key == 'included':
            assert sorted(
                expected[key],
                key=_included_sort_key
            ) == sorted(
                value[key],
                key=_included_sort_key
            )
        else:
            assert expected[key] == value[key]
