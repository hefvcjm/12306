# coding = gbk
import requests
import random
import base64
import json
import datetime
from station_name import stations

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
                                " AppleWebKit/537.36 (KHTML, like Gecko) " \
                                "Chrome/71.0.3578.98 Safari/537.36"


# 获取验证码图片
def getPassCode():
    captcha_url = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&{0}".format(
        random.random())
    req = session.get(captcha_url)
    image64 = json.loads(req.text)
    image_data = base64.b64decode(image64['image'])
    file = open("captcha.jpg", "wb")
    file.write(image_data)
    file.close()
    print(req.content.decode("utf-8"))


# 发送验证码验证
def checkPassCode(randCode):
    check_url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
    data = {
        "answer": randCode,
        "rand": "sjrand",
        "login_site": "E",
    }
    req = session.post(check_url, data)
    print(req.content.decode("utf-8"))
    check_result = json.loads(req.text)
    return check_result


# 登录
def login(username="hef222@163.com", password="hef940527"):
    login_url = "https://kyfw.12306.cn/passport/web/login"
    data = {
        "username": username,
        "password": password,
        "appid": "otn",
    }
    req = session.post(login_url, data)
    print(req.content.decode("utf-8"))
    return json.loads(req.text)


# 获取验证码对应坐标
def getCoordinate(num):
    map_pos = {
        1: "37,35",
        2: "107,35",
        3: "181,35",
        4: "255,35",
        5: "37,115",
        6: "107,115",
        7: "181,115",
        8: "255,115"
    }
    result = []
    for i in num:
        result.append(map_pos[int(i)])
    return ','.join(result)


# uamtk验证
def uamtkAuth():
    uamtk_auth_url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
    data = {
        "appid": "otn"
    }
    req = session.post(uamtk_auth_url, data)
    print(req.content.decode("utf-8"))
    return json.loads(req.text)


# 验证
def uamAuthClient(tk):
    auth_url = "https://kyfw.12306.cn/otn/uamauthclient"
    data = {
        "tk": tk
    }
    req = session.post(auth_url, data)
    print(req.content.decode("utf-8"))


def queryLeftTicket(station_from="IZQ", station_to="TAZ", date="2019-01-10", purpose_code="ADULT"):
    url = r'https://kyfw.12306.cn/otn/leftTicket/queryZ?' \
          r'leftTicketDTO.train_date=' + date + \
          '&leftTicketDTO.from_station=' + station_from + \
          '&leftTicketDTO.to_station=' + station_to + \
          '&purpose_codes=' + purpose_code
    req = session.get(url)
    print(req.status_code)
    print(req.content.decode("utf-8"))
    return json.loads(req.text)


# 解析查询结果
def parseQueryResult(result):
    left_info_list = result["data"]["result"]
    split_info_list = [item.split("|") for item in left_info_list]
    # |20|21高级软座|22|23软卧一等卧|24|25|26无座|27|28硬卧二等卧|29硬座|30二等座|31一等座|32商务特等座|33动卧|
    station_map = result["data"]["map"]
    show_index = [3, 4, 7, 8, 9, 10, 31, 30, 26, 33, 32, 28, 29, 23, 21]
    show_name = ['车次', '出发站', '到达站', '出发时间', '到达时间', '时长', '一等座', '二等座', '无座', '动卧', '商务特等座', '硬卧二等卧', '硬座', '软卧一等卧',
                 '高级软座']
    show_info_list = []
    for item in split_info_list:
        temp = []
        for i in show_index:
            if item[i] == "":
                temp.append("-")
            else:
                if i in [4, 7]:
                    temp.append(station_map[item[i]])
                else:
                    temp.append(item[i])
        show_info_list.append(temp)
    return show_name, show_info_list, split_info_list


# 检查用户登录状态
def checkUser():
    url = "https://kyfw.12306.cn/otn/login/checkUser"
    data = {
        "_json_att": ""
    }
    req = session.post(url, data)
    print(req.content.decode("utf-8"))
    return json.loads(req.text)


