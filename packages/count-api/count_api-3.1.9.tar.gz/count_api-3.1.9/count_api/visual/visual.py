#!/usr/bin/env python3

from __future__ import print_function, unicode_literals
import os
from ..util import base_embed_url, base_preview_url, base_return_url, try_catch, throw_this, print_this, get_str
from ..api_requests import APIRequests
from builtins import str

def get_unique_path(base_path, extension):
    i = 0
    path = '%s.%s' % (base_path,extension)
    while os.path.exists(path):
        i += 1
        path =  path = '%s_%s.%s' % (base_path,get_str(i),extension)
    return path


class IFrame(object):
    """
    Generic class to embed an iframe in an IPython notebook
    """

    iframe = """
        <iframe
            width="{width}"
            height="{height}"
            src="{src}{params}"
            frameborder="0"
            allowfullscreen
        ></iframe>
        """

    def __init__(self, src, width, height):
        self.src = src
        self.width = width
        self.height = height

    def _repr_html_(self):
        """return the embed iframe"""
        params = ""
        return self.iframe.format(src=self.src,
                                  width=self.width,
                                  height=self.height,
                                  params=params)

class Visual:
    """Visual class containing the following methods:
        - `embed()`:
          - Returns IFrame to current visual. For use with interactive environments, e.g Jupyter notebooks.
          - `Return` IFrame.
        - `download_csv()`:
          - Download csv of visual on [count.co](https://count.co).
          - Downloads to Downloads folder if path is defaulted.
          - path: str download path.
        - `download_preview()`:
          - Download png of visual on [count.co](https://count.co).
          - Downloads to Downloads folder if path is defaulted.
          - path: str download path.
          - height: int pixels.
          - width: int pixels.
        - `preview_url()`:
          - Returns url to preview view on [count.co](https://count.co).
          - `Return`: String.
        - `set_chart_options(dict: chart_option)`:
          - Set chart options.
          - `chart_options`: Dictionary of chart options to be applied. Accepted dict keys:values:
            - `type`: `line`,`bar`,`circle`,`area`, `auto`
            - `x_type`: `linear`, `log`
            - `y_type`: `linear`, `log`
            - `size_type`: `linear`, `log`
            - `color_type`: `linear`, `log`
          - `Return`: Self.
        - `url()`:
          - Returns url to visual view on [count.co](https://count.co).
          - `Return`: String.
        - `url_embed()`:
          - Returns url to visual view on [count.co](https://count.co) suitable for embedding
          - `Return`: String.
    """
    def __init__(self, key, table_key):
        self.key = key
        self.table_key = table_key
        self.chart_options = None

    def _get_slack_token(self, notebook_key):
        user_profile = APIRequests.instance().users_getprofile()
        workspaces = user_profile['workspaces']
        slack_token = None
        w_idx = 0
        if workspaces:
            while slack_token == None and w_idx < len(workspaces): 
                try:
                    slack_token = APIRequests.instance().auth_getstate(notebook_key, workspaces[w_idx])
                except:
                    pass
                w_idx = w_idx + 1
        return slack_token['state'] if slack_token else slack_token

    def set_chart_options(self, chart_options):
        """`set_chart_options(dict: chart_option)`:
            - Set chart options.
            - `chart_options`: Dictionary of chart options to be applied. Accepted dict keys:values:
              - `type`: `line`,`bar`,`circle`,`area`, `auto`
              - `x_type`: `linear`, `log`
              - `y_type`: `linear`, `log`
              - `size_type`: `linear`, `log`
              - `color_type`: `linear`, `log`
            - `Return`: Self.
        """
        self.chart_options = chart_options
        return self

    def url(self):
        """`url()`:
            - Returns url to visual view on [count.co](https://count.co).
            - `Return`: String.
        """
        return self._url(base_return_url)

    def url_embed(self):
        """`url_embed()`:
            - Returns url to visual view on [count.co](https://count.co) suitable for embedding
            - `Return`: String.
        """
        return self._url(base_embed_url)

    def embed(self):
        """`embed()`:
            - Returns IFrame to current visual. For use with interactive environments, e.g Jupyter notebooks.
            - `Return` IFrame.
        """
        return IFrame(self.url_embed(),width = 1000,height = 1000)

    def _url(self, base_url):
        query_params = self._query_params()
        return "%s/%s?%s" % (base_url,self.table_key,'&'.join(query_params))

    def _query_params(self):
        options_dict = self.chart_options.options_dict
        query_params = []
        query_params.append('v=%s' % (self.key))
        query_params.append('view=visual')
        query_params.extend(["%s=%s" % (key, options_dict[key]) for key in options_dict if options_dict[key]])
        return query_params

    def preview_url(self):
        """`preview_url()`:
            - Returns url to preview visual on [count.co](https://count.co).
            - `Return`: String.
        """
        preview_url = self._url(base_preview_url)
        slack_token = self._get_slack_token(self.key)

        return "%s&state=%s" % (preview_url,slack_token)

    @try_catch
    def download_preview(self, path=None, height=315, width=600):
        """`download_preview()`:
            - Download png of visual on [count.co](https://count.co).
            - Downloads to Downloads folder if path is defaulted.
            - path: str download path.
            - height: int pixels.
            - width: int pixels.
        """
        dtype='png'
        accepted_types = ['png']
        if dtype not in accepted_types:
            throw_this('download dtype is not one of %s' % (','.join(accepted_types)))
        if not path:
            home_dir = os.path.expanduser('~')
            base_path = os.path.join(home_dir,'Downloads','count_%s_%s' % (self.table_key,self.key))
            path = get_unique_path(base_path, dtype)

        return APIRequests.instance().notebooks_downloadpreview(self.table_key, self.key, self._query_params(), height, width, path, dtype)

    @try_catch
    def download_csv(self, path=None):
        """`download_csv()`:
            - Download csv of visual on [count.co](https://count.co).
            - Downloads to Downloads folder if path is defaulted.
            - path: str download path.
        """
        # get unique path
        if not path:
            home_dir = os.path.expanduser('~')
            base_path = os.path.join(home_dir,'Downloads','count_%s_%s' % (self.table_key,self.key))
            path = get_unique_path(base_path, 'csv')

        return APIRequests.instance().notebooks_download(self.key, path)

