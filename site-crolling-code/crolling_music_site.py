import numpy as np
import pandas as pd
import os
import glob
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from datetime import datetime

url_path = [
    'https://www.genie.co.kr/chart/top200',
    'https://www.melon.com/chart/day/index.htm',
    'https://www.melon.com/chart/day/index.htm#params%5Bidx%5D=51',
    'https://music.bugs.co.kr/chart/track/day/total',
    'https://vibe.naver.com/chart/total',
    'https://charts.youtube.com/charts/TopSongs/kr?hl=ko',
    'https://music.apple.com/kr/playlist/%EC%98%A4%EB%8A%98%EC%9D%98-top-100-%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD/pl.d3d10c32fbc540b38e266367dc8cb00c'
] # 목표로 하는 URL 주소들 지니뮤직, 멜론뮤직, 벅스뮤직, 네이버 바이브, 유튜브 뮤직, 애플뮤직을 크롤링

site_name = [
    '지니뮤직',
    '멜론뮤직(1-50)',
    '멜론뮤직(51-100)',
    '벅스뮤직',
    '네이버바이브',
    '유튜브뮤직',
    '애플뮤직'
]

options = Options()
options.headless = True
browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=options) # Chrome Base로 Selenium을 사용한다. 이때 실제 인터넷창이 뜨지 않는 Headless Browser로 사용한다

def genie_music_crolling(driver) :
    '''
    지니뮤직 크롤링용 코드
    인자로 받아오는것은 외부에서 선언엔 셀레늄 드라이버를 가져온다.
    '''
    genie_ranking = [] # 지니뮤직에서 크롤링하여 가져올 랭킹들을 저장할 리스트 
    month = datetime.today().month # 크롤링하는 날짜가 몇월인지 확인하기 위하여
    day = datetime.today().day # 크롤링하는 날짜가 몇일인지를 확인하기 위하여 
    today = "{0}-{1}".format(month, day)
    driver.find_element_by_xpath('//*[@id="body-content"]/div[3]/ul/li[2]/a').click() # 지니뮤직의 경우 최초에 일간 종합순위로 이동을 시켜야한다 
    for i in range(1, 51) : # 최초 1위부터 50위까지를 가져온다. 
        ranking = driver.find_element_by_xpath('//*[@id="body-content"]/div[4]/div/table/tbody/tr[{0}]/td[2]'.format(i)).text # 지니뮤직 랭킹순위를 가져온다 몇위가 올랐는지 몇위가 떨어졌는지 확인 할 수 있다.
        title = driver.find_element_by_xpath('//*[@id="body-content"]/div[4]/div/table/tbody/tr[{0}]/td[5]/a[1]'.format(i)).text # 곡명을 가져온다
        artist_name = driver.find_element_by_xpath('//*[@id="body-content"]/div[4]/div/table/tbody/tr[{0}]/td[5]/a[2]'.format(i)).text # 가수명을 가져온다 
        album_name = driver.find_element_by_xpath('//*[@id="body-content"]/div[4]/div/table/tbody/tr[{0}]/td[5]/a[3]'.format(i)).text # 앨범명을 가져온다
        genie_ranking.append([i, title, artist_name, today]) # 몇번째로 가져왔는지를 확인하고 타이틀, 가수명, 날짜와 함께 저장한다 앨범은 저장하지 않는다 
    driver.find_element_by_xpath('//*[@id="body-content"]/div[5]/a[2]').click() # 지니뮤직의 경우 1~50위 51~100위가 나뉘어져 있기 때문에 나머지 51~100위를 확인한다.
    for i in range(1, 51) : # 51~100 위를 가져온다 
        ranking = driver.find_element_by_xpath('//*[@id="body-content"]/div[4]/div/table/tbody/tr[{0}]/td[2]'.format(i)).text
        title = driver.find_element_by_xpath('//*[@id="body-content"]/div[4]/div/table/tbody/tr[{0}]/td[5]/a[1]'.format(i)).text
        artist_name = driver.find_element_by_xpath('//*[@id="body-content"]/div[4]/div/table/tbody/tr[{0}]/td[5]/a[2]'.format(i)).text
        album_name = driver.find_element_by_xpath('//*[@id="body-content"]/div[4]/div/table/tbody/tr[{0}]/td[5]/a[3]'.format(i)).text
        genie_ranking.append([i+50, title, artist_name, today]) # 상동, i에 50을 더하여 추후 순위들을 반영시킨다 

    return genie_ranking