# 请求下单
def submitOrderRequest(secretStr, train_date, purpose_codes, query_from_station_name, query_to_station_name):
    url = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
    data = {
        "secretStr": secretStr,
        "train_date": train_date,
        "back_train_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "tour_flag": "dc",
        "purpose_codes": purpose_codes,
        "query_from_station_name": query_from_station_name,
        "query_to_station_name": query_to_station_name,
        "undefined": ""
    }
    print(data)
    req = session.post(url, data)
    print(req.content.decode("utf-8"))
    return json.loads(req.text)


# 下单页面
def initDc():
    url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
    data = {
        "_json_att": ""
    }
    req = session.post(url, data)
    print(req.content.decode("utf-8"))


# 获取乘客信息
def getPassengerDTOS():
    url = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
    data = {
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": ""
    }
    req = session.post(url, data)
    print(req.content.decode("utf-8"))


def getPassCodeNew():
    url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&" + str(random.random())
    req = session.get(url)
    image64 = json.loads(req.text)
    image_data = base64.b64decode(image64['image'])
    file = open("passCodeNew.jpg", "wb")
    file.write(image_data)
    file.close()
    print(req.content.decode("utf-8"))


def checkOrderInfo(cancel_flag, bed_level_order_num, passengerTicketStr, oldPassengerStr, tour_flag, whatsSelect,
                   REPEAT_SUBMIT_TOKEN):
    url = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
    data = {
        "cancel_flag": cancel_flag,
        "bed_level_order_num": bed_level_order_num,
        "passengerTicketStr": passengerTicketStr,
        "oldPassengerStr": oldPassengerStr,
        "tour_flag": tour_flag,
        "randCode": "",
        "whatsSelect": whatsSelect,
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": REPEAT_SUBMIT_TOKEN
    }
    req = session.post(url, data)
    print(req.content.decode("utf-8"))


# cancel_flag: 2
# bed_level_order_num: 000000000000000000000000000000
# passengerTicketStr: O,0,3,黄恩芳,1,450422199507080017,15823086497,N_O,0,1,陈大东,1,452423196610153311,,N
# oldPassengerStr: 黄恩芳,1,450422199507080017,3_陈大东,1,452423196610153311,1_
# tour_flag: dc
# randCode:
# whatsSelect: 1
# _json_att:
# REPEAT_SUBMIT_TOKEN: cdaff9cee1daf1fcc03168fb436fc691

def getQueueCount(train_date, train_no, stationTrainCode, seatType, fromStationTelecode, toStationTelecode, leftTicket,
                  purpose_codes, train_location, REPEAT_SUBMIT_TOKEN):
    url = "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
    data = {
        "train_date": train_date,
        "train_no": train_no,
        "stationTrainCode": stationTrainCode,
        "seatType": seatType,
        "fromStationTelecode": fromStationTelecode,
        "toStationTelecode": toStationTelecode,
        "leftTicket": leftTicket,
        "purpose_codes": purpose_codes,
        "train_location": train_location,
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": REPEAT_SUBMIT_TOKEN
    }
    req = session.post(url, data)
    print(req.content.decode("utf-8"))


# train_date: Thu Jan 10 2019 00:00:00 GMT+0800 (China Standard Time)
# train_no: 6c000G140801
# stationTrainCode: G1408
# seatType: O
# fromStationTelecode: IZQ
# toStationTelecode: CWQ
# leftTicket: CTZ7ZN5CyfxdYfxYlaEbPqwTNaySxI2OImVy2SUz9zudWt5M
# purpose_codes: 00
# train_location: QZ
# _json_att:
# REPEAT_SUBMIT_TOKEN: cdaff9cee1daf1fcc03168fb436fc691

def confirmSingleForQueue(passengerTicketStr, oldPassengerStr, purpose_codes, key_check_isChange, train_location,
                          choose_seats, seatDetailType, whatsSelect, roomType, dwAll, REPEAT_SUBMIT_TOKEN):
    url = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
    data = {
        "passengerTicketStr": passengerTicketStr,
        "oldPassengerStr": oldPassengerStr,
        "randCode": "",
        "purpose_codes": purpose_codes,
        "key_check_isChange": key_check_isChange,
        "train_location": train_location,
        "choose_seats": choose_seats,
        "seatDetailType": seatDetailType,
        "whatsSelect": whatsSelect,
        "roomType": roomType,
        "dwAll": dwAll,
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": REPEAT_SUBMIT_TOKEN
    }
    req = session.post(url, data)
    print(req.content.decode("utf-8"))


