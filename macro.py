# -*- coding: utf-8 -*-
import sys
import time
import warnings
import codecs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
print("Content-type: text/html;charset=utf-8\r\n")

# 기본 사용자 세팅 (모두 입력하세요)
userId = ""  # 에브리타임 아이디 입력
userPw = ""  # 에브리타임 비밀번호 입력
targetBoard = ""  # 대상 게시판 번호 (에브리타임 URL에서 얻을 수 있음)

# =========================================== #

# 메인 코드

warnings.filterwarnings("ignore")
now = datetime.now()
url = "https://everytime.kr/" + str(targetBoard)
# headless part code from :
# https://beomi.github.io/2017/09/28/HowToMakeWebCrawler-Headless-Chrome/

while True:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    count = 1
    driver = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)

    driver.get("https://everytime.kr/login")

    # 로그인
    driver.find_element_by_name('userid').send_keys(userId)
    driver.find_element_by_name('password').send_keys(userPw)
    driver.find_element_by_name('password').send_keys(Keys.RETURN)
    time.sleep(1)

    # 자유게시판
    while True:
        try:
            driver.get(url)
            time.sleep(0.5)
            driver.find_element_by_class_name('vote').click()
            time.sleep(0.5)
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(1)

            try:
                msg = alert.text
                if msg == "이미 공감하였습니다.":
                    alert.accept()
                    print("시도횟수 : " + str(count) + " / Msg : 이미 공감한 게시물")
                time.sleep(1.8)
            except:
                print("시도횟수 : " + str(count) + " / Msg : 공감을 눌렀습니다.")
                time.sleep(2)
            finally:
                if count >= 500:
                    print(now)
                    print("===========프로세스 유지를 위해 새로고침합니다============")
                    driver.quit()
                    break
                count += 1
        except:
            print(now)
            driver.quit()
            break
