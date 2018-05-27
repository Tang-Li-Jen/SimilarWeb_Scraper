import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

# setting
path = '/Users/charlie/Desktop/SimilarWeb/'
driver = webdriver.Chrome(path +'chromedriver')
from_year = '2018'
from_month = '04'
from_day = '01'
to_year = '2018'
to_month = '04'
to_day = '30'

#login page
driver.get('https://account.similarweb.com/login')
time.sleep(10)

# set your account / password
email = ''
password = ''

driver.find_element_by_css_selector('#UserName--1').send_keys(email)
driver.find_element_by_css_selector('#Password--2').send_keys(password)
driver.find_element_by_css_selector('#authApp > main > div > div.login__authbox > form > button').click()


time.sleep(10)
driver.get('https://pro.similarweb.com/#/industry/topsites/All/999/1m?webSource=Total')
time.sleep(10)

req = requests.Session()
cookies = driver.get_cookies()
for cookie in cookies:
    req.cookies.set(cookie['name'],cookie['value'])
driver.close()

cat_ls = pd.read_table(path+ 'All_Categories_list.txt')
for element in cat_ls['Categories']:
	headers = {
	    'accept': 'application/json, text/plain, */*',
	    'accept-encoding':'gzip, deflate, br',
	    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
	    'referer':'https://pro.similarweb.com/',
	    'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
	    'x-requested-with': 'XMLHttpRequest',
	"x-sw-page": 'https://pro.similarweb.com/#/industry/topsites/{}/999/1m?webSource=Total'.format(element),
	"x-sw-page-view-id": "a1ebf5f3-deb3-4b29-b2d7-44a083566318"
	}
	url = 'https://pro.similarweb.com/widgetApi/TopSitesExtended/TopSitesExtended/Table?country=999&from={0}%7C{1}%7C{2}&includeSubDomains=true&isWindow=false&keys=${3}&metric=TopSitesExtended&timeGranularity=Monthly&to={4}%7C{5}%7C{6}&webSource=Total'.format(from_year, from_month, from_day, element, to_year, to_month, to_day)
	r = req.get(url, headers = headers)
	df = r.json()
	df = pd.DataFrame.from_records(df[u'Data'])
	df.to_csv(path+'/data/{}.csv'.format(element), index=False, encoding='UTF-8')
	print '{} is completed'.format(element)
