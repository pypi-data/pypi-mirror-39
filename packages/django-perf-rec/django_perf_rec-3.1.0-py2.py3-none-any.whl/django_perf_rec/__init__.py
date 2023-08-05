# -*- coding:utf-8 -*-
"""
isort:skip_file
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import six

try:
    import pytest
except ImportError:
    pytest = None

if pytest is not None:
    if six.PY2:
        pytest.register_assert_rewrite(b'django_perf_rec.api')
    else:
        pytest.register_assert_rewrite('django_perf_rec.api')

from .api import TestCaseMixin, get_record_name, get_perf_path, record  # noqa: F401

__version__ = '3.1.0'
