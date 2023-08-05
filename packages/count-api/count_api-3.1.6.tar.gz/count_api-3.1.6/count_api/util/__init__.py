from __future__ import print_function, unicode_literals

import os
from functools import wraps
from future.utils import raise_with_traceback

from builtins import str

def throw_this(msg):
  if debug:
    raise_with_traceback(Exception(msg))
  else:
    raise Exception(msg)

def print_this(msg):
  print('CountAPI: ' + msg)

def isinstance_usertype(inst, name):
    return name == inst.__class__.__name__

def try_catch(f):
  @wraps(f)
  def wrapper(self, *args, **kwarg):
      try:
          return f(self, *args, **kwarg)
      except Exception as e:
          msg = e.args[0]
          if debug:
              raise_with_traceback(Exception('CountAPI: Error: ' + msg))
          else:
              raise Exception('CountAPI: Error: ' + msg)
  return wrapper

base = os.environ.get('COUNT_API_URL', 'https://count.co')
print_this('Running with url: %s' % (base))
base_url = '%s/api/v1/' % (base)
base_return_url = '%s/explore' % (base)
base_embed_url = '%s/embed' % (base)
base_preview_url = '%s/api/v1/notebooks.getPreview' % (base)

double_sliver = 1.0e-10
datetime_sliver = 24*60*60*1000

debug = True if 'COUNT_API_DEBUG' in os.environ else False