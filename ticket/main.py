# coding = gbk
from ticket.interface.Request import *
from ticket.interface.InterfaceConfig import *
from ticket.log.Log import *
from ticket.utils.Utils import *
from ticket.config.Config import *
import base64


def request(name, arg=None, deal_func=result_deal, show_log=True):
    return Request(createRequestInfo(name, arg), deal_func=deal_func).request(show_log=show_log)


def login(username="hef222@163.com", password="hef940527"):
    def save_image(response):
        image64 = json.loads(response.text)
        image_data = base64.b64decode(image64['image'])
        file = open("captcha.jpg", "wb")
        file.write(image_data)
        file.close()

    while True:
        # 获取登录验证码
        request("login_pass_code", deal_func=save_image)
        # 验证码验证
        randCode = input("输入验证码，空格分隔:")
        if randCode == "":
            continue
        check_result = request("check_login_pass_code", [getCoordinate(randCode.split())])
        if check_result["result_code"] == "4":
            login_result = request("login", [username, password])
            if login_result["result_code"] == 0:
                uamtk_auth_result = request("uamtk_auth")
                if uamtk_auth_result["result_code"] == 0:
                    request("uam_auth_client", [uamtk_auth_result["newapptk"]])
                    return True


def main():
    user_check_result = request("check_user")
    if user_check_result["data"]["flag"] is False:
        login()
        print("用户未登录，请重新登录")
    query_info = {
        "date": date,
        "station_from": station_from,
        "station_to": station_to,
        "purpose_code": purpose_code
    }
    query_result = request("query_left_ticket", query_info)
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
            order = request("submit_order_request",
                            [requests.utils.unquote(ticket_info[int(index_train) - 1][0]), date,
                             purpose_code,
                             stations[station_from]["chi_name"],
                             stations[station_to]["chi_name"]], show_log=False)
            if order["status"] is False:
                print("提交失败")
                continue
            break
    initDc_page = request("init_dc", show_log=False)
    jsVariable = getJsVariable(initDc_page)
    print(str(jsVariable).replace("'", "\""))
    REPEAT_SUBMIT_TOKEN = jsVariable["REPEAT_SUBMIT_TOKEN"]
    print("REPEAT_SUBMIT_TOKEN:", REPEAT_SUBMIT_TOKEN)
    passenger_info = request("get_passenger_dto", [REPEAT_SUBMIT_TOKEN])
    passenger_list = passenger_info["data"]["normal_passengers"]
    n = 1
    print("乘客信息:")
    for item in passenger_list:
        print(n, '\t', item["passenger_name"] + (
            "(%s)" % item["passenger_type_name"] if item["passenger_type_name"] == "学生" else ""))
        n += 1
    index = input("选择乘客编号，空格分隔:")
    passenger_index = [int(i) - 1 for i in index.strip().split()]
    commit_passenger_info = ["passenger_flag", "passenger_type", "passenger_name",
                             "passenger_id_type_code",
                             "passenger_id_no", "mobile_no"]
    commit_passenger_info_old = ["passenger_name", "passenger_flag", "passenger_id_type_code",
                                 "passenger_type", ]
    passengerTicketStr_list = []
    oldPassengerStr_list = []
    for index in passenger_index:
        temp = [seat_type]
        for name in commit_passenger_info:
            temp.append(passenger_list[index][name])
        temp.append("N")
        old_temp = []
        for name in commit_passenger_info_old:
            old_temp.append(passenger_list[index][name])
        old_temp.append("")
        passengerTicketStr_list.append(",".join(temp))
        oldPassengerStr_list.append(",".join(old_temp))
    passengerTicketStr = "_".join(passengerTicketStr_list)
    oldPassengerStr = "".join(oldPassengerStr_list)
    request("check_order_info", [passengerTicketStr, oldPassengerStr, "1", REPEAT_SUBMIT_TOKEN])
    go_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    time_format = '%a %d %b %Y 00:00:00 GMT+0800 (China Standard Time)'
    train_date = go_date.strftime(time_format)
    train_no = ticket_info[int(index_train) - 1][2]
    stationTrainCode = ticket_info[int(index_train) - 1][3]
    seatType = "0"
    fromStationTelecode = station_from
    toStationTelecode = station_to
    leftTicket = ticket_info[int(index_train) - 1][12]
    purpose_codes = jsVariable["ticketInfoForPassengerForm"]["purpose_codes"]
    train_location = ticket_info[int(index_train) - 1][15]
    request("order_queue", [train_date, train_no, stationTrainCode, seatType, fromStationTelecode,
                            toStationTelecode,
                            leftTicket,
                            purpose_codes, train_location, REPEAT_SUBMIT_TOKEN])
    key_check_isChange = jsVariable["ticketInfoForPassengerForm"]["key_check_isChange"]
    request("confirm_single_queue", [passengerTicketStr, oldPassengerStr, purpose_codes, key_check_isChange,
                                     leftTicket, train_location, "1", REPEAT_SUBMIT_TOKEN])
    orderSequence_no = jsVariable["order_request_params"]["sequence_no"]
    # print(json.dumps(jsVariable, sort_keys=True, indent=4, separators=(',', ':')))
    orderSequence_no = orderSequence_no if orderSequence_no is not None else ""
    request("result_order_dc_queue", [orderSequence_no, REPEAT_SUBMIT_TOKEN])


# 查询信息
# 发车站
station_from = "IZQ"
# 到达站
station_to = "TAZ"
# 日期
date = "2019-01-10"
# 类型
purpose_code = "ADULT"
# 座位类型
seat_type = 'O'
#https://gist.github.com/hefvcjm/d2a48e6050e750824e309783fb938cf6

if __name__ == '__main__':
    login()
    main()