# passengerTicketStr: O,0,3,黄恩芳,1,450422199507080017,15823086497,N_O,0,1,陈大东,1,452423196610153311,,N
# oldPassengerStr: 黄恩芳,1,450422199507080017,3_陈大东,1,452423196610153311,1_
# randCode:
# purpose_codes: 00
# key_check_isChange: 08BFCE9B4FC5D53CF4BFFF923DDEE0F9A59C68C33696238F71CA6DA6
# leftTicketStr: CTZ7ZN5CyfxdYfxYlaEbPqwTNaySxI2OImVy2SUz9zudWt5M
# train_location: QZ
# choose_seats: 1D1F
# seatDetailType: 000
# whatsSelect: 1
# roomType: 00
# dwAll: N
# _json_att:
# REPEAT_SUBMIT_TOKEN: cdaff9cee1daf1fcc03168fb436fc691

def queryOrderWaittingTime(tourFlag, REPEAT_SUBMIT_TOKEN):
    url = "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=1546777824674&tourFlag=" \
          + tourFlag + "&_json_att=&REPEAT_SUBMIT_TOKEN=" + REPEAT_SUBMIT_TOKEN
    req = session.get(url)
    print(req.content.decode("utf-8"))


def resultOrderForDcQueue(orderSequence_no, REPEAT_SUBMIT_TOKEN):
    url = "https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
    data = {
        "orderSequence_no": orderSequence_no,
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": REPEAT_SUBMIT_TOKEN
    }
    req = session.post(url, data)
    print(req.content.decode("utf-8"))


def initOrderPage(REPEAT_SUBMIT_TOKEN):
    url = "https://kyfw.12306.cn/otn//payOrder/init?random=1546777828848"
    data = {
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": REPEAT_SUBMIT_TOKEN
    }
    req = session.post(url, data)
    print(req.content.decode("utf-8"))


# orderSequence_no: EC75120458
# _json_att:
# REPEAT_SUBMIT_TOKEN: cdaff9cee1daf1fcc03168fb436fc691

# 查询信息
# 发车站
station_from = "IZQ"
# 到达站
station_to = "TAZ"
# 日期
date = "2019-01-10"
# 类型
purpose_code = "ADULT"
# 车票类型map
purpose_code_map = {"ADULT": "成人票"}

while True:
    session = requests.Session()
    getPassCode()
    randCode = input("输入验证码:")
    if randCode == "":
        continue
    check_result = checkPassCode(getCoordinate(randCode.split()))
    if check_result["result_code"] == "4":
        login_result = login()
        if login_result["result_code"] == 0:
            uamtk_auth_result = uamtkAuth()
            if uamtk_auth_result["result_code"] == 0:
                uamAuthClient(uamtk_auth_result["newapptk"])
                query_result = queryLeftTicket()
                user_check_result = checkUser()
                if user_check_result["data"]["flag"] is False:
                    print("用户未登录，请重新登录")
                    continue
                show_name, show_info, ticket_info = parseQueryResult(query_result)
                print("查询信息如下:")
                print("出发站:", stations[station_from]["chi_name"])
                print("到达站:", stations[station_to]["chi_name"])
                print("日期:", date)
                print("车票类型:", purpose_code_map[purpose_code])
                print(end="\t\t")
                for item in show_name:
                    print(item, end="\t\t")
                print()
                n = 1
                for item in show_info:
                    print(n, end="\t\t")
                    n += 1
                    for i in item:
                        print(i, end="\t\t")
                    print()
                index = input("输入预定车票序号:")
                order = submitOrderRequest(requests.utils.unquote(ticket_info[int(index) - 1][0]), date, purpose_code,
                                           stations[station_from]["chi_name"],
                                           stations[station_to]["chi_name"])
                if order["status"] is False:
                    pass

                break

# checkUser()
# queryLeftTicket()