def melon_music_crolling_1_to_50(driver):
    # 멜론뮤직의 경우 1위부터 50위까지가 한페이지, 51~100이 URL 단으로 나뉘어져 있다 
    melon_music_ranking = []
    month = datetime.today().month
    day = datetime.today().day
    today = "{0}-{1}".format(month, day)
    for i in range(1, 51):
        ranking = str(i)
        title = driver.find_element_by_xpath(
            '//*[@id="frm"]/div/table/tbody/tr[{0}]/td[6]/div/div/div[1]/span/a'.format(i)).text
        artist_name = driver.find_element_by_xpath(
            '//*[@id="frm"]/div/table/tbody/tr[{0}]/td[6]/div/div/div[2]/a'.format(i)).text
        melon_music_ranking.append([ranking, title, artist_name, today])
    return melon_music_ranking


def melon_music_crolling_51_to_100(driver):
    melon_music_ranking = []
    month = datetime.today().month
    day = datetime.today().day
    today = "{0}-{1}".format(month, day)
    for i in range(51, 101):
        ranking = str(i)
        title = driver.find_element_by_xpath(
            '//*[@id="frm"]/div/table/tbody/tr[{0}]/td[6]/div/div/div[1]/span/a'.format(i)).text
        artist_name = driver.find_element_by_xpath(
            '//*[@id="frm"]/div/table/tbody/tr[{0}]/td[6]/div/div/div[2]/a'.format(i)).text
        melon_music_ranking.append([ranking, title, artist_name, today])
    return melon_music_ranking

def bugs_music_crolling(driver) :
    bugs_ranking = []
    month = datetime.today().month
    day = datetime.today().day
    today = "{0}-{1}".format(month, day)
    for i in range(1, 101) :
        ranking = driver.find_element_by_xpath('//*[@id="CHARTday"]/table/tbody/tr[{0}]/td[2]/div/strong'.format(i)).text
        title = driver.find_element_by_xpath('//*[@id="CHARTday"]/table/tbody/tr[{0}]/th/p/a'.format(i)).text
        artist_name = driver.find_element_by_xpath('//*[@id="CHARTday"]/table/tbody/tr[{0}]/td[5]/p/a'.format(i)).text
        album_name = driver.find_element_by_xpath('//*[@id="CHARTday"]/table/tbody/tr[{0}]/td[6]/a'.format(i)).text
        bugs_ranking.append([ranking, title, artist_name, today])


    return bugs_ranking

def naver_music_crolling(driver) :
    naver_music_ranking = []
    month = datetime.today().month
    day = datetime.today().day
    today = "{0}-{1}".format(month, day)
    driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/a/i').click() # 네이버 뮤직의 경우 일간 종합차트를 들어갈경우 광고팝업이 생성되는데, 해당 팝업을 종료시킨다 
    for i in range(1, 101) :
        title = driver.find_element_by_xpath('//*[@id="content"]/div[5]/div[1]/div/table/tbody/tr[{0}]/td[4]/div[1]/span/a'.format(i)).text
        ranking = driver.find_element_by_xpath('//*[@id="content"]/div[5]/div[1]/div/table/tbody/tr[{0}]/td[3]/span'.format(i)).text
        artist_name = driver.find_element_by_xpath('//*[@id="content"]/div[5]/div[1]/div/table/tbody/tr[{0}]/td[5]/span/span/span/a'.format(i)).text
        album_name = driver.find_element_by_xpath('//*[@id="content"]/div[5]/div[1]/div/table/tbody/tr[{0}]/td[6]/a'.format(i)).text
        naver_music_ranking.append([ranking, title, artist_name, today])
    return naver_music_ranking

