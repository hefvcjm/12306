import requests

date = '2019-02-02'
station_from = 'IZQ'
station_to = 'TAZ'
purpose_code = 'ADULT'
url = r'https://kyfw.12306.cn/otn/leftTicket/queryZ?' \
      r'leftTicketDTO.train_date=' + date + \
      '&leftTicketDTO.from_station=' + station_from + \
      '&leftTicketDTO.to_station=' + station_to + \
      '&purpose_codes=' + purpose_code
req = requests.get(url)
print(req.status_code)
print(req.text)
