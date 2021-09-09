# 25개구 for문으로 돌려서 카페 정보 크롤링하기

import os
from time import sleep
import time
import re
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

##########################################################################
##################### variable related selenium ##########################
##########################################################################
# 서울 특별시 구 리스트
dong_list = ['창곡동','산성동','단대동','신흥동','복정동','태평동','수진동',
           '신촌동','오야동','심곡동','둔전동','고등동','시흥동','사송동','상적동',
           '금토동','은행동','금광동','상대원동','갈현동','중동','성남동','하대원동','여수동'
           ,'도촌동','야탑동','이매동','율동','서현동','분당동','수내동','정자동','구미동'
           ,'동원동','금곡동','궁내동','백현동','판교동','삼평동','하산운동','운중동','석운동']

  
    
# csv 파일에 헤더 만들어 주기
for index, gu_name in enumerate(dong_list):
    
    fileName = dong_list[index]+'.csv' # index.__str__() + '_' + gu_name + '.'+'csv'
    file = open(fileName, 'w', encoding='utf-8-sig', newline="")
    wr = csv.writer(file)
    wr.writerow(["상호명", "품목", '동', "구", "주소", "전화번호", "비고"])
    #file.write("카페명" + "|" + "주소" + "|" + "영업시간" + "|" + "전화번호" + "|" + "대표사진주소" + "\n")
    file.close()  

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome("./chromedriver",options=options)  # chromedriver 열기
    
    driver.get('https://map.kakao.com/')  # 주소 가져오기
    driver.implicitly_wait(5)
    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]') # 검색 창
    search_area.send_keys(gu_name + ' 음식점')  # 검색어 입력
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
    driver.implicitly_wait(3) # 기다려 주자

    more_page = driver.find_element_by_id("info.search.place.more")

    try :
        more_page.click()
    except :
        print("클릭 안됨")
        
    more_page.send_keys(Keys.ENTER) # 더보기 누르고
    # 첫 번째 검색 페이지 끝
    # driver.implicitly_wait(5) # 기다려 주자
    time.sleep(1)

    # fastenLocation = driver.find_element_by_css_selector("#info\.searchHeader\.message > div > div.line.lower > a")

    # try :
    #     fastenLocation.click()
    # except :
    #     print("클릭 안됨")
        
    # fastenLocation.send_keys(Keys.ENTER)

    # time.sleep(1)

    # next 사용 가능?
    next_btn = driver.find_element_by_id("info.search.page.next")
    has_next = "disabled" not in next_btn.get_attribute("class").split(" ")
    Page = 1
    print("?????????")
    time.sleep(3)
    while has_next: # 다음 페이지가 있으면 loop
    # for i in range(2, 6): # 2, 3, 4, 5
        time.sleep(1)
        # place_lists = driver.find_elements_by_css_selector('#info\.search\.place\.list > li:nth-child(1)')
        # 페이지 루프
        #info\.search\.page\.no1 ~ .no5
        page_links = driver.find_elements_by_css_selector("#info\.search\.page a")
        pages = [link for link in page_links if "HIDDEN" not in link.get_attribute("class").split(" ")]
        print(len(pages), "개의 페이지 있음")
        # pages를 하나씩 클릭하면서
        for i in range(1, len(pages)):
            xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
            try:
                page = driver.find_element_by_xpath(xPath)
                page.send_keys(Keys.ENTER)
            except ElementNotInteractableException:
                print('End of Page')
                break;
            sleep(3)
            place_lists = driver.find_elements_by_css_selector('#info\.search\.place\.list > li')
            for p in place_lists: # WebElement
                # print(p.get_attribute('innerHTML'))
                # print("type of p:", type(p))
                #print("???????")
                store_html = p.get_attribute('innerHTML')
                store_info = BeautifulSoup(store_html, "html.parser")
                # BS -> 분석
                #
                place_name = store_info.select('.head_item > .tit_name > a.link_name')
                #print(place_name)
                # place_address = store_info.select('.info_item > .addr > p')
                # place_hour = store_info.select('.info_item > .openhour > p > a')
                # place_tel = store_info.select('.info_item > .contact > span')
                 # print("length:", len(place_name))
                if len(place_name) == 0:
                    continue # 광고

                place_name = store_info.select('.head_item > .tit_name > .link_name')[0].text
                place_address = store_info.select('.info_item > .addr > p')[0].text
                place_tel = store_info.select('.info_item > .contact > span')[0].text
                place_condition = store_info.select('.head_item > .subcategory')[0].text
                place_other_addr = store_info.select('.info_item > .addr > p')[1].text

                addresslist = place_address.split(' ')

                if("경기" in addresslist[0]) :
                    place_detail_address1 = addresslist[2]
                else :
                    place_detail_address1 = addresslist[1]

                place_page = store_info.select('.info_item > .contact > a')[1].get_attribute_list('href')[0]
                print("page : "+place_page, "other page : ", place_other_addr)
                
                if(place_page == "#none") :
                    place_page = store_info.select('.info_item > .contact > a')[0].get_attribute_list('href')[0]
                
                print(place_name, " : ",place_address)

                dongList_split = ""
                if(len(dong_list[index])==2) :
                    dongList_split = dong_list[index][:1]

                if(len(dong_list[index])==3):
                    dongList_split = dong_list[index][:2]
                
                if(len(dong_list[index])==4):
                    dongList_split = dong_list[index][:3]
                
                if("경기 성남시" in place_address) :

                    if(place_other_addr == "") :
                        if((dongList_split in place_address) or (dongList_split in place_other_addr)) :
                            print("삽입값 : ", place_address, "  ", place_other_addr)
                            file = open(fileName, 'a', encoding='utf-8-sig', newline="")
                            wr = csv.writer(file)
                            wr.writerow([place_name, place_condition, dong_list[index], place_detail_address1, place_address, place_tel, place_page])
                            file.close()
                        
                    if(place_other_addr != "") :
                        if(dongList_split in place_other_addr) :
                            print("삽입값 : ", place_address, "  ", place_other_addr)
                            file = open(fileName, 'a', encoding='utf-8-sig', newline="")
                            wr = csv.writer(file)
                            wr.writerow([place_name, place_condition, dong_list[index], place_detail_address1, place_address, place_tel, place_page])
                            file.close()
                        
            print(i, ' of', ' [ ' , Page, ' ] ')
        next_btn = driver.find_element_by_id("info.search.page.next")
        has_next = "disabled" not in next_btn.get_attribute("class").split(" ")
        if not has_next:
            print('Arrow is Disabled')
            driver.close()
            file.close()
            break # 다음 페이지 없으니까 종료
        else: # 다음 페이지 있으면
            Page += 1
            next_btn.send_keys(Keys.ENTER)
    print("End of Crawl")