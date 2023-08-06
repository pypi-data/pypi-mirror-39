#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : agent_data_service.py
Author : Zerui Qin
CreateDate : 2018-12-20 10:00:00
LastModifiedDate : 2018-12-20 10:00:00
Note : Agent客户端类, 获取Agent相关服务
"""

from utils.error import AgentServiceException
from watero_go.agent_control_service import AgentControlService
from watero_go.agent_data_service import AgentDataService


class AgentClient:
    """
    Agent客户端
    """

    def __init__(self, s_host, s_port, s_api_version):
        """
        初始化
        :param s_host: Watero Center公网地址
        :param s_port: Watero Center服务端口号
        :param s_api_version: API版本: v1, v2, etc...
        """
        self.host = s_host
        self.port = s_port
        self.api_version = s_api_version

    def get_service(self, s_service):
        """
        获取Agent相关服务
        :param s_service: 服务名称
        :return:
        """
        if s_service == 'agent_data_service':
            return AgentDataService(self.host, self.port, self.api_version)
        elif s_service == 'agent_control_service':
            return AgentControlService(self.host, self.port)
        else:
            raise AgentServiceException(s_service)
