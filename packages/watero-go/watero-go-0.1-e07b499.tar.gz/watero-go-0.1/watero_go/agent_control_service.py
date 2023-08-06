#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : agent_control_service.py
Author : Zerui Qin
CreateDate : 2018-12-20 10:00:00
LastModifiedDate : 2018-12-20 10:00:00
Note : Agent控制服务类, 获取Agent控制服务相关方法
"""
from utils import mac_addr


class AgentControlService:
    """
    Agent控制服务
    """

    def __init__(self, s_host, s_port):
        """
        初始化
        :param s_host: Watero Center公网地址
        :param s_port: Watero Center服务端口号
        """
        self.url = s_host + ':' + str(s_port)
        self.mac_addr = mac_addr.get_mac_address()
