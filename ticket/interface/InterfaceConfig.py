# coding = utf-8
import random
import requests
import datetime
import copy
from ticket.log.Log import *

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
                                " AppleWebKit/537.36 (KHTML, like Gecko) " \
                                "Chrome/71.0.3578.98 Safari/537.36"


# 用来占位
class Placeholder:
    def __init__(self, name):
        self.name = name


def createRequestInfo(name, fill_data=None):
    """
    构造请求信息
    :param name: INTERFACE_CONFIG中的某个键名
    :param fill_data: 按照Placeholder.name为键的字典或者按照Placeholder顺序的列表
    :return: 构造好的请求信息
    """

    def fillPlaceHolder(info_dict, args):
        nonlocal index
        if isinstance(args, dict):
            for key, value in info_dict.items():
                if isinstance(value, dict):
                    fillPlaceHolder(value, args)
                elif isinstance(value, Placeholder):
                    info_dict[key] = args[value.name]
        elif isinstance(args, list):
            for key, value in info_dict.items():
                if isinstance(value, dict):
                    fillPlaceHolder(value, args)
                elif isinstance(value, Placeholder):
                    info_dict[key] = args[index]
                    index = index + 1
        return info_dict

    index = 0
    request_info = fillPlaceHolder(copy.deepcopy(INTERFACE_CONFIG[name]), fill_data)
    if request_info is None:
        return None
    request_info["session"] = session
    logger.debug(request_info)
    return request_info


INTERFACE_CONFIG = {
    # 获取登陆验证码
    "login_pass_code": {
        "method": "get",
        "url": "https://kyfw.12306.cn/passport/captcha/captcha-image64",
        "params": {
            "login_site": "E",
            "module": "login",
            "rand": "sjrand",
            str(random.random()): ""
        },
        "data": None
    },
    # 发送验证码验证
    "check_login_pass_code": {
        "method": "post",
        "url": "https://kyfw.12306.cn/passport/captcha/captcha-check",
        "data": {
            "answer": Placeholder("randCode"),
            "rand": "sjrand",
            "login_site": "E",
        }
    },
    # 登陆
    "login": {
        "method": "post",
        "url": "https://kyfw.12306.cn/passport/web/login",
        "params": None,
        "data": {
            "username": Placeholder("username"),
            "password": Placeholder("password"),
            "appid": "otn",
        }
    },
    # uamtk验证
    "uamtk_auth": {
        "method": "post",
        "url": "https://kyfw.12306.cn/passport/web/auth/uamtk",
        "params": None,
        "data": {
            "appid": "otn",
        }
    },
    # uamtk验证客户端
    "uam_auth_client": {
        "method": "post",
        "url": "https://kyfw.12306.cn/passport/web/auth/uamtk",
        "params": None,
        "data": {
            "tk": Placeholder("tk"),
        }
    },
    # 查询余票
    "query_left_ticket": {
        "method": "get",
        "url": 'https://kyfw.12306.cn/otn/leftTicket/queryZ',
        "params": {
            "leftTicketDTO.train_date": Placeholder("date"),
            "leftTicketDTO.from_station": Placeholder("station_from"),
            "leftTicketDTO.to_station": Placeholder("station_to"),
            "purpose_codes": Placeholder("purpose_code")
        },
        "data": None
    },
    # 检查用户登录状态
    "check_user": {
        "method": "post",
        "url": "https://kyfw.12306.cn/otn/login/checkUser",
        "params": None,
        "data": {
            "_json_att": ""
        },
    },
    # 请求下单
    "submit_order_request": {
        "method": "post",
        "url": "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest",
        "params": None,
        "data": {
            "secretStr": Placeholder("secretStr"),
            "train_date": Placeholder("train_date"),
            "back_train_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "tour_flag": "dc",
            "purpose_codes": Placeholder("purpose_codes"),
            "query_from_station_name": Placeholder("query_from_station_name"),
            "query_to_station_name": Placeholder("query_to_station_name"),
            "undefined": ""
        },
    },
    # 下单页面
    "init_dc": {
        "method": "post",
        "url": "https://kyfw.12306.cn/otn/confirmPassenger/initDc",
        "params": None,
        "data": {
            "_json_att": "",
        }
    },
    # 获取乘客信息
    "get_passenger_dto": {
        "method": "post",
        "url": "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs",
        "params": None,
        "data": {
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": Placeholder("REPEAT_SUBMIT_TOKEN")
        }
    },
    # 获取下单验证码
    "order_pass_code": {
        "method": "get",
        "url": "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew",
        "params": {
            "module": "passenger",
            "rand": "randp",
            str(random.random()): ""
        },
        "data": None
    },
    # 检查订单信息
    "check_order_info": {
        "method": "post",
        "url": "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo",
        "params": None,
        "data": {
            "cancel_flag": "2",
            "bed_level_order_num": "000000000000000000000000000000",
            "passengerTicketStr": Placeholder("passengerTicketStr"),
            "oldPassengerStr": Placeholder("oldPassengerStr"),
            "tour_flag": "dc",
            "randCode": "",
            "whatsSelect": Placeholder("whatsSelect"),
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": Placeholder("REPEAT_SUBMIT_TOKEN")
        }
    },
    # 检查队列信息
    "order_queue": {
        "method": "post",
        "url": "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount",
        "params": None,
        "data": {
            "train_date": Placeholder("train_date"),
            "train_no": Placeholder("train_no"),  # 列车编号 2
            "stationTrainCode": Placeholder("stationTrainCode"),  # 列车代号 3
            "seatType": Placeholder("seatType"),
            "fromStationTelecode": Placeholder("fromStationTelecode"),  # 出发站代号
            "toStationTelecode": Placeholder("toStationTelecode"),  # 到达站代号
            "leftTicket": Placeholder("leftTicket"),
            "purpose_codes": Placeholder("purpose_codes"),
            "train_location": Placeholder("train_location"),
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": Placeholder("REPEAT_SUBMIT_TOKEN")
        }
    },
    # 确认订单
    "confirm_single_queue": {
        "method": "post",
        "url": "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue",
        "params": None,
        "data": {
            "passengerTicketStr": Placeholder("passengerTicketStr"),
            "oldPassengerStr": Placeholder("oldPassengerStr"),
            "randCode": "",
            "purpose_codes": Placeholder("purpose_codes"),
            "key_check_isChange": Placeholder("key_check_isChange"),
            "leftTicketStr": Placeholder("leftTicketStr"),
            "train_location": Placeholder("train_location"),
            "choose_seats": "",
            "seatDetailType": "",
            "whatsSelect": Placeholder("whatsSelect"),
            "roomType": "00",
            "dwAll": "N",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": Placeholder("REPEAT_SUBMIT_TOKEN")
        }
    },
    # 查询等待时间
    "query_waiting_time": {
        "method": "get",
        "url": "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime",
        "params": {
            "random": "1546777824674",
            "tourFlag": "dc",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": Placeholder("REPEAT_SUBMIT_TOKEN")
        },
        "data": None
    },
    #
    "result_order_dc_queue": {
        "method": "post",
        "url": "https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue",
        "params": None,
        "data": {
            "orderSequence_no": Placeholder("orderSequence_no"),
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": Placeholder("REPEAT_SUBMIT_TOKEN")
        }
    },
    #
    "init_order_page": {
        "method": "post",
        "url": "https://kyfw.12306.cn/otn//payOrder/init",
        "params": {
            "random": "1546777828848"
        },
        "data": {
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": Placeholder("REPEAT_SUBMIT_TOKEN")
        }
    }
}
