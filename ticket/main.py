# coding = gbk
from ticket.interface.Request import *
from ticket.interface.GetPassCode import *
from ticket.interface.InterfaceConfig import *
from ticket.log.Log import *
from ticket.utils.Utils import *
from ticket.config.station_name import *


def login(username="hef222@163.com", password="hef940527"):
    while True:
        # 获取登录验证码
        GetLoginPassCode(createRequestInfo("login_pass_code")).request()
        # 验证码验证
        randCode = input("输入验证码，空格分隔:")
        if randCode == "":
            continue
        check_result = Request(createRequestInfo("check_login_pass_code", [getCoordinate(randCode.split())])).request()
        if check_result["result_code"] == "4":
            login_result = Request(createRequestInfo("login", [username, password])).request()
            if login_result["result_code"] == 0:
                uamtk_auth_result = Request(createRequestInfo("uamtk_auth")).request()
                if uamtk_auth_result["result_code"] == 0:
                    Request(createRequestInfo("uam_auth_client", [uamtk_auth_result["newapptk"]])).request()
                    return True


def main():
    # 登录
    # login()
    query_info = {
        "date": date,
        "station_from": station_from,
        "station_to": station_to,
        "purpose_code": purpose_code
    }
    query_result = Request(createRequestInfo("query_left_ticket", query_info)).request()
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
    while True:
        index_train = input("输入预定车票序号:")
        temp_seat_left = show_info[int(index_train) - 1][6:]
        if temp_seat_left.count("无") + temp_seat_left.count("-") == len(temp_seat_left):
            print("该车次已经没有空位")
            continue
        else:
            order = Request(
                createRequestInfo("submit_order_request",
                                  [requests.utils.unquote(ticket_info[int(index_train) - 1][0]), date,
                                   purpose_code,
                                   stations[station_from]["chi_name"],
                                   stations[station_to]["chi_name"]])).request()
            if order["status"] is False:
                print("提交失败")
                break
    initDc_page = Request(createRequestInfo("init_dc")).request()
    jsVariable = getJsVariable(initDc_page)



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
purpose_code_map = {"ADULT": "成人票", "0X00": "学生票"}
if __name__ == '__main__':
    main()
