from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')  # 가상 환경에서 실행하기 위한 코드
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')

driver = webdriver.Chrome('./chromedriver.exe', options=options)

titles = []
reviews = []

for i in range(1, 38):  # 페이지
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
    driver.get(url)
    for j in range(1, 21):
        try:
            movie_title_path = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
            title = driver.find_element_by_xpath(movie_title_path).text
            print(title)
        except:
            print('error')