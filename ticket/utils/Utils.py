# coding = gbk

# 获取验证码对应坐标
import json
import re


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


# 解析查询结果
def parseQueryResult(result):
    left_info_list = result["data"]["result"]
    split_info_list = [item.split("|") for item in left_info_list]
    # |20|21高级软座|22|23软卧一等卧|24|25|26无座|27|28硬卧二等卧|29硬座|30二等座|31一等座|32商务特等座|33动卧|
    station_map = result["data"]["map"]
    show_index = [3, 4, 7, 8, 9, 10, 31, 30, 26, 33, 32, 28, 29, 23, 21]
    show_name = ['车次', '出发站', '到达站', '出发时间', '到达时间', '时长', '一等座', '二等座', '无座', '动卧', '商务特等座', '硬卧', '硬座', '软卧',
                 '高级软卧']
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


def getJsVariable(initDcPage):
    token_name = re.compile(r"var globalRepeatSubmitToken = '(\S+)'")
    ticketInfoForPassengerForm_name = re.compile(r'var ticketInfoForPassengerForm=(\{.+\})?')
    order_request_params_name = re.compile(r'var orderRequestDTO=(\{.+\})?')
    token = re.search(token_name, initDcPage).group(1)
    re_tfpf = re.findall(ticketInfoForPassengerForm_name, initDcPage)
    re_orp = re.findall(order_request_params_name, initDcPage)
    if re_tfpf:
        ticketInfoForPassengerForm = json.loads(re_tfpf[0].replace("'", '"'))
    else:
        ticketInfoForPassengerForm = ""
    if re_orp:
        order_request_params = json.loads(re_orp[0].replace("'", '"'))
    else:
        order_request_params = ""
    return {
        "REPEAT_SUBMIT_TOKEN": token,
        "ticketInfoForPassengerForm": ticketInfoForPassengerForm,
        "order_request_params": order_request_params,
    }
