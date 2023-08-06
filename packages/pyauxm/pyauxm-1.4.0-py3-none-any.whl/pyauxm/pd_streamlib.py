#!/usr/bin/env python
# coding: utf8
"""
Chainable pandas row-processing.
"""

from __future__ import print_function, unicode_literals, absolute_import, division

import re
import functools
import six
import numpy as np
import pandas as pd


def _get_func_argnames(func):
    # TODO: support defaults (kwargs)
    assert callable(func)
    func_code = func.__code__
    result = func_code.co_varnames[:func_code.co_argcount]
    if hasattr(func, '__self__'):
        # classmethods and bound methods, but not staticmethods.
        # XX: not certain about this.
        result = result[1:]
    return result


def _nmap_common(df, func, source=None, axis='columns', result_type='broadcast', **apply_kwargs):
    if source is None:
        source = _get_func_argnames(func)
    pre_df = df[list(source)]
    return pre_df.apply(
        # TODO: experiment with the performance of this part.
        lambda row: func(**row.to_dict()),
        axis=axis,
        # NOTE: requires pandas >= 0.23.0
        result_type=result_type,
        **apply_kwargs)


def nmap_one(df, func, target_column, source=None, inplace=False, **apply_kwargs):
    """
    Map df rows using `func(row)` and make a new column from the return value.
    """
    results = _nmap_common(df, func, source=source, result_type='reduce')
    if not inplace:
        df = df.copy()
    df[target_column] = results
    return df


def nmap(df, func, target=None, source=None, inplace=False, **apply_kwargs):
    """
    Map df rows using `func(row)` and make multiple new columns from the iterable return value.

    ...

    :param target: names of the target columns.
    """
    results = _nmap_common(df, func, source=source, result_type='expand')

    if not target:
        if isinstance(results.columns, pd.RangeIndex):
            raise ValueError("Refusing to put in new columns from a RangeIndex; specify the `target` or return dicts")
        target = results.columns
    else:
        if len(results.columns) != len(target):
            raise ValueError("`target` length mismatch: result has %r, target has %r" % (
                len(results.columns), len(target)))

    if not inplace:
        df = df.copy()

    for src, dst in zip(results.columns, target):
        df[dst] = results[src]

    return df


_nfilter_extras = dict(
    # name -> func(series, value): bool_series
    {'in': lambda series, value: series.map(lambda cell: value in cell)},
    isnull=lambda series, value: pd.isnull(series) if value else ~pd.isnull(series),  # pylint: disable=invalid-unary-operand-type
    defined=lambda series, value: ~pd.isnull(series) if value else pd.isnull(series),  # pylint: disable=invalid-unary-operand-type
    nonzero=lambda series, value: series.map(bool) if value else ~series.map(bool),
    zero=lambda series, value: ~series.map(bool) if value else series.map(bool),
    re=lambda series, value, **kwargs: series.map(lambda cell: bool(re.search(value, cell, **kwargs))),
    startswith=lambda series, value: series.map(lambda cell: cell.startswith(value)),
    endswith=lambda series, value: series.map(lambda cell: cell.endswith(value)),
    gt=lambda series, value: series.map(lambda cell: cell > value),
    gte=lambda series, value: series.map(lambda cell: cell >= value),
    lt=lambda series, value: series.map(lambda cell: cell < value),
    lte=lambda series, value: series.map(lambda cell: cell <= value),
    # ...
)


def _nfilter_one_by_extras(df, name, value):
    parts = name.split("__", 1)
    if len(parts) < 2:
        raise ValueError("Incorrect usage of _nfilter_one_by_extras")
    name, extra = parts

    flt_func = _nfilter_extras.get(extra)
    if flt_func is None:
        raise ValueError("Unknown extra-filter", extra)

    return flt_func(df[name], value)


def nfilter_base_gen(df, *args, **kwargs):
    """
    DRY concise filters.

    Supported filters:

      * `lambda field1, field2: ...`
      * `name__defined=True`
      * `name__in=[...]`
      * `name__re="..."` (contains)
      * `name__{modifier}`
      * `name=lambda value: ...`  # uncertain, subject to change
      * `name=value`
    """
    for arg in args:
        flt = _nmap_common(df, func=arg, result_type='reduce')
        if flt.dtype.name != 'bool':
            flt = flt.map(bool)  # avoid some inconveniences
        yield flt

    for name, value in kwargs.items():
        flt = None
        if "__" in name:
            yield _nfilter_one_by_extras(df, name, value)
        elif callable(value):
            target = _nmap_common(df, func=value, source=[name], result_type='reduce')
            yield df[name] == target
        else:
            yield df[name] == value


def nfilter_base(df, *args, **kwargs):
    return list(nfilter_base_gen(df, *args, **kwargs))


def _nfilter_to_selection(df, *args, **kwargs):
    filters = nfilter_base(df, *args, **kwargs)
    if not filters:
        return df
    selected = functools.reduce(lambda left, right: left & right, filters)
    return selected


def nfilter(df, *args, **kwargs):
    """
    Shorthand for 'where X and Y and ...'.
    """
    selected = _nfilter_to_selection(df, *args, **kwargs)
    return df[selected]


