# coding = gbk
sort_name = ["商务特等座", "一等座", "二等座", "高级软座", "软卧一等卧", "动卧", "硬卧二等卧", "软座", "硬座", "无座", "其他"]
a = '|20|21高级软座|22|23软卧一等卧|24|25|26无座|27|28硬卧二等卧|29硬座|30二等座|31一等座|32商务特等座|33动卧|'
index_name_dict = {21: '高级软座', 23: '软卧一等卧', 26: '无座', 28: '硬卧二等卧', 29: '硬座', 30: '二等座', 31: '一等座', 32: '商务特等座',
                   33: '动卧'}
s = r"hVXhuJriQfFR24C%2BIrKCIzZefyNfUlhJTlxYLkpyFG0DBrVDweZqq%2BVD29kV2VlmPRgFwvubGg%2BC%0AzU5At%2BiQ1qN%2BVg%2FWZoE7KtaaaYqjmXBvRqmkMkTzahJwB%2B2v1IMqe20lBcKWZN%2BOEJGFR793Z7yo%0A6UoUh9biIQqQWQnKrwDfG5sfYYF2H2gdiCFtUG%2FR80rabSIrh1OFZetq4OSzyWvcnonHk5JOH0c6%0AlUVm7V9aMhtWvBiOT170UUp3zvcbEL%2FshfLootYGY6gQMV4AU%2BtkDEkFAegui9ODhaFiUazZBxKU%0A|预订|6c000G140801|G1408|IZQ|NXG|IZQ|CWQ|06:23|09:05|02:42|Y|52XfSIGGr%2BZTDivs%2BjwpNkYWG%2FQ0W%2FtN%2FFacH4ALcp4SVA0f|20190110|3|QZ|01|05|1|0|||||||||||有|7|4||O0M090|OM9|1|0"
a = s.split('|')
left_tickets = {}
for i in index_name_dict.keys():
    left_tickets[index_name_dict[i]] = a[i]
print(left_tickets)
print(sorted(sort_name))
temp = dict()
n = 0
for i in a:
    temp[n] = a[n]
    n += 1
print(temp)
