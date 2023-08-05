from __future__ import print_function, unicode_literals, absolute_import

from ..util import throw_this, isinstance_usertype, double_sliver, datetime_sliver
from ..column import Column
from ..visual import ChartOptions
from builtins import str

def is_column_type(var):
    return isinstance_usertype(var,Column.__name__)

def get_most_restrictive_filters(filters):
    ret_filters = []
    in_filters = [f for f in filters if f['comparator'] == 'IN']
    # combine in filters
    filter_keys = [f['columnKey'] for f in in_filters if f['negate']]
    for filter_key in set(filter_keys):
        # assumes only one comparator IN
        values = []
        [values.append(f['value']) for f in in_filters if f['columnKey'] == filter_key]
        col_type = [f['columnType'] for f in in_filters if f['columnKey'] == filter_key][0]
        ret_filters.append({'columnKey':filter_key, 'columnType': col_type, 'comparator': 'IN', 'value': values, 'negate': True})

    filter_keys = [f['columnKey'] for f in in_filters if not f['negate']]
    for filter_key in set(filter_keys):
        # assumes only one comparator IN
        values = []
        [values.append(f['value']) for f in in_filters if f['columnKey'] == filter_key]
        col_type = [f['columnType'] for f in in_filters if f['columnKey'] == filter_key][0]
        ret_filters.append({'columnKey':filter_key, 'columnType': col_type, 'comparator': 'IN', 'value': values, 'negate': False})

    filter_keys = [f['columnKey'] for f in filters if f['comparator'] != 'IN']
    for filter_key in set(filter_keys):
        col_filters = [f for f in filters if f['columnKey'] == filter_key]
        gt = [f for f in col_filters if '>' in f['comparator']]
        if gt:
            hi = gt[0]
            for f in gt:
                if f['value'] > hi['value']:
                    hi = f
                    continue
                if f['value'] == hi['value'] and hi['comparator'] != '>':
                    hi = f
            ret_filters.append(hi)
        lt = [f for f in col_filters if '<' in f['comparator']]
        if lt:
            lo = lt[0]
            for f in lt:
                if f['value'] < lo['value']:
                    lo = f
                    continue
                if f['value'] == lo['value'] and lo['comparator'] != '<':
                    lo = f
            ret_filters.append(lo)
    return ret_filters

def add_sliver(_filter):
    if _filter['columnType'] == 'double':
      _filter['value'] = _filter['value'] + double_sliver
    elif  _filter['columnType'] == 'datetime':
      _filter['value'] = _filter['value'] + datetime_sliver
    else:
      _filter['value'] = _filter['value'] + 1
    return _filter

def subtract_sliver(_filter):
    if _filter['columnType'] == 'double':
      _filter['value'] = _filter['value'] - double_sliver
    elif  _filter['columnType'] == 'datetime':
      _filter['value'] = _filter['value'] - datetime_sliver
    else:
      _filter['value'] = _filter['value'] - 1
    return _filter

def fill_missing_filters(filters, column_data):
    filter_keys = [f['columnKey'] for f in filters if f['comparator'] == 'IN']
    ret_filters = [f for f in filters if f['columnKey'] in filter_keys]
    
    filter_keys = [f['columnKey'] for f in filters if f['comparator'] != 'IN']
    tmp_filters = [f for f in filters if f['columnKey'] in filter_keys]
    for col in [c for c in column_data if c['key'] in filter_keys]:
        col_filters = [f for f in filters if f['columnKey'] == col['key']]
        if not [f for f in col_filters if '>' in f['comparator']]:
            tmp_filters.append({'columnKey':col['key'], 'columnType': col['type'], 'comparator': '>=', 'value': col['range'][0], 'negate': False, 'or': False})
        if not [f for f in col_filters if '<' in f['comparator']]:
            tmp_filters.append({'columnKey':col['key'], 'columnType': col['type'], 'comparator': '<=', 'value': col['range'][1], 'negate': False, 'or': False})

    for f_key in set(filter_keys):
        this_key_filters = [f for f in tmp_filters if f['columnKey'] == f_key]
        if this_key_filters:
            [lower_bound_filter] = [f for f in this_key_filters if '>' in f['comparator']]
            [upper_bound_filter] = [f for f in this_key_filters if '<' in f['comparator']]

            # pull out one value for datetime
            [col_type_range] = [(col['type'],[col['range'][0][0],col['range'][1][0]]) if col['type'] == 'datetime' else (col['type'],col['range']) for col in column_data if col['key']==f_key]
            if col_type_range[0] == 'datetime':
                if isinstance(lower_bound_filter['value'],list):
                    val = lower_bound_filter['value'][0]
                    lower_bound_filter['value'] = val
                if isinstance(upper_bound_filter['value'],list):
                    val = upper_bound_filter['value'][0]
                    upper_bound_filter['value'] = val

            # bound
            if lower_bound_filter['value'] > col_type_range[1][1]:
                lower_bound_filter['value'] = col_type_range[1][1]
            if lower_bound_filter['value'] < col_type_range[1][0]:
                lower_bound_filter['value'] = col_type_range[1][0]
            if upper_bound_filter['value'] > col_type_range[1][1]:
                upper_bound_filter['value'] = col_type_range[1][1]
            if upper_bound_filter['value'] < col_type_range[1][0]:
                upper_bound_filter['value'] = col_type_range[1][0]

            if lower_bound_filter['comparator'] == '>':
                lower_bound_filter = add_sliver(lower_bound_filter)
            if lower_bound_filter['comparator'] == '<':
                lower_bound_filter = subtract_sliver(lower_bound_filter)
            if upper_bound_filter['comparator'] == '>':
                upper_bound_filter = add_sliver(upper_bound_filter)
            if upper_bound_filter['comparator'] == '<':
                upper_bound_filter = subtract_sliver(upper_bound_filter)


            negate = lower_bound_filter['negate']
            if not negate and lower_bound_filter['or'] and upper_bound_filter['or']:
                # if lower_bount_filter < upper_bound_filter and we're or then there's no filter to add
                if lower_bound_filter['value'] > upper_bound_filter['value']:
                    negate = True
                    (lower_bound_filter['value'],upper_bound_filter['value']) = (upper_bound_filter['value'],lower_bound_filter['value'])
                    ret_filters.append({'columnKey':lower_bound_filter['columnKey'], 'columnType': lower_bound_filter['columnType'], 'comparator': 'BETWEEN', 'value': [lower_bound_filter['value'], upper_bound_filter['value']], 'negate': negate})
            else:
                ret_filters.append({'columnKey':lower_bound_filter['columnKey'], 'columnType': lower_bound_filter['columnType'], 'comparator': 'BETWEEN', 'value': [lower_bound_filter['value'], upper_bound_filter['value']], 'negate': negate})

    return ret_filters        