# TODO?: nfilter_any (for `or` over the arguments)
# Probably less useful than writing an explicit `nfilter(lambda col1, col2: col1 or col2)`

def nexclude(df, *args, **kwargs):
    """
    Shorthand for 'where not (X and Y and ...)'
    """
    selected = _nfilter_to_selection(df, *args, **kwargs)
    return df[~ selected]


def nproject_one(df, value, **kwargs):
    if callable(value):
        return _nmap_common(df, func=value, result_type='reduce')

    if isinstance(value, six.string_types):
        return df[value]  # simple rename

    raise Exception("Unexpected nproject_one value", value)


def nproject(df, *args, **kwargs):
    """
    :param args: Either of:
      * ``: only set new columns as a result of processing.
      * `'-'`: do not return the original columns.
      * `'-col1', '-col2'`: exclude the specified columns from the source.
      * `'col1', 'col2'`: leave only the specified columns from the source.

    :param kwargs:
      * column_name -> column_expression
        * column_name: name of the target (output) column.
        * column expression: describes how the value will be obtained. Either of:
          * string: will make a copy of another column (useful for renaming).
          * `lambda col1, col2, ...: result_value` - will make a new column from the call result.
    """

    # # TODO?: _inplace
    # :param _inplace: (default: False) whether the passed dataframe should be mutated.
    # inplace = kwargs.pop('_inplace', False)

    if not args:
        # leave the columns as-is
        res_columns = list(df.columns)
    elif any(isinstance(val, six.string_types) and val.startswith("-") for val in args):
        # Exclude some columns
        assert all(val.startswith("-") for val in args), "should either be all inclusive or all exclusive"
        if len(args) == 1 and args[0] == '-':
            res_columns = []
        else:
            exclude_fields = set(val[1:] for val in args)
            # unknown_excluded = exclude_fields - set(df.columns)
            res_columns = list(col for col in df.columns if col not in exclude_fields)
    else:
        res_columns = list(args)

    result = df[res_columns]  # supposed to make a shallow copy too

    # TODO?: support automatic ordering of the projections for new-column dependencies.
    # e.g. `a=lambda col1: ..., b=lambda a: ...`

    for key, value in kwargs.items():
        res_value = nproject_one(df, value, key=key)
        if res_value is not None:
            result[key] = res_value

    return result


def nsort(df, *args, **sort_values_kwargs):
    """
    `df.sort_values` that allows temporary fields, in form of callables (same
    as `nproject`).

    :param args: fields / callables, ordered, to be used for sorting.

    :param sort_values_kwargs: additional arguments to `pandas.DataFrame.sort_values`

    Example:

        df.nsort(
            'a',
            lambda b: 1 if b.startswith('x') else 2,
            'b',
            ascending=[True, False, False],
            na_position='first')
    """
    order_columns = ['x{:02d}'.format(idx) for idx in range(len(args))]
    projection = dict(zip(order_columns, args))
    order_df = nproject(df, '-', **projection)
    order_df.sort_values(order_columns, **sort_values_kwargs)
    return df.loc(order_df.index)


def patch_all():
    pd.DataFrame.nmap_one = nmap_one
    pd.DataFrame.nmap = nmap
    pd.DataFrame.nfilter = nfilter
    pd.DataFrame.nexclude = nexclude
    pd.DataFrame.nproject = nproject
    pd.DataFrame.nsort = nsort


def _examples():
    """ ... """

    # WARNING:
    patch_all()

    df = pd.DataFrame(dict(
        col1=['A', 'A', 'B', np.nan, 'D', 'C'],
        col2=[2, 1, 9, 8, 7, 4],
        col3=[0, 1, 9, 4, 2, 3],
    ))
    # make a copy of the column
    dfp = df.nproject(col3cp='col3')
    assert list(dfp.columns) == list(df.columns) + ['col3cp'], dfp.columns
    # process a couple columns into a new one
    dfp = df.nproject(col23=lambda col2, col3: col2 + col3 * 2)
    assert list(dfp.columns) == list(df.columns) + ['col23'], dfp.columns
    # Reminder: the simple stuff can be done in this more performant way; the
    # `nproject` method is for more tricky per-row computations.
    assert (dfp['col23'] == (dfp['col2'] + dfp['col3'] * 2)).all(), dfp['col23']

    # process a couple columns into a couple new columns
    dfp = df.nmap(lambda col2, col3: (col2 * col3, col3 / col2), target=('colm', 'cold'))
    assert list(dfp.columns) == list(df.columns) + ['colm', 'cold'], dfp.columns

    # Same but returning a dict
    dfp = df.nmap(lambda col2, col3: dict(colm=col2 * col3, cold=col3 / col2))
    assert (
        (list(dfp.columns) == list(df.columns) + ['colm', 'cold']) or
        (list(dfp.columns) == list(df.columns) + ['cold', 'colm'])), dfp.columns

    dfp = df.nfilter(col2__gte=3)
    assert list(dfp['col3']) == [9, 4, 2, 3], dfp['col3']


if __name__ == '__main__':
    _examples()
