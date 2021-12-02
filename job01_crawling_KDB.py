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

# 영화 제목 xpath
# //*[@id="old_content"]/ul/li[1]/a
# //*[@id="old_content"]/ul/li[2]/a
# //*[@id="old_content"]/ul/li[20]/a
# //*[@id="movieEndTabMenu"]/li[6]/a/em  리뷰버튼,
# //*[@id="reviewTab"]/div/div/div[2]/span/em 리뷰 건수

# //*[@id="pagerTagAnchor1"]   리뷰 페이지 버튼
# //*[@id="pagerTagAnchor10"]/em   리뷰 다음 페이지 버튼
# //*[@id="reviewTab"]/div/div/ul/li[1]/a/strong 리뷰 제목
# //*[@id="SE-ec9bce5c-9be3-47a9-9957-b075426d88fb"] 리뷰 한 줄
# //*[@id="content"]/div[1]/div[4]/div[1]/div[4]        # class:user_tx_area

review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'

review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'

for i in range(1, 38):  # 페이지
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
    for j in range(1, 21):  # 한페이지 최대 타이틀
        try:
            driver.get(url)
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
            title = driver.find_element_by_xpath(movie_title_xpath).text
            print("+++++++++++++++++++++++++++++++++++++++++++++++++")
            print("title :", title)
            driver.find_element_by_xpath(movie_title_xpath).click()
            # driver.find_element_by_xpath(review_button_xpath).click()
            review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href')
            driver.get(review_page_url)
            time.sleep(0.05)
            review_range = driver.find_element_by_xpath(review_number_xpath).text
            review_range = int(review_range.replace(',', '')) // 10 + 2
            print("------review-------")
            for k in range(1, review_range):  # 리뷰페이지
                driver.get(review_page_url + '&page={}'.format(k))
                time.sleep(0.05)
                for l in range(1, 11):  # 한페이지 최대 리뷰
                    review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
                    try:
                        driver.find_element_by_xpath(review_title_xpath).click()
                        time.sleep(0.05)
                        review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                        print(review[-20:])
                        titles.append(title)  # 에러났을때를 대비하여 append를 몰아둔다.
                        reviews.append(review)
                        print("===")
                        driver.back()
                    except:
                        print("{}페이지 {} 번째 review가 없습니다".format(k, l))
                        driver.get(url)
                        break
        except:
            print('error')
