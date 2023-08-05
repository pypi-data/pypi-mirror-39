#!/usr/bin/env python3

from __future__ import print_function, unicode_literals, absolute_import

import os
import json
import six
from .table_tile import TableTile
from .util import print_this, throw_this, base_url, base_return_url, isinstance_usertype, try_catch, get_str, get_formatted
from .visual import ChartOptions, Visual
from .column import Column, Filter
from .api_requests import APIRequests
from .visual_helper import visual_helper
from builtins import str

def is_column_type(var):
    return isinstance_usertype(var,Column.__name__)

class Table:
    """Table class containing the following methods:
        - `[index]`:
          - Get Column object from column index.
          - `index`: Integer index of column
          - `Return`: Column Object.
        - `[name]`:
          - Get Column object from column name. Returns first column found with header matching name.
          - `name`: String column name.
          - `Return`: Column Object.
        - `append(path = None, data = None)`:
          - Appends csv file from path or csv data from str (keyword arg only method) to existing table. New table must match column types of existing table.
          - `path`: String filepath to the .csv or .xls(x). Cannot be used in conjunction with `path`.
          - `data`: String csv data to upload. Cannot be used in conjunction with `path`.
          - `Return`: Self.
        - `column(index)`:
          - Get Column object from column index.
          - `index`: Integer index of column
          - `Return`: Column Object.
        - `column(name)`:
          - Get Column object from column name. Returns first column found with header matching name.
          - `name`: String column name.
          - `Return`: Column Object.
        - `columns(name = None)`:
          - Get list of Column objects with headers matching name parameter. If name is defaulted, returns all columns in table.
          - `Return`: List of Column Objects.
        - `delete()`:
          - Deletes table from [count.co](https://count.co) server. Future references to this Table will be undefined.
        - `head(n=10)`:
          - Prints first n rows of table
          - `n`: Integer number of rows requested. Max 100. Default 10.
        - `tail(n=10)`:
          - Prints last n rows of table
          - `n`: Integer number of rows requested. Max 100. Default 10.
        - `overwrite(path = None, name = None, data = None, column_types = None, column_names = None)`:
          - Uploads csv file from path or csv data from str (keyword arg only method), overwriting existing table. New table must match column types of existing table.
          - `path`: String filepath to the .csv or .xls(x). Cannot be used in conjunction with `path`.
          - `data`: String csv data to upload. Cannot be used in conjunction with `path`.
          - `name`: String name of table.
          - `column_types`: List of strings of column types. Acceptable types of column type are 'string', 'int', 'double', and 'datetime'.
          - `column_names`: List of strings of column names.
          - if `column_names`/`column_types` have length greater than the number of columns in the table, the extra enties are ignored.
          - `column_names`: and `column_types` must have same length if both are set.
          - `Return`: Self.
        - `size()`:
          - Size of table as a tuple of ints (column_extent, row_extent)
          - `Return`: Tuple (int, int)
        - `upload_visual(x = None, y = None, color = None, size = None, label = None, aggregates = None, filters = None, groupings = None, chart_options = None)`:
          - Uploads chart visual to [count.co](https://count.co).
          - `x`: Column object/string column name to be used for x-axis
          - `y`: Column object/string column name to be used for y-axis
          - `color`: Column object/string column name to be used for color-axis
          - `size`: Column object/string column name to be used for size-axis           
          - `label`: Column object/string column name to be used for label-axis
          - `aggregates`: Tuple/list of tuples/dictionary of aggregates to be applied to columns.
          - `filters`: Tuple/list of tuples/dictionary of filters to be applied to columns.
          - `groupings`: Tuple/list of tuples/dictionary of groupings to be applied to columns.
          - `chart_options`: Dictionary of chart options to be applied. Accepted dict keys:values:
            - `type`: `line`,`bar`,`circle`,`area`, `auto`
            - `x_type`: `linear`, `log`
            - `y_type`: `linear`, `log`
            - `size_type`: `linear`, `log`
            - `color_type`: `linear`, `log`
            - `label_type`: `linear`, `log`
          - `Return`: Visual object.
        - `url()`:
          - Get url to table view on count.co.
          - `Return`: String of URL.
    """
    def __init__(self, table_key, count_api):
        self.headers = count_api.headers
        self.key = table_key

    def _get_filter_objects_from_list(self,filters):
        if not filters:
            return None
        
        if isinstance(filters,dict):
            new_filters = []
            for key in filters:
                cvs = filters[key]
                if not isinstance(cvs,list):
                    cvs = [cvs]
                new_filters.extend([(key.name,) + tuple(cv) if is_column_type(key) else (key,) + tuple(cv) for cv in cvs])
            filters = new_filters

        if not isinstance(filters,list):
            filters = [filters]

        expanded_filters = []
        for filt in filters:
            if not (len(filt) == 3 or len(filt) == 6):
                throw_this('filter lists must be of length 3 or 6.')
            if len(filt) == 6:
                [col, comparator, val, op, comparator2, val2] = filt
                _or = op == 'OR'
                expanded_filters.append((col,comparator,val, _or))
                expanded_filters.append((col,comparator2,val2, _or))
            elif len(filt) == 3:
                [col, comparator, val] = filt
                if 'IN' in comparator and type(val) is list:
                    for v in val:
                        expanded_filters.append((col, comparator, v))
                else:
                    expanded_filters.append(filt)

        dict_filters = {}
        all_columns = self.columns()
        for filt in expanded_filters:
            _or = False
            if len(filt) == 3:
                [col, comparator, val] = filt
            if len(filt) == 4:
                [col, comparator, val, _or] = filt
            if not is_column_type(col):
                col = [c for c in all_columns if c.name == col].pop(0)
            if is_column_type(col):
                col = get_str(col.key)
            if not isinstance(comparator,str):
                comparator = get_str(comparator)
            if not isinstance(val, list):
                val = [val]
            
            # this breaks multiple columns named same
            for v in val:
                if not (isinstance(v, int) or isinstance(v, float) or isinstance(v, list) or isinstance(v,tuple) or isinstance_usertype(v,'datetime')):
                    v = get_str(v)
                if col in dict_filters:
                    dict_filters[col].append((comparator, v, _or))
                else:
                    dict_filters[col] = [(comparator, v, _or)]

        ret_filters = []
        for key in dict_filters:
            [col_obj] = [c for c in all_columns if key == c.key]
            ret_filters.append(col_obj.filter_list(dict_filters[key]))
        return ret_filters

    @try_catch
    def upload_visual(self, x = None, y = None,  color = None,  size = None, label = None, aggregates = None, groupings = None, filters = None, chart_options = None):
        """`upload_visual(x = None, y = None, color = None, size = None, label = None, aggregates = None, filters = None, groupings = None, chart_options = None)`:
            - Uploads chart visual to [count.co](https://count.co).
            - `x`: Column object/string column name to be used for x-axis
            - `y`: Column object/string column name to be used for y-axis
            - `color`: Column object/string column name to be used for color-axis
            - `size`: Column object/string column name to be used for size-axis           
            - `label`: Column object/string column name to be used for label-axis
            - `aggregates`: Tuple/list of tuples/dictionary of aggregates to be applied to columns.
            - `filters`: Tuple/list of tuples/dictionary of filters to be applied to columns.
            - `groupings`: Tuple/list of tuples/dictionary of groupings to be applied to columns.
            - `chart_options`: Dictionary of chart options to be applied. Accepted dict keys:values:
              - `type`: `line`,`bar`,`circle`,`area`, `auto`
              - `x_type`: `linear`, `log`
              - `y_type`: `linear`, `log`
              - `size_type`: `linear`, `log`
              - `color_type`: `linear`, `log`
              - `label_type`: `linear`, `log`
            - `Return`: Visual object.
        """

        # SELECTS
        all_columns = self.columns()
        x = visual_helper.column_name_to_column(all_columns, x) if x else None
        y = visual_helper.column_name_to_column(all_columns, y) if y else None
        size = visual_helper.column_name_to_column(all_columns, size) if size else None
        color = visual_helper.column_name_to_column(all_columns, color) if color else None
        label = visual_helper.column_name_to_column(all_columns, label) if label else None

        [x,y,size,color,label] = visual_helper.add_aggregates_to_axes(aggregates, x, y, size, color, label)
        [x,y,size,color,label] = visual_helper.add_groupings_to_axes(groupings, x, y, size, color, label)
        selects = visual_helper.get_select_from_columns([x,y,size,color,label])

        if not selects:
            throw_this('no axes defined')

        # FILTERS
        filters = self._get_filter_objects_from_list(filters)
        filters = visual_helper.get_final_filters(filters, self._get_raw_columns_data())
        
        # ORDERDINGS
        orderings = []

        # CHART OPTIONS
        if chart_options is None:
            chart_options = {}
        # generate prior to running query in case there are trivial validation errors
        chart_axes = visual_helper.create_chart_axes(x,y,size,color,label)
        chart_options_obj = ChartOptions(chart_options, chart_axes)

        # QUERY
        query = {'filters': filters, 'orderings':orderings, 'selects':selects, 'tableKey': self.key}
        try:
            notebook_key = APIRequests.instance().tables_addnotebook(self.key, query)
        except Exception as e:
            msg = e.args[0]
            if 'empty filter' in msg.lower():
                throw_this('Empty filter')
            else:
                throw_this(msg)

        return Visual(notebook_key, self.key).set_chart_options(chart_options_obj)

    def _get_raw_columns_data(self):
        return APIRequests.instance().tables_getcolumns(self.key)

    @try_catch
    def columns(self, name=None):
        """`columns(name = None)`:
            - Get list of Column objects with headers matching name parameter. If name is defaulted, returns all columns in table.
            - `Return`: List of Column Objects.
        """
        columns = self._get_raw_columns_data()
        return [Column(key=col['key'],type=col['type'],name=col['name']) for col in columns if not name or col['name'] == name]

    @try_catch
    def column(self, index_or_name):
        """`column(index)`:
            - Get Column object from column index.
            - `index`: Integer index of column
            - `Return`: Column Object.
            `column(name)`:
            - Get Column object from column name. Returns first column found with header matching name.
            - `name`: String column name.
            - `Return`: Column Object.
        """
        if isinstance(index_or_name, int):
            return self._column_with_index(index_or_name)
        return self._column_with_name(get_str(index_or_name))

    @try_catch
    def __getitem__(self, index_or_name):
        """`[index]`:
            - Get Column object from column index.
            - `index`: Integer index of column
            - `Return`: Column Object.
            `[name]`:
            - Get Column object from column name. Returns first column found with header matching name.
            - `name`: String column name.
            - `Return`: Column Object.
        """
        return self.column(index_or_name)

    def _column_with_name(self,name):
        columns = self.columns(name)
        if columns:
            return columns[0]
        return None

    def _column_with_index(self, index):
        columns = self.columns()
        if index < len(columns) and index > -1:
            return columns[index]
        return None

    @try_catch
    def size(self):
        """`size()`:
            - Size of table as a tuple of ints (column_extent, row_extent)
            - `Return`: Tuple (int, int)
        """
        ret = APIRequests.instance().tables_getmetadata(self.key)
        return (ret[0], ret[1])

    @try_catch
    def head(self, n=10):
        """`head(n=10)`:
            - Prints first n rows of table
            - `n`: Integer number of rows requested. Max 100. Default 10.
        """
        return self._head(n)

    @try_catch
    def tail(self, n=10):
        """`tail(n=10)`:
            - Prints last n rows of table
            - `n`: Integer number of rows requested. Max 100. Default 10.
        """
        end_at = self.size()[1]
        return self._head(n, end_at)

    def _head(self, n, end_at = None):
        limit = min(n,100)
        selects = [{'columnKey':'*', 'columnType': None, 'operator': None }]
        query = {'filters': [], 'orderings':[], 'selects':selects, 'tableKey': self.key}
        offset = (end_at - limit) if end_at else 0
        r = APIRequests.instance().tables_getdata(self.key, query, offset, limit)
        table_tile = TableTile(r)
        col_data = []
        col_names = []
        for col in table_tile.columns:
            col_data.append(col.slice_(0,limit))
            col_names.append(col.name)

        output = []
        row_output = [u"{0:>6}".format('index')]
        max_cols = 5
        for idx,col in enumerate(col_names):
            if(idx < max_cols):
                row_output.append(u"{0:>15}".format(get_str(col)[:12]))
        output.append(''.join(row_output))

        size = self.size()[1]
        for i in range(0,min(limit,size)):
            row_output = [u"{0:>6}".format(get_str(i + offset))]
            for idx,col in enumerate(col_data):
                if(idx < max_cols):
                    row_output.append(u"{0:>15}".format(get_str(col[i])[:12]))
            output.append(''.join(row_output))
        print(u'\n'.join(output)) 

    @try_catch
    def delete(self):
        """`delete()`:
            - Deletes table from [count.co](https://count.co) server. Future references to this Table will be undefined.
        """
        APIRequests.instance().tables_delete(self.key)
        return

    @try_catch
    def append(self, *args, **kwargs):
        """`append(path = None, data = None)`:
            - Appends csv file from path or csv data from str (keyword arg only method) to existing table. New table must match column types of existing table.
            - `path`: String filepath to the .csv or .xls(x). Cannot be used in conjunction with `path`.
            - `data`: String csv data to upload. Cannot be used in conjunction with `path`.
            - `Return`: Self.
        """
        if args:
            throw_this('append function expects keyword arguments only.')
        kwargs['append_key'] = self.key
        self._overwrite_concatenate(kwargs)

    @try_catch
    def overwrite(self, *args, **kwargs):
        """`overwrite(path = None, name = None, data = None, column_types = None, column_names = None)`:
            - Uploads csv file from path or csv data from str (keyword arg only method), overwriting existing table. New table must match column types of existing table.
            - `path`: String filepath to the .csv or .xls(x). Cannot be used in conjunction with `path`.
            - `data`: String csv data to upload. Cannot be used in conjunction with `path`.
            - `name`: String name of table.
            - `column_types`: List of strings of column types. Acceptable types of column type are 'string', 'int', 'double', and 'datetime'.
            - `column_names`: List of strings of column names.
            - if `column_names`/`column_types` have length greater than the number of columns in the table, the extra enties are ignored.
            - `column_names`: and `column_types` must have same length if both are set.
            - `Return`: Self.
        """
        kwargs['overwrite_key'] = self.key
        if args:
            throw_this('overwrite function expects keyword arguments only.')
        self._overwrite_concatenate(kwargs)

    def _overwrite_concatenate(self, kwargs):

        path = kwargs.pop('path') if 'path' in kwargs else None
        name = kwargs.pop('name') if 'name' in kwargs else None
        data = kwargs.pop('data') if 'data' in kwargs else None
        types = kwargs.pop('column_types') if 'column_types' in kwargs else None
        names = kwargs.pop('column_names') if 'column_names' in kwargs else None
        overwrite_key = kwargs.pop('overwrite_key') if 'overwrite_key' in kwargs else None
        append_key = kwargs.pop('append_key') if 'append_key' in kwargs else None

        # Check raw dataframe not uploaded
        if isinstance_usertype(data, 'DataFrame'):
            data = data.to_csv(encoding='utf-8', index=False)
        if kwargs:
            throw_this('unexpected **kwargs: %s' % (list(kwargs.keys())) )
        if path and data:
            throw_this('either path or data must be specified, but not both')
        if types and not isinstance(types,list):
            throw_this('column_types must be a list of strings')
        if names and not isinstance(names,list):
            throw_this('column_names must be a list of strings')
        if append_key and (names or types):
            throw_this('cannot set column_types or column_names on appending')
        if overwrite_key and append_key:
            throw_this('both overwrite_key and append_key cannot be specified')

        acceptable_types = ['STRING', 'INT', 'DOUBLE', 'DATETIME', 'UNKNOWN']
        if types:
            types = [t if t else 'UNKNOWN' for t in types] 
            wrong_types = [t for t in types if not isinstance(t,six.string_types)]
            if len(wrong_types) > 0:
                throw_this('%s are not acceptable column types.' % (','.join(wrong_types)))
            types = [t.upper() for t in types]
            for type_ in types:
                if type_ not in acceptable_types:
                    throw_this('%s is not an acceptable column type. Acceptable column types are %s' % (type_, acceptable_types))

        fn = None
        data_param = None
        if path:
            if os.path.isfile(path):
                fn = APIRequests.instance().tables_upload_file
                data_param = os.path.abspath(path)
            else: 
                throw_this('cannot find: ' + path)
        if data:
            if len(data) > 0:
                fn = APIRequests.instance().tables_upload_data
                data_param = data
            else :
                throw_this('data length 0')
        try:
            r = fn(data_param, name, overwrite_key=overwrite_key, append_key=append_key, column_types=types, column_names=names)
            self.key = r
            return self
        except Exception as e:
            msg = e.args[0]
            if 'has different number of columns to original table' in msg.lower():
                throw_this('number of columns should match original table when using append')
            if 'has too few columns' in msg.lower():
                throw_this('number of columns should be equal to or greater than original table when using overwrite')
            if 'has wrong type, should have same as' in msg.lower():
                throw_this('column type mismatch with original table: please check column types of new table match original')
            throw_this(msg)

    def url(self):
        """`url()`:
            - Get url to table view on count.co.
            - `Return`: String of URL.
        """
        return  "%s/%s" % (base_return_url,self.key)
