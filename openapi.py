import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import calendar

today = datetime.date.today()
yesterday = today - datetime.timedelta(1)
yesterday_wd = calendar.day_name[yesterday.weekday()]

month = yesterday.month
day = yesterday.day

if day < 10:
    day = '0'+ str(day)
if month < 10:
    month = '0' + str(month)

yesterdate = str(yesterday.year) + str(month) + str(day)

startnumber=1
endnumber=1000
CommerceInfor = {}

if yesterday_wd == 'Sunday':
    url='http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.xml?key=388a212ee044200c65327069a5e040fe&targetDt='+yesterdate+'&weekGb=0'
else:
    url='http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key=430156241533f1d058c603178cc3ca0e&targetDt='+yesterdate
req=requests.get(url)
html=req.text
soup = BeautifulSoup(html, 'html.parser')

Names = []
Rank_change = []
total_audi = []
audi_week = []
w_date = []

date_range = soup.find('showrange')
Movie_Names = soup.find_all('movienm')
rank_int = soup.find_all('rankinten')
audicount = soup.find_all('audiacc')
audiweek = soup.find_all('audicnt')

for code in Movie_Names:
    Names.append(code.text)
for code in audiweek:
    audi_week.append(code.text)
for code in rank_int:
    Rank_change.append(code.text)
for code in audicount:
    total_audi.append(code.text)

def rank(a):
    if (int(a) < 0):
        inten = abs(int(a))
        return "↓" + str(inten)
    elif (int(a) > 0):
        return "↑" + a
    else:
        return '-'

def print_t():
    if yesterday_wd == 'Sunday':
        print("----주간 박스오피스 순위----")
        print("날짜 :", date_range.text, '\n')
    else:
        print("----일별 박스오피스 순위----")
        print("날짜 :", yesterdate, '\n')
    for i in range(0,10):
        print((i+1), "위 ", rank(Rank_change[i]))
        print(Names[i])
        print("주간관객수 :", audi_week[i])
        print("누적관객수 :", total_audi[i], '\n\n')

def printn():
    print(Names)


print_t()
