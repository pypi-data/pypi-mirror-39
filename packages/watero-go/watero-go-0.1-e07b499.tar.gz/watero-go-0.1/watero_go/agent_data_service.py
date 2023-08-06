#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : agent_data_service.py
Author : Zerui Qin
CreateDate : 2018-12-20 10:00:00
LastModifiedDate : 2018-12-20 10:00:00
Note : Agent数据服务类, 获取Agent数据服务相关方法
"""
import time

import psutil
import requests

from utils import mac_addr
from utils.log import log_debug


class AgentDataService:
    """
    Agent数据服务
    """

    def __init__(self, s_host, s_port, s_api_version):
        """
        初始化
        :param s_host: Watero Center公网地址
        :param s_port: Watero Center服务端口号
        :param s_api_version: API版本: v1, v2, etc...
        """
        self.url = s_host + ':' + str(s_port) + '/api/' + s_api_version + '/heartbeat'
        self.mac_addr = mac_addr.get_mac_address()

    def register_agent(self):
        """
        发送Agent注册信息
        :return: str - access_token
        """
        payload = dict()
        payload['mac_addr'] = self.mac_addr
        response = requests.post(url=self.url, data=payload)
        res_json = response.json()
        if response.status_code == 200:  # 服务器状态码为200
            access_token = res_json['message']['access_token']
            if res_json['status'] == 1:
                log_debug.logger.info('Add access_token successfully')
            elif res_json['status'] == 2:
                log_debug.logger.info('Update access_token successfully')
            return access_token
        elif response.status_code == 403:
            log_debug.logger.error(res_json['message']['info'])
            return None
        else:
            log_debug.logger.error('Unknown error')
            return None

    def send_heartbeat(self, s_access_token):
        """
        发送Agent心跳信息
        :param s_access_token: Agent注册之后返回的access_token
        :return:
        """
        payload = dict()
        payload['mac_addr'] = self.mac_addr
        payload['access_token'] = s_access_token
        payload['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        response = requests.post(url=self.url, data=payload)
        res_json = response.json()
        if response.status_code == 200:  # 服务器状态码为200
            log_debug.logger.info(res_json['message']['info'])
        elif response.status_code == 403:  # 服务器状态码为403
            log_debug.logger.error(res_json['message']['info'])
        else:
            log_debug.logger.error('Unknown error')

    def send_device_resource(self, s_access_token):
        """
        发送Agent设备资源信息
        :param s_access_token: Agent注册之后返回的access_token
        :return:
        """
        payload = dict()
        payload['mac_addr'] = self.mac_addr
        payload['access_token'] = s_access_token
        payload['cpu_percent'] = psutil.cpu_percent()  # CPU占用率
        payload['cpu_count'] = psutil.cpu_count(logical=False)  # CPU非逻辑核心数
        payload['cpu_freq_current'] = psutil.cpu_freq()[0]  # CPU当前频率
        payload['cpu_freq_min'] = psutil.cpu_freq()[1]  # CPU最小频率
        payload['cpu_freq_max'] = psutil.cpu_freq()[2]  # CPU最大频率
        payload['total_memory'] = int(psutil.virtual_memory()[0] / 1024 / 1024)  # 总内存
        payload['available_memory'] = int(psutil.virtual_memory()[1] / 1024 / 1024)  # 可用内存
        payload['sensors_battery_percent'] = psutil.sensors_battery()[0]  # 电量百分比
        payload['boot_time'] = psutil.datetime.datetime.fromtimestamp(psutil.boot_time()).strftime(
            "%Y-%m-%d %H:%M:%S")  # 启动时间
        payload['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        response = requests.post(url=self.url, data=payload)
        res_json = response.json()
        if response.status_code == 200:  # 服务器状态码为200
            log_debug.logger.info(res_json['message']['info'])
        elif response.status_code == 403:  # 服务器状态码为403
            log_debug.logger.error(res_json['message']['info'])
        else:
            log_debug.logger.error('Unknown error')
