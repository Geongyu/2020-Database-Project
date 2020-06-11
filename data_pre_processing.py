import numpy as np 
import pandas as pd
import os
import glob
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from datetime import datetime

# 파일을 하나로 합치기 위하여 

apple_music = []
bugs_music = []
genie_music = []
melon_music = []
vibe_music = [] 
youtube_music = [] 

for i in croll_folder :
    file = os.listdir(os.path.join(folder, i))
    apple_music.append(os.path.join(folder, i, file[0]))
    bugs_music.append(os.path.join(folder, i, file[1]))
    genie_music.append(os.path.join(folder, i, file[2]))
    melon_music.append(os.path.join(folder, i, file[3]))
    vibe_music.append(os.path.join(folder, i, file[4]))
    youtube_music.append(os.path.join(folder, i, file[5]))

bin_dataframe = pd.DataFrame(columns=["Rangking", "Title", "Artist", "Date", "Source Site"])
for apple, bugs, genie, melon, vibe, youtube in zip(apple_music, bugs_music, genie_music, melon_music, vibe_music, youtube_music) : 
    apple = pd.read_csv(apple)
    bugs = pd.read_csv(bugs)
    genie = pd.read_csv(genie)
    melon = pd.read_csv(melon)
    vibe = pd.read_csv(vibe)
    youtube = pd.read_csv(youtube)
    apple.loc[:,'Source Site'] = "Apple Music"
    bugs.loc[:,'Source Site'] = "Bugs Music"
    genie.loc[:,'Source Site'] = "Genie Music"
    melon.loc[:,'Source Site'] = "Melon Music"
    vibe.loc[:,'Source Site'] = "Naver Vibe"
    youtube.loc[:,'Source Site'] = "Youtube Music"
    bin_dataframe = bin_dataframe.append(apple)
    bin_dataframe = bin_dataframe.append(bugs)
    bin_dataframe = bin_dataframe.append(genie)
    bin_dataframe = bin_dataframe.append(melon)
    bin_dataframe = bin_dataframe.append(vibe)
    bin_dataframe = bin_dataframe.append(youtube)
bin_dataframe = bin_dataframe.reset_index(drop=True)

name = bin_dataframe.Artist

# 합친파일을 기준으로, 소속사를 크롤링한다

options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
site = "https://people.search.naver.com/"
driver.get(site)

agency =[]
find = 0 
for num, i in enumerate(name) :
    driver.get(site)
    driver.find_element_by_xpath('//*[@id="nx_query"]').send_keys(i.split("&")[0].split("(")[0])
    driver.find_element_by_xpath('//*[@id="search_form"]/fieldset/input').click()
    try :
        a = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[2]/div/div/div').text.split("\n")
        agency.append([i, a[a.index("소속")+1]])
    except :
        agency.append([i, "무소속"])
    finally :
        print("[{0}/{1}][{4}] {2}의 소속사는 {3} 입니다..".format(num, len(name), i, agency[-1][-1], len(agency)))

driver.close()

real_agency = []
for i in agency :
    real_agency.append(i[1])

bin_dataframe['agency'] = real_agency

