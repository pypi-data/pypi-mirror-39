#!/usr/bin/env python3

from __future__ import print_function, unicode_literals
from builtins import str
import os
import json
import sys
import six
from .table import Table
from .util import throw_this, print_this, isinstance_usertype, try_catch
from .api_requests import APIRequests
from builtins import str

class CountAPI:
    """CountAPI class containing the following methods:
      - `set_api_token(api_token)`
        - Sets API token obtained from [count.co](https://count.co).
        - `api_token`: String API token 
      - `upload(path = None, name = None, data = None, overwrite_key = None)`
        - Uploads csv file from path or csv data from str (keyword arg only method).
        - `path`: String filepath to the .csv or .xls(x). Cannot be used in conjunction with `path`.
        - `data`: String csv data to upload. Cannot be used in conjunction with `path`.
        - `name`: String name of table.
        - `overwrite_key`: String key of the table for which you would like to replace the data.
        - `append_key`: String key of the table to which you would like to append data.
        - `column_types`: List of strings of column types. Acceptable types of column type are 'string', 'int', 'double', and 'datetime'.
        - `column_names`: List of strings of column names.
        - if `column_names`/`column_types` have length greater than the number of columns in the table, the extra enties are ignored.
        - `column_names`: and `column_types` must have same length if both are set.
        - `column_names` and `column_types` cannot be used in conjuction with `append_key`
        - `Return`: Table object.
      - `delete_table(table_key)`:
          - Deletes specified table from [count.co](https://count.co) server.
          - `table_key`: String table key.
      - `table(table_key)`:
          - Get a table object from an existing table key.
          - `table_key`: String table key.
          - `Return`: Table Object.

    """
    def __init__(self):
        self.headers = None

    @try_catch
    def set_api_token(self, api_token):
        """`set_api_token(api_token)`
            - Sets API token obtained from [count.co](https://count.co).
            - `api_token`: String API token 
        """
        APIRequests.instance().set_api_token(api_token)

    @try_catch
    def upload(self, *args, **kwargs):
        """`upload(path = None, name = None, data = None, overwrite_key = None)`
            - Uploads csv file from path or csv data from str (keyword arg only method).
            - `path`: String filepath to the .csv or .xls(x). Cannot be used in conjunction with `path`.
            - `data`: String csv data to upload. Cannot be used in conjunction with `path`.
            - `name`: String name of table.
            - `overwrite_key`: String key of the table for which you would like to replace the data.
            - `append_key`: String key of the table to which you would like to append data.
            - `column_types`: List of strings of column types. Acceptable types of column type are 'string', 'int', 'double', and 'datetime'.
            - `column_names`: List of strings of column names.
            - if `column_names`/`column_types` have length greater than the number of columns in the table, the extra enties are ignored.
            - `column_names`: and `column_types` must have same length if both are set.
            - `column_names` and `column_types` cannot be used in conjuction with `append_key`
            - `Return`: Table object.
        """

        path = kwargs.pop('path') if 'path' in kwargs else None
        name = kwargs.pop('name') if 'name' in kwargs else None
        overwrite_key = kwargs.pop('overwrite_key') if 'overwrite_key' in kwargs else None
        append_key = kwargs.pop('append_key') if 'append_key' in kwargs else None
        data = kwargs.pop('data') if 'data' in kwargs else None
        types = kwargs.pop('column_types') if 'column_types' in kwargs else None
        names = kwargs.pop('column_names') if 'column_names' in kwargs else None

        # Check raw dataframe not uploaded
        if isinstance_usertype(data, 'DataFrame'):
            data = data.to_csv(encoding='utf-8', index=False)

        if kwargs:
            throw_this('unexpected **kwargs: %s' % (list(kwargs.keys())) )
        if args:
            throw_this('upload function expects keyword arguments only.')
        if path and data:
            throw_this('either path or data must be specified, but not both')
        if overwrite_key and append_key:
            throw_this('both overwrite_key and append_key cannot be specified')
        if types and not isinstance(types,list):
            throw_this('column_types must be a list of strings')
        if names and not isinstance(names,list):
            throw_this('column_names must be a list of strings')
        if append_key and (names or types):
            throw_this('cannot set column_types or column_names on appending')

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

        # Check table exists
        if overwrite_key:
            overwrite_key = str(overwrite_key)
            if len(overwrite_key) != 11:
                throw_this('expected 11 character alphanumeric strings for key.')
            try:
                APIRequests.instance().tables_getmetadata(overwrite_key)
            except:
                throw_this('table corresponding to overwrite_key %s not found' % (overwrite_key))

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
            return Table(r, self)
        except Exception as e:
            msg = str(e.args[0])
            if 'has different number of columns to original table' in msg.lower():
                throw_this('number of columns should match original table when using append')
            if 'has too few columns' in msg.lower():
                throw_this('number of columns should be equal to or greater than original table when using overwrite')
            if 'has wrong type, should have same as' in msg.lower():
                throw_this('column type mismatch with original table: please check column types of new table match original')
            throw_this(msg)

    @try_catch
    def delete_table(self, table_key):
        """`delete_table(table_key)`:
            - Deletes specified table from [count.co](https://count.co) server.
            - `table_key`: String table key.
        """
        APIRequests.instance().tables_delete(table_key)
        return

    @try_catch
    def table(self, table_key):
        """`table(table_key)`:
            - Get a table object from an existing table key.
            - `table_key`: String table key.
            - `Return`: Table Object.
        """
        return Table(table_key, self)

    def _get_notebook_metadata(self, notebook_key):
        return APIRequests.instance().tables_getnotebook_metadata(notebook_key)