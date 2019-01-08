# coding=gbk
# ������վ��Ϣ
import sys

stations = None

with open("config/station_name", "r", encoding='utf-8') as file:
    station_names = file.readline()
if station_names:
    station_full_infos = station_names.split(r'@')
    stations = dict()
    for item in station_full_infos:
        station_slice = item.split('|')
        temp = dict()
        temp['simple_py'] = station_slice[0]
        temp['chi_name'] = station_slice[1]
        temp['code'] = station_slice[2]
        temp['full_py'] = station_slice[3]
        temp['index'] = station_slice[5]
        stations[station_slice[2]] = temp

purpose_code_map = {"ADULT": "����Ʊ", "0X00": "ѧ��Ʊ"}

seat_type_map = {
    'һ����': 'M',
    '�ص���': 'P',
    '������': 'O',
    '������': 9,
    'Ӳ��': 1,
    '����': 1,
    '����': 4,
    'Ӳ��': 3,
}