def expand_filters(filters):
    expanded_filters = []
    for f in filters:
        if f.comparator_value:
            expanded_filters.extend([{'columnKey':f.key, 'columnType': f.type, 'comparator': cv['comparator'], 'value': cv['value'], 'negate': cv['negate'], 'or': cv['or']} for cv in f.comparator_value])
    return expanded_filters

def get_select_from_columns(columns):
    column_objs = []
    for col in [col for col in columns if col]:
        op = None
        if col.grouping:
            grouping_to_query_op = {'AUTO': 'BINS(DEFAULT_)'}
            op = grouping_to_query_op.get(col.grouping,col.grouping.upper())
        elif col.operator:
            op = col.operator
        column_objs.append({'columnKey':col.key, 'columnType': col.type, 'operator': op })
    return column_objs

def column_based_input_to_dict(_input):
    if isinstance(_input,tuple):
        _input = [_input]
    if isinstance(_input, list):
        _input = [(x[0].name,x[1]) if is_column_type(x[0]) else x for x in _input if x]
        _input = dict(_input)
    if isinstance(_input,dict):
        _input = dict([(key.name,_input[key]) if is_column_type(key) else (key,_input[key]) for key in _input if _input[key]])
    return _input

def add_aggregates_to_axes(aggregates, x, y, size, color, label):
    if aggregates:
        aggregates = column_based_input_to_dict(aggregates)

        axis_mapping = {'x': x, 'y': y, 'size': size, 'color': color, 'label': label}
        star_operators = ['NUMBER OF RECORDS', 'NUMBER']

        for axis_key in axis_mapping:
            axis = axis_mapping[axis_key]
            name = axis.name if axis else None
            if name and name in aggregates:
                if aggregates[name] and aggregates[name].upper() in star_operators:
                    axis_mapping[axis_key] = Column(key='*', type=None, name=None, operator='COUNT')
                elif axis:
                    axis.aggregate(aggregates[name])

        x = axis_mapping['x']
        y = axis_mapping['y']
        size = axis_mapping['size']
        color = axis_mapping['color']
        label = axis_mapping['label']
    return [x,y,size,color,label]

def add_groupings_to_axes(groupings, x, y, size, color, label):
    if groupings:
        groupings = column_based_input_to_dict(groupings)

        axis_mapping = {'x': x, 'y': y, 'size': size, 'color': color, 'label': label}
        for axis_key in axis_mapping:
            axis = axis_mapping[axis_key]
            name = axis.name if axis else None
            if name and name in groupings:
                axis.group_by(groupings[name])

        x = axis_mapping['x']
        y = axis_mapping['y']
        size = axis_mapping['size']
        color = axis_mapping['color']
        label = axis_mapping['label']
    return [x, y, size, color, label]

def column_name_to_column(all_columns, x):
    if is_column_type(x):
        return x
    col = [col for col in all_columns if col.name == str(x)]
    if not col:
        throw_this('cannot find column named %s.' % (str(x)))
    return col.pop(0)

def create_chart_axes(x, y, size, color, label):        
    chart_axes = {}
    for idx,(axis,s) in enumerate(zip(ChartOptions.AXES,[x,y,size,color,label])):
        result_col_type = None
        if s:
            result_col_type = 'int' if s.type == 'string' and s.operator == 'DISTINCT' else s.type
        chart_axes[axis] = {'key': s.key, 'type': result_col_type, 'idx': str(idx)} if s else None

    idx = 0

    dict_selects = {'x': x, 'y': y, 'size': size, 'color': color, 'label': label}
    for axis in ChartOptions.AXES:
        s = dict_selects[axis]
        if s:
            chart_axes[axis]['idx'] = idx
            idx = idx + 1
    return chart_axes

def get_final_filters(filters, raw_column_data):
    if filters is None:
        filters = []
    else:
        # add missing filters
        filters_list = filters if isinstance(filters, list) else [filters]
        filters = fill_missing_filters(get_most_restrictive_filters(expand_filters(filters_list)), raw_column_data)
    return filters