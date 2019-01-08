# coding = utf-8
from ticket.log.Log import *
import json

# request 请求方法
Method = ["post", "get"]


def result_deal(response):
    """
    默认请求结果处理接口
    :param response:  session请求返回结果
    :return:
    """
    try:
        return json.loads(response.text)
    except json.decoder.JSONDecodeError:
        return response.content.decode("utf-8")


class Request:
    def __init__(self, args, deal_func=result_deal):
        """
        构造方法
        :param args
        """
        self.__session = args["session"]
        self.__method = args["method"]
        self.__url = args["url"]
        self.__params = args["params"]
        self.__data = args["data"]
        self.__deal_func = deal_func

    def request(self, show_log=True):
        """
        执行请求
        :param show_log: 是否显示日志
        :return:
        """
        execute = None
        if self.__method == "post":
            execute = self.__session.post
        elif self.__method == "get":
            execute = self.__session.get
        else:
            logger.warn("无效请求Method", self.__method)
        response = execute(url=self.__url, params=self.__params, data=self.__data)
        if show_log:
            logger.info(response.content.decode("utf-8"))
        return self.__deal_func(response)
