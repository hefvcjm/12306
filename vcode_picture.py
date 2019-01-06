# coding = gbk
import requests
import base64
import time
import json
from PIL import Image
import matplotlib.pyplot as plt

session = requests.session()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "kyfw.12306.cn",
    "If-Modified-Since": "Tue, 06 Nov 2018 07:12:00 GMT",
    "Referer": "https://kyfw.12306.cn/otn/view/index.html",
    "Upgrade-Insecure-Requests": 1,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", }
session.get('https://kyfw.12306.cn/otn/resources/login.html')

stamp = str(int(time.time()))
url = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&" + stamp
url = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&" + stamp + "&callback=jQuery191013772607308618667_1546665518041&_=" + stamp
headers = {
    "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Connection": "keep-alive",
    "Host": "kyfw.12306.cn",
    "Referer": "https://kyfw.12306.cn/otn/resources/login.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"}
req = session.get(url, headers=headers, cookies=session.cookies)
print(req.status_code)
print(req.text)
JSON = json.loads(req.text[req.text.index('(') + 1:-2])
print(JSON)
imagedata = base64.b64decode(JSON['image'])
file = open('pictures\\' + stamp + '.jpg', "wb")
file.write(imagedata)
file.close()
img = Image.open('pictures\\' + stamp + '.jpg')
plt.figure("picture")
plt.imshow(img)
plt.show()

conf_url = "https://kyfw.12306.cn/otn/login/conf"
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Connection": "keep-alive",
    "Host": "kyfw.12306.cn",
    "Origin": "https://kyfw.12306.cn",
    "Referer": "https://kyfw.12306.cn/otn/resources/login.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"}
req = session.post(conf_url, headers=headers, cookies=session.cookies)
print(req.content.decode('utf-8'))

randCode = input("输入验证码:")

checkCode_url = "https://kyfw.12306.cn/passport/captcha/captcha-check?callback=jQuery191013772607308618667_1546665518041&answer=" + randCode.replace(
    ',', '%2C') + "&rand=sjrand&login_site=E&_=" + stamp
data_check = {'answer': randCode, 'rand': 'sjrand', 'login_site': 'E'}
req_check = session.get(checkCode_url, cookies=session.cookies)
print(req_check.url)
print(req_check.status_code)
print(req_check.content.decode('utf-8'))

JSON = json.loads(req_check.text[req_check.text.index('(') + 1:-2])
print(JSON)

auth_url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
req = session.post(auth_url, data={"appid": "otn"})
print(req.content.decode('utf-8'))

if JSON['result_code'] == "4":
    banner_url = 'https://kyfw.12306.cn/otn/index12306/getLoginBanner'
    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Connection": "keep-alive",
        "Host": "kyfw.12306.cn",
        "Referer": "https://kyfw.12306.cn/otn/resources/login.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}
    req = session.get(banner_url, headers=headers, cookies=session.cookies)
    print(req.content.decode('utf-8'))

    login_url = "https://kyfw.12306.cn/passwort/web/login"
    data = {'username': "hef222@163.com", "password": "hef940527", "appid": "otn", "answer": randCode}
    headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
               "Connection": "keep-alive",
               "Host": "kyfw.12306.cn",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Origin": "https://kyfw.12306.cn",
               "Referer": "https://kyfw.12306.cn/otn/resources/login.html",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
               "X-Requested-With": "XMLHttpRequest"}
    req_login = requests.post(login_url, data=data, headers=headers, cookies=session.cookies)
    print(req_login.url)
    print(req_login.status_code)
    print(req_login.content.decode('utf-8'))