class ChartOptions:
    AVAILABLE_AXIS_TYPES = ['linear', 'log']
    AVAILABLE_CHART_TYPES = ['circle', 'line', 'bar', 'area', 'auto']
    AXIS_TYPE_KEYS = ['x_type', 'y_type', 'size_type', 'color_type', 'label_type']
    AXIS_TYPE_MAPPING = {'x': 'x_type', 'y': 'y_type', 'size': 'size_type', 'color': 'color_type', 'label': 'label_type'}
    AXES = ['x', 'y', 'size', 'color', 'label']

    def __init__(self, chart_options, chart_axes):
        self.options_dict = {}
        self.chart_axes = chart_axes
        self.set_chart_options(chart_options)

    def validate_chart_options(self, chart_options):
        validation_msg = []

        if not isinstance(chart_options, dict):
            validation_msg.append('Error: expected dict type for chart_options')

        chart_axes = self.chart_axes
        if chart_options and isinstance(chart_options, dict):

            chart_type = chart_options.get('type', '').lower()
            if chart_type and chart_type not in ChartOptions.AVAILABLE_CHART_TYPES:
                validation_msg.append('Error: Chart type {chart_type} is not recognized. List of available chart types is [{list}]'.format(list=','.join(ChartOptions.AVAILABLE_CHART_TYPES), chart_type=chart_type))
            
            for axis_type_key in ChartOptions.AXIS_TYPE_KEYS:
                axis_type = chart_options.get(axis_type_key, '').lower()
                if axis_type and axis_type not in ChartOptions.AVAILABLE_AXIS_TYPES:
                    validation_msg.append('Error: {axis_type_key} {axis_type} is not recognized. List of available axis types is [{list}]'.format(list=','.join(ChartOptions.AVAILABLE_AXIS_TYPES), axis_type_key=axis_type_key, axis_type=axis_type))
            
            for axis,axis_type_key in zip(ChartOptions.AXES,ChartOptions.AXIS_TYPE_KEYS):
                if chart_axes[axis]:
                    if chart_options.get(axis_type_key, '').lower() and (chart_axes[axis]['type'] == 'string' or chart_axes[axis]['type'] == 'datetime'):
                        print_this('Warning: ignorning {axis_type_key} set for {type_} column'.format(axis_type_key=axis_type_key,type_=chart_axes[axis]['type']))
        return validation_msg

    def set_chart_options(self, chart_options):
        validation_msg = self.validate_chart_options(chart_options)
        if validation_msg:
            throw_this('|'.join(validation_msg))

        self.options_dict['type'] = chart_options.get('type', '').lower()
        if self.options_dict['type'] == 'auto':
          self.options_dict['type'] = None

        for axis_type_key in ChartOptions.AXIS_TYPE_KEYS:
            self.options_dict[axis_type_key] = None

        for axis,axis_type_key in zip(sorted(self.chart_axes),sorted(ChartOptions.AXIS_TYPE_KEYS)):
            if self.chart_axes[axis]:
                if self.chart_axes[axis]['type'] == 'string':
                    self.options_dict[axis_type_key] = 'ordinal'
                elif self.chart_axes[axis]['type'] == 'datetime':
                    self.options_dict[axis_type_key] = 'time'
                else:
                    self.options_dict[axis_type_key] = chart_options.get(axis_type_key, 'linear')
        
        for axis in self.chart_axes:
            if self.chart_axes[axis]:
                self.options_dict[axis] = get_str(self.chart_axes[axis]['idx'])

        return self