def youtube_music_crolling(driver) :
    youtube_music_ranking = []
    month = datetime.today().month
    day = datetime.today().day
    today = "{0}-{1}".format(month, day)
    import time
    time.sleep(5) # 유튜브 뮤직의 경우 최초 접속시 충분한 시간이 지난후에 Script 문이 Loading된다. 
    for i in range(1, 101) :
        title = driver.find_element_by_xpath('//*[@id="{0}"]/div[3]/div[1]/ytmc-ellipsis-text/div/span'.format(i)).text
        ranking = str(i)
        artist_name = driver.find_element_by_xpath('//*[@id="{0}"]/div[3]/div[2]/ytmc-ellipsis-text/div/span'.format(i)).text
        youtube_music_ranking.append([ranking, title, artist_name, today])
    return youtube_music_ranking

def apple_music_crolling(driver) :
    apple_music_ranking = []
    month = datetime.today().month
    day = datetime.today().day
    today = "{0}-{1}".format(month, day)
    import time
    time.sleep(5) # 애플 뮤직의 경우 최초 접속시 충분한 시간이 지난후에 Script 문이 Loading 된다
    for i in range(3, 103) : # 애플뮤직의 최초 2개 컬럼의 경우에는 베스트 탑 100 곡이 아닌 추천곡이 출력된다. 
        title, artist = driver.find_element_by_xpath('//*[@id="ember14"]/div/div[1]/div[2]/div[2]/div[{0}]/div[2]'.format(i)).text.split("\n")
        album_name = driver.find_element_by_xpath('//*[@id="ember14"]/div/div[1]/div[2]/div[2]/div[{0}]/div[3]'.format(i)).text
        apple_music_ranking.append([i-2, title, artist, today])
    return apple_music_ranking

for url, name in tqdm(zip(url_path, site_name)) :
    browser.get(url)
    if name == '지니뮤직' :
        genie_ranking = genie_music_crolling(browser)
    elif name == '멜론뮤직(1-50)':
        melon_ranking_1_to_50 = melon_music_crolling_1_to_50(browser)
    elif name == '멜론뮤직(51-100)':
        melon_ranking_51_to_100 = melon_music_crolling_51_to_100(browser)
    elif name == '벅스뮤직' :
        bugs_ranking = bugs_music_crolling(browser)
    elif name == '네이버바이브' :
        naver_ranking = naver_music_crolling(browser)
    elif name == '유튜브뮤직' :
        youtube_ranking = youtube_music_crolling(browser)
    elif name == "애플뮤직" :
        apple_ranking = apple_music_crolling(browser)

genie = pd.DataFrame(genie_ranking, columns=["Rangking", "Title", "Artist", "Date"]) # 각각의 컬럼이름을 명명한후 판다스 데이터 프레임 형태로 저장한다 
melon = pd.DataFrame(melon_ranking_1_to_50 + melon_ranking_51_to_100, columns=["Rangking", "Title", "Artist", "Date"])
bugs = pd.DataFrame(bugs_ranking, columns=["Rangking", "Title", "Artist", "Date"])
vibe = pd.DataFrame(naver_ranking, columns=["Rangking", "Title", "Artist", "Date"])
youtube = pd.DataFrame(youtube_ranking, columns=["Rangking", "Title", "Artist", "Date"])
apple = pd.DataFrame(apple_ranking, columns=["Rangking", "Title", "Artist", "Date"])

work_dir = "./music_crolling" # 음원순위 크롤링 파일을 저장할 위치를 지정한다 
if not os.path.exists(work_dir):
    os.makedirs(work_dir) # 해당 폴더가 존재하지 않을경우 해당 이름으로 된 폴더를 만들어 낸다

month = datetime.today().month
day = datetime.today().day

genie.to_csv(work_dir + "/genie-{0}-{1}.csv".format(month, day), index=False)
melon.to_csv(work_dir + "/melon-{0}-{1}.csv".format(month, day), index=False)
bugs.to_csv(work_dir + "/bugs-{0}-{1}.csv".format(month, day), index=False)
vibe.to_csv(work_dir + "/vibe-{0}-{1}.csv".format(month, day), index=False)
youtube.to_csv(work_dir + "/youtube-{0}-{1}.csv".format(month, day), index=False)
apple.to_csv(work_dir + "/apple-{0}-{1}.csv".format(month, day), index=False)
# 파일을 저장할 때 추출된 음원 사이트 + 월, 일 로 저장을 한다 

browser.close()
# 메모리 반환을 위한 헤드리스 브라우져를 종료시킨다