def change_artist_name(bin_dataframe) :
    bin_dataframe.loc[bin_dataframe.Artist == "문별 (마마무)", "Artist"] = "문별"
    bin_dataframe.loc[bin_dataframe.Artist == "솔라 (마마무)", "Artist"] = "솔라"
    bin_dataframe.loc[bin_dataframe.Artist == "문별(마마무)", "Artist"] = "문별"
    bin_dataframe.loc[bin_dataframe.Artist == "VICTON(빅톤)", "Artist"] = "VICTON"
    bin_dataframe.loc[bin_dataframe.Artist == "VICTON (빅톤)", "Artist"] = "VICTON"
    bin_dataframe.loc[bin_dataframe.Artist == "Harry Styles(해리 스타일스)", "Artist"] = "Harry Styles"
    bin_dataframe.loc[bin_dataframe.Artist == "Lady GaGa(레이디 가가)", "Artist"] = "Lady GaGa"
    bin_dataframe.loc[bin_dataframe.Artist == "New Hope Club(뉴 호프 클럽)", "Artist"] = "New Hope Club"
    bin_dataframe.loc[bin_dataframe.Artist == "육성재 (비투비)", "Artist"] = "육성재"
    bin_dataframe.loc[bin_dataframe.Artist == "서은광 (비투비)", "Artist"] = "서은광"
    bin_dataframe.loc[bin_dataframe.Artist == "Idina Menzel(이디나 멘젤)", "Artist"] = "Idina Menzel"
    bin_dataframe.loc[bin_dataframe.Artist == "Dua Lipa(두아 리파)", "Artist"] = "Dua Lipa"
    bin_dataframe.loc[bin_dataframe.Artist == "두아 리파", "Artist"] = "Dua Lipa(두아 리파)"
    bin_dataframe.loc[bin_dataframe.Artist == "IZ*ONE (아이즈원)", "Artist"] = "아이즈원"
    bin_dataframe.loc[bin_dataframe.Artist == "IZ*ONE(아이즈원)", "Artist"] = "아이즈원"
    bin_dataframe.loc[bin_dataframe.Artist == "정용화(Jung Yong Hwa)", "Artist"] = "정용화"
    bin_dataframe.loc[bin_dataframe.Artist == "정용화 (CNBLUE)", "Artist"] = "정용화"
    bin_dataframe.loc[bin_dataframe.Artist == "정용화 (Jung Yong Hwa)", "Artist"] = "정용화"
    bin_dataframe.loc[bin_dataframe.Artist == "Maktub", "Artist"] = "마크툽"
    bin_dataframe.loc[bin_dataframe.Artist == "마크툽 (Maktub)", "Artist"] = "마크툽"
    bin_dataframe.loc[bin_dataframe.Artist == "마크툽(Maktub)", "Artist"] = "마크툽"
    bin_dataframe.loc[bin_dataframe.Artist == "마크툽 (MAKTUB)", "Artist"] = "마크툽"
    bin_dataframe.loc[bin_dataframe.Artist == "폴킴(Paul Kim)", "Artist"] = "폴킴"
    bin_dataframe.loc[bin_dataframe.Artist == "The Weeknd (위켄드)", "Artist"] = "The Weeknd"
    bin_dataframe.loc[bin_dataframe.Artist == "The Weeknd(위켄드)", "Artist"] = "The Weeknd"
    bin_dataframe.loc[bin_dataframe.Artist == "ITZY(있지)", "Artist"] = "ITZY"
    bin_dataframe.loc[bin_dataframe.Artist == "ITZY (있지)", "Artist"] = "ITZY"
    bin_dataframe.loc[bin_dataframe.Artist == "Ariana Grande(아리아나 그란데)", "Artist"] = "Ariana Grande"
    bin_dataframe.loc[bin_dataframe.Artist == "Ariana Grande (아리아나 그란데)", "Artist"] = "Ariana Grande"
    bin_dataframe.loc[bin_dataframe.Artist == "Sia(시아)", "Artist"] = "Sia"
    bin_dataframe.loc[bin_dataframe.Artist == "AKMU (악동뮤지션)", "Artist"] = "악동뮤지션"
    bin_dataframe.loc[bin_dataframe.Artist == "아이유(IU)", "Artist"] = "아이유"
    bin_dataframe.loc[bin_dataframe.Artist == "아이유 (IU)", "Artist"] = "아이유"
    bin_dataframe.loc[bin_dataframe.Artist == "TWICE (트와이스)", "Artist"] = "TWICE"
    bin_dataframe.loc[bin_dataframe.Artist == "TWICE(트와이스)", "Artist"] = "TWICE"
    bin_dataframe.loc[bin_dataframe.Artist == "휘인(Whee In)", "Artist"] = "휘인"
    bin_dataframe.loc[bin_dataframe.Artist == "휘인 (Whee In)", "Artist"] = "휘인"
    bin_dataframe.loc[bin_dataframe.Artist == "딘딘(DinDin)", "Artist"] = "딘딘"
    bin_dataframe.loc[bin_dataframe.Artist == "딘딘 (DinDin)", "Artist"] = "딘딘"
    bin_dataframe.loc[bin_dataframe.Artist == "오마이걸(OH MY GIRL)", "Artist"] = "오마이걸"
    bin_dataframe.loc[bin_dataframe.Artist == "오마이걸 (OH MY GIRL)", "Artist"] = "오마이걸"
    bin_dataframe.loc[bin_dataframe.Artist == "먼데이 키즈 (Monday Kiz)", "Artist"] = "먼데이키즈"
    bin_dataframe.loc[bin_dataframe.Artist == "먼데이키즈(Monday Kiz)", "Artist"] = "먼데이키즈"
    bin_dataframe.loc[bin_dataframe.Artist == "마마무 (Mamamoo)", "Artist"] = "마마무"
    bin_dataframe.loc[bin_dataframe.Artist == "마마무(Mamamoo)", "Artist"] = "마마무"
    bin_dataframe.loc[bin_dataframe.Artist == "김필(Kim Feel)", "Artist"] = "김필"
    bin_dataframe.loc[bin_dataframe.Artist == "김필 (Kim Feel)", "Artist"] = "김필"
    bin_dataframe.loc[bin_dataframe.Artist == "Red Velvet (레드벨벳)", "Artist"] = "레드벨벳"
    bin_dataframe.loc[bin_dataframe.Artist == "Red Velvet", "Artist"] = "레드벨벳"
    bin_dataframe.loc[bin_dataframe.Artist == "DAY6(데이식스)", "Artist"] = "데이식스"
    bin_dataframe.loc[bin_dataframe.Artist == "DAY6 (데이식스)", "Artist"] = "데이식스"
    bin_dataframe.loc[bin_dataframe.Artist == "마크툽(MAKTUB)", "Artist"] = "마크툽"
    bin_dataframe.loc[bin_dataframe.Artist == "Dua Lipa(두아 리파)", "Artist"] = "Dua Lipa"
    bin_dataframe.loc[bin_dataframe.Artist == "거미 (Gummy)", "Artist"] = "거미"
    bin_dataframe.loc[bin_dataframe.Artist == "태연 (TAEYEON)", "Artist"] = "태연"
    bin_dataframe.loc[bin_dataframe.Artist == "어반자카파 (URBAN ZAKAPA)", "Artist"] = "어반자카파"
    bin_dataframe.loc[bin_dataframe.Artist == "백현 (BAEKHYUN)", "Artist"] = "백현"
    bin_dataframe.loc[bin_dataframe.Artist == "백현(BAEKHYUN)", "Artist"] = "백현"
    bin_dataframe.loc[bin_dataframe.Artist == "HYNN (박혜원)", "Artist"] = "박혜원"
    bin_dataframe.loc[bin_dataframe.Artist == "박혜원(HYNN)", "Artist"] = "박혜원"
    bin_dataframe.loc[bin_dataframe.Artist == "HYNN(박혜원)", "Artist"] = "박혜원"
    bin_dataframe.loc[bin_dataframe.Artist == "Shawn Mendes(션 멘데스)", "Artist"] = "Shawn Mendes"
    bin_dataframe.loc[bin_dataframe.Artist == "Sam Smith(샘 스미스)", "Artist"] = "Sam Smith"
    bin_dataframe.loc[bin_dataframe.Artist == "Justin Bieber(저스틴 비버)", "Artist"] = "Justin Bieber"
    bin_dataframe.loc[bin_dataframe.Artist == "조이 (JOY)", "Artist"] = "조이"
    bin_dataframe.loc[bin_dataframe.Artist == "엠씨더맥스 (M.C the MAX)", "Artist"] = "엠씨더맥스"
    bin_dataframe.loc[bin_dataframe.Artist == "엠씨더맥스(M.C the MAX)", "Artist"] = "엠씨더맥스"
    bin_dataframe.loc[bin_dataframe.Artist == "비(RAIN)", "Artist"] = "비"
    bin_dataframe.loc[bin_dataframe.Artist == "RAIN", "Artist"] = "비"
    bin_dataframe.loc[bin_dataframe.Artist == "(여자) 아이들", "Artist"] = "(여자)아이들"
    bin_dataframe.loc[bin_dataframe.Artist == 'Apink (에이핑크)', "Artist"] = "에이핑크"
    bin_dataframe.loc[bin_dataframe.Artist == "창모(CHANGMO)", "Artist"] = "창모"
    bin_dataframe.loc[bin_dataframe.Artist == "창모 (CHANGMO)", "Artist"] = "창모"
    bin_dataframe.loc[bin_dataframe.Artist == "에이핑크(Apink)", "Artist"] = "에이핑크"
    bin_dataframe.loc[bin_dataframe.Artist == "에이프릴 (APRIL)", "Artist"] = "에이프릴"
    bin_dataframe.loc[bin_dataframe.Artist == "에이프릴(APRIL)", "Artist"] = "에이프릴"
    bin_dataframe.loc[bin_dataframe.Artist == "규현 (KYUHYUN)", "Artist"] = "규현"
    bin_dataframe.loc[bin_dataframe.Artist == "규현(KYUHYUN)", "Artist"] = "규현"
    bin_dataframe.loc[bin_dataframe.Artist == "Jo Jung-suk", "Artist"] = "조정석"
    bin_dataframe.loc[bin_dataframe.Artist == "코난 그레이", "Artist"] = "Conan Gray"
    bin_dataframe.loc[bin_dataframe.Artist == "마마무(MAMAMOO)", "Artist"] = "마마무"

    return bin_dataframe

bin_dataframe.to_csv("Final_Croll.csv")

