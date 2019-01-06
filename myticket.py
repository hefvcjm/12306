# coding = gbk
import datetime
import os
import platform

import ntplib as ntplib
import requests
import base64
import time
import json
from PIL import Image
import matplotlib.pyplot as plt
from requests.cookies import RequestsCookieJar
import random
import copy
from requests.auth import HTTPBasicAuth

session = requests.Session()
cookies = RequestsCookieJar()


def autoSynchroTime():
    """
    同步北京时间，执行时候，请务必用sudo，sudo，sudo 执行，否则会报权限错误，windows打开ide或者cmd请用管理员身份
    :return:
    """
    c = ntplib.NTPClient()

    hosts = ['ntp1.aliyun.com', 'ntp2.aliyun.com', 'ntp3.aliyun.com', 'ntp4.aliyun.com', 'cn.pool.ntp.org']

    print(u"正在同步时间，请耐心等待30秒左右")
    print(u"系统当前时间{}".format(str(datetime.datetime.now())[:22]))
    system = platform.system()
    if system == "Windows":  # windows 同步时间未测试过，参考地址：https://www.jianshu.com/p/92ec15da6cc3
        for host in hosts:
            os.system('w32tm /register')
            os.system('net start w32time')
            os.system('w32tm /config /manualpeerlist:"{}" /syncfromflags:manual /reliable:yes /update'.format(host))
            os.system('ping -n 3 127.0.0.1 >nul')
            sin = os.system('w32tm /resync')
            if sin is 0:
                break
    else:  # mac同步地址，如果ntpdate未安装，brew install ntpdate    linux 安装 yum install -y ntpdate
        for host in hosts:
            sin = os.system('ntpdate {}'.format(host))
            if sin is 0:
                break
    print(u"同步后时间:{}".format(str(datetime.datetime.now())[:22]))


headers_base = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}


def getPassCode():
    url = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&{0}".format(
        random.random())
    headers = copy.deepcopy(headers_base)
    headers["Connection"] = "keep-alive"
    headers["Host"] = "kyfw.12306.cn"
    headers["Referer"] = "https://kyfw.12306.cn/otn/resources/login.html"
    req = session.get(url, headers=headers)
    print(req.status_code)
    JSON = json.loads(req.text)
    print(JSON)
    imagedata = base64.b64decode(JSON['image'])
    name = str(random.randint(0, 10 ** 6))
    file = open('pictures\\' + name + '.jpg', "wb")
    file.write(imagedata)
    file.close()
    img = Image.open('pictures\\' + name + '.jpg')
    plt.figure("picture")
    plt.imshow(img)
    plt.show()
    print(req.cookies)
    session.cookies = req.cookies


def checkPassCode(randCode):
    url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
    data = {
        "answer": randCode,
        "rand": "sjrand",
        "login_site": "E"
    }
    headers = copy.deepcopy(headers_base)
    headers["Connection"] = "keep-alive"
    headers["Host"] = "kyfw.12306.cn"
    headers["Referer"] = "https://kyfw.12306.cn/otn/login/init"
    req = session.post(url, data=data, headers=headers)
    print(req.text)
    return json.loads(req.text)


def login(username, password, randCode):
    auth = HTTPBasicAuth("appid", "otn")
    url = "https://kyfw.12306.cn/passwort/web/login"
    data = {'username': username, "password": password, "appid": "otn", "answer": randCode}
    headers = copy.deepcopy(headers_base)
    headers["Connection"] = "keep-alive"
    headers["Host"] = "kyfw.12306.cn"
    headers["Referer"] = "https://kyfw.12306.cn/otn/login/init"
    headers["Content-Length"] = str(len(data))
    req = session.post(url, data=data, headers=headers, cookies=session.cookies, auth=auth)
    print(req.status_code)
    print(req.content.decode("utf-8"))
    print(req.url)


# autoSynchroTime()
getPassCode()
randCode = input("输入验证码:")
check_result = checkPassCode(randCode)
if check_result["result_code"] == "4":
    print("验证成功")
    login("hef222@163.com", "hef940527", randCode)
