#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : error.py
Author : Zerui Qin
CreateDate : 2018-12-20 10:00:00
LastModifiedDate : 2018-12-20 10:00:00
Note : 自定义异常类
"""


class AgentServiceException(Exception):
    """
    AgentService异常
    """

    def __init__(self, s_service):
        Exception.__init__(self)
        err = 'Can not found {0}'.format(s_service)
        self.message = err
