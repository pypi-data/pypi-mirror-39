#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: capture.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 03.08.2018
import json
import sys
import traceback


def exception_capture():
    """Capture and format the exception info

    Return:
        a str
    """
    exc_type, exc_info, exc_tb = sys.exc_info()
    exc_tb = traceback.format_tb(exc_tb)
    return json.dumps(
        {
            u'exc_type': str(exc_type),
            u'exc_info': exc_info.__repr__(),
            u'exc_tb': exc_tb
        }
    )
