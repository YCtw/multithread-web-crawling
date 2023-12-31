from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import concurrent.futures
import pygsheets
import copy
import pandas as pd

TARGET = 300 #3000

#For post crawler
postCountOriginal = 1
pageOriginal = 1
postList = []

#For like crawler
postCountLike = 1
pageLike = 1
likeList = []

#For all post update
postUpdateListCount = [["Post"]]
postUpdateListText = [["內容"]]
postUpdateListLike = [["點讚數"]]

#For filter post update
postFilterListCount = [["Post"]]
postFilterListText = [["內容"]]
postFilterListLike = [["點讚數"]]

def connectedPage():
    CHROME_DRIVER = "C:/Users/yuhan/OneDrive/桌面/hundred_days_chrome_driver/chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--profile-directory=Default')
    options.add_argument("user-data-dir=C:/Users/yuhan/AppData/Local/Google/Chrome/User Data")
    s = Service(executable_path=CHROME_DRIVER)
    driver = webdriver.Chrome(service=s, options=options)
    driver.get("https://mbasic.facebook.com/groups/1786425331505061/?refid=18&_ft_=encrypted_tracking_data.0AY9AmE87qMe-B6Uz-nKi-LNOe1VtpFk2ZFGdXrs3-Dz3orvA1r5DslmJovJPgmU61DEQ2l_MX4MP7HLS3blEGF81fAoUkj5xXfFojbOq-CWx6_Q05MqpL8i57zroZgbRNkVoIWoZgYj0qLHEk_KDGF2nUMd4v1yWGvYdj_Fs3yWvp9PZCS-Cb5sOLfUIqybvdGk-pk35LZgV5VrFzFbWzU4fdGlqfW17bYWwwa_-UBmPvF6tzPMNxXyplOHZX_zMU7BLYQUzBSPU1cbsUXqPbw-7CyvohusVEjAY5kzphNkPYPnjmIIHeocp_1mdJe7m1xcAmU_2K5dRLXTa2obd0F3pMYtAodHcefwE4HDLI73kbKJN3DY89GqCU6CR9NilDMuP1houb-pbZkNDafHY6R4BjJlm6bftIHOdPKNEK951Exn3Ftvnq5lPuv-qFZr4XXBgqqHMCBJySnWczRDk-Sqg0JcgGliHGIhk77EShi7yRSItkiNd8EpwejqC0E42bTILPyqY0yFsDIapPqWLo1rx84DDfmBzO6thq1xxYpwvLKPD56sFcflUOG1LadM6buZEakDeNE6mE5oFYA8XhOH5l01Gvhcs9JEXjWcSAsaTJccUjTbAzy0GeeR5u4a6jumtg9kEShmBGO8cQO8yNMpgXl7MdKiZWCbiA1M7RmEQzIlH4_8eW1CZ8-Abs1DB5BpSximz4fh-ofSine-60vl2oeAL0jurlvt-N-VBeCGBlqdcALxPaXhF1FDrGcbFq0swKC2WkT4Qv7cz0ZMpD1_FLorUTb3EyabAaIL3GjU1ZSG5yx35aeNpuyC3g8YBKkb-xIULh9xuBuYjaqZM1N_BxxMGB9QZU0VV-NWnSc3aLMw0hNonsFQaebeux2bbA3A0BKEouhRHPpnRTcrKHCWAr-gzPFIiGUCXz94VPeyavWY0C1nt1bSiwRDbEyrqjObVsgrKI5QT7Y26eLUouNehPYAD7syu2Pdpbbt0uHrPToNF_GPJhjBOSPUxJ0XpObBor87KaQfg7FEUzuApHw45VGfJV71qdzCpOX9CdzaUYSfDzMUuUtQXbTQZEC-nZ93Jnc_apJQiGPCbk5pN4ctbDf_Ob31AUkmkd9oUY9ERX90fveBNOqeAlp01JU9tVZTzc7P-88p1XIKsNw&__tn__=C-R&paipv=0&eav=Afa4RpEdqax4kua-Y6CZo5S9xsFjipgOFaxWzoe0-hZlwuydsr-DA3lsN_ZnE2uFffI")
    return driver

def nextPage(driver):
    try:
        nextPage = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[2]/div/div[1]/div[5]/div[2]")
    except:
        nextPage = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[2]/div/div[1]/div[4]/div")
    nextPage.click()

