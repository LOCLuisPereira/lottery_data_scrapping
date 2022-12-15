from bs4 import BeautifulSoup
import requests
import re

handler_csv = open('euromillions.csv','w')
print(
    'day_of_week,year,month,day,n1,n2,n3,n4,n5,s1,s2',
    file=handler_csv
)

url = 'https://portalseven.com/lottery/euromillions_winning_numbers.jsp?fromDate=2021-12-12&toDate=2022-12-12&viewType=3#'
raw = requests.get(url).text

html_tree = BeautifulSoup(raw, 'html.parser')

html_table = str(html_tree.find(
    'table',
    class_='table table-bordered table-condensed table-striped text-center table-hover'
))

for entry in html_table.split('<tr>')[1:] :
    # 2011 MAR 18 has one value missing
    try :
        dt = re.findall('<td class="text-left">(.*)</', entry)[0] 
        nm = [int(n) for n in re.findall('b>([0-9]+)</b', entry)]
    except :
        print(entry)

    dt = dt.split(',')
    day_of_the_week = dt[0].lower()
    month = re.findall('([a-z]*)', dt[1].replace(' ','').lower())[0]
    day = re.findall('([0-9]+)', dt[1].replace(' ','').lower())[0]
    year = int(dt[2].replace(' ', ''))

    nms = ','.join(str(n) for n in nm)

    print(
        f'''{day_of_the_week},{year},{month},{day},{nms}''',
        file=handler_csv
    )