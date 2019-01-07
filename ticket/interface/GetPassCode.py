# coding = utf-8
from ticket.interface.Request import *
import base64


# 获取登陆验证码
class GetLoginPassCode(Request):
    def result_deal(self, response):
        image64 = json.loads(response.text)
        image_data = base64.b64decode(image64['image'])
        file = open("captcha.jpg", "wb")
        file.write(image_data)
        file.close()


# 获取下单验证码
class GetOrderPassCode(Request):
    def result_deal(self, response):
        pass
