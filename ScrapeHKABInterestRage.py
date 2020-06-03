from bs4 import BeautifulSoup
import urllib3
import urllib.request
from datetime import timedelta, date
import datetime
import csv
import sys

urlWArg = 'https://www.hkab.org.hk/hibor/listRates.do?lang=en&Submit=Search&year=%d&month=%d&day=%d'

def get_sibling(element):
    sibling = element.next_sibling
    if sibling == "\n":
        return get_sibling(sibling)
    else:
        return sibling


def make_soup(url):
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    txt = r.data

    return BeautifulSoup(r.data,'html.parser')
    #return BeautifulSoup(r.data,'lxml')

def GetValue(year, month, day):
    ret = ""
    soup = make_soup(urlWArg % (year, month, day))
    result1 = soup.find('td', string='1 Month')
    if result1 is not None:
        result1a = get_sibling(result1)
        ret = result1a.text
    soup.decompose()
    return ret


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

start_dt_str = input("Start Date(yyyymmdd): ")
end_dt_str = input("End Date(yyyymmdd): ")

format_str = '%Y%m%d'
start_dt = datetime.datetime.strptime(start_dt_str, format_str).date()
end_dt = datetime.datetime.strptime(end_dt_str, format_str).date()

dr = daterange(start_dt, end_dt)

filename = 'HKABInterst.csv'
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    for dt in dr:
        val = GetValue(dt.year, dt.month, dt.day)
        print ('.', end = "")
        sys.stdout.flush()
        if val != "":
            writer.writerow([dt.strftime("%Y/%m/%d"), val])
            file.flush()

print ("\nSuccessfully output to " + filename)

