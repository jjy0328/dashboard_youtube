from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

import time
import random
import pandas as pd

# 랜덤한 User-Agent 생성
ua = UserAgent().random
options = webdriver.ChromeOptions()

# User-Agent 설정
options.add_argument("--disable-cache") # 캐시 사용안함
options.add_argument("--incognito") # 시크릿 모드
options.add_argument("disable-gpu") # 가속 사용 x
options.add_argument(f'user-agent={ua}') # UA 설정
options.add_experimental_option('excludeSwitches', ['enable-logging']) # 로그 숨기기
options.add_experimental_option("excludeSwitches", ["enable-automation"]) # 자동화 테스트를 위한 옵션 해제 : 크롬이 소프트웨어에 의해 제어되고있다는 메세지 비활성화
options.add_experimental_option("useAutomationExtension", False) # 자동화 테스트를 위한 옵션 해제 : 브라우저 세션을 더 자연스럽게 보이게 함

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
# 유튜브 접속
driver.get("https://www.youtube.com/")

# 랜덤한 시간을 지정해서 휴식
sleep_time = random.uniform(1, 2) # 페이지 로딩을 위한 time.sleep() 시간 설정
waiting_time = random.uniform(300, 600) # 동영상 및 광고 시청을 위한 time.sleep() 시간 설정 
typing_time = random.uniform(0.3, 0.5) # 검색어 입력을 위한 time.sleep() 시간 설정

# 기본 정보 수집
def extract_web_elements():
    # 요소 찾기
    title_element = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string')
    user_element = driver.find_element(By.XPATH, '//*[@id="text"]/a')
    expended_element = driver.find_element(By.XPATH, '//*[@id="expand"]')
    content_element = driver.find_element(By.XPATH, '//*[@id="description-inline-expander"]/yt-attributed-string/span/span[1]')
    keyword_elements = driver.find_elements(By.XPATH, '//*[@id="info"]/a')

    # 추출된 요소들의 텍스트 가져오기
    title = title_element.text
    user = user_element.text
    expended = expended_element.text
    content = content_element.text
    keywords = [keyword_element.text for keyword_element in keyword_elements]

    return {
        "title": title,
        "user": user,
        "expended": expended,
        "content": content,
        "keywords": keywords
    }

# 광고 정보 수집
def extract_ad_titles():
    waiting_time = random.uniform(300, 600)  # Random waiting time between 300 to 600 seconds
    start_time = time.time()
    ad_titles = []

    while time.time() - start_time < waiting_time:
        try:
            
            ad_title_element = driver.find_element(By.XPATH, '//div[@class="ytp-ad-text ytp-flyout-cta-headline"]')
            ad_title = ad_title_element.text

            if ad_title and ad_title not in ad_titles:
                ad_titles.append(ad_title)
                print(ad_title)

        except NoSuchElementException:
            time.sleep(3)
            continue

        except StaleElementReferenceException:
            break
        time.sleep(5)

    return ad_titles


# 검색어 입력 : 서치 박스 클릭
search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[2]/ytd-searchbox')))
search_box.click()

# # 만약 검색어가 입력되어 있다면 지워주기
try:
    delete_btn = driver.find_element(By.XPATH, '//*[@id="search-clear-button"]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
    time.sleep(sleep_time)
    delete_btn.click()
except Exception as e:
    pass 

# 검색어 입력 : 검색어 입력
text_to_type = "드라마 요약"

# 한 글자씩 입력하면서 각 글자 사이에 지연 주기 -> 일정한 시간을 줄 경우, 봇으로 탐지할 가능성이 높음
for char in text_to_type:
    search_box.send_keys(char)
    time.sleep(typing_time)  # 지연 시간은 필요에 따라 조정 가능
search_box.send_keys(Keys.ENTER)

time.sleep(sleep_time)
# 랜덤하게 하나의 동영상 재생
title_to_click = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
for _ in range(len(title_to_click)):
    random_index = random.randint(0, len(title_to_click) - 1)
    if title_to_click[random_index].is_displayed() and title_to_click[random_index].is_enabled():
        title_to_click[random_index].click()

        # 광고 정보 먼저 수집
        ad_info = extract_ad_titles()
        print(f"광고 제목 : {ad_info}")

        # 동영상 정보 수집
        data = extract_web_elements()
        print(f"영상 정보 : {data}")


# 브라우저 닫기
driver.quit()