#n = target post
def postCrawler(n):
    global postCountOriginal
    global pageOriginal
    driver = connectedPage()
    time.sleep(2)

    while True:

        time.sleep(2)
        posts = driver.find_elements(by=By.CLASS_NAME, value="ds") #每頁8個貼文

        if pageOriginal > 1:
            posts = posts[1:] #第一篇公告不用爬了

        #設定完後開始爬內容
        for post in posts:
            # print(f"__________________________{postCountOriginal}篇貼文__________________________")
            try: #有一些post沒有內文
                text = post.find_element(by=By.TAG_NAME, value="span").text
                postList.append(text)
                # print(text)
            except:
                postList.append("")
                pass
            postCountOriginal += 1

            if postCountOriginal > n:  # 爬到目標文章數
                return

        #換頁
        time.sleep(2)
        pageOriginal += 1
        nextPage(driver)

#n = target post
def likeCrawler(n): #蒐集前幾篇的like
    global postCountLike
    global pageLike
    driver = connectedPage()
    time.sleep(2)

    while True:
        time.sleep(2)

        if pageLike == 1:
            firstPostLikes = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[2]/div/div[1]/div[3]/section/section/article/footer/div[2]/span[1]/a[1]")
            likeList.append(firstPostLikes.text)
            postCountLike += 1

            # 第一篇公告不用爬了

        for a in range(1, 8):
            otherPostLikes = driver.find_element(by=By.XPATH, value=f"/html/body/div/div/div[2]/div/div[1]/div[4]/section/article[{a}]/footer/div[2]/span[1]/a[1]")
            likeList.append(otherPostLikes.text)
            postCountLike += 1

            if postCountLike > n:  # 爬到目標文章數的like
                return

        # 換頁
        time.sleep(2)
        pageLike += 1
        nextPage(driver)

def postFilter(keyword, likes):
    postCopy = copy.deepcopy(postList)
    likeCopy = copy.deepcopy(likeList)
    convertLikeCopy = []
    for like in likeCopy:
        try:
            convertLikeCopy.append(int(like))
        except:
            likeSplit = like.split(',')
            convertLikeCopy.append(1000 * int(likeSplit[0]) + int(likeSplit[1]))

    likeDictionary = {
        "內容": postCopy,
        "點讚數": convertLikeCopy
    }
    df = pd.DataFrame(likeDictionary)

    postFilterResult = df.loc[(df["點讚數"] >= likes) & df["內容"].str.contains(keyword)]["內容"].tolist()
    postLikeResult = df.loc[(df["點讚數"] >= likes) & df["內容"].str.contains(keyword)]["點讚數"].tolist()

    return postFilterResult, postLikeResult


#Multithread to do the crawling - 1 for content for the post, 1 for likes for the post
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    thread1 = executor.submit(postCrawler, TARGET)
    thread2 = executor.submit(likeCrawler, TARGET)

    # Wait for both functions to complete
    concurrent.futures.wait([thread1, thread2])


#Update to all first
gc = pygsheets.authorize(service_file='keys.json')
postUpdateListCount = postUpdateListCount + [[f"貼文{count}"] for count in range(1,TARGET+1)]
postUpdateListText = postUpdateListText + [[text] for text in postList]
postUpdateListLike = postUpdateListLike + [[like] for like in likeList]

sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/11Wz_ezGESLnQIygWN6aAyqog9UgUSk2JJwxbQDWpk0w/edit#gid=621577692')
allSheet = sht.worksheet_by_title("all")
allSheet.update_values('A1:', postUpdateListCount)
allSheet.update_values('B1', postUpdateListText)
allSheet.update_values('C1', postUpdateListLike)


#過濾貼文，Update to filter first
filterListText, filterListLike = postFilter("生魚片",100)
postFilterListCount = postFilterListCount + [[f"貼文{count}"] for count in range(1,len(filterListText)+1)]
postFilterListText = postFilterListText + [[text] for text in filterListText]
postFilterListLike = postFilterListLike + [[like] for like in filterListLike]

sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/11Wz_ezGESLnQIygWN6aAyqog9UgUSk2JJwxbQDWpk0w/edit#gid=621577692')
filterSheet = sht.worksheet_by_title("filter")
filterSheet.update_values('A1:', postFilterListCount)
filterSheet.update_values('B1', postFilterListText)
filterSheet.update_values('C1', postFilterListLike)
