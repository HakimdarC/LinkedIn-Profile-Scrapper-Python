from selenium import webdriver
from parameters import param
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import shutil
import csv

driver = webdriver.Chrome(r'C:\chromedriver_win32\chromedriver.exe')
def login_search():
    driver.get('https://www.linkedin.com/login')
    driver.maximize_window()

    email=driver.find_element_by_xpath('//*[@id="username"]')
    email.send_keys(param.linked_username)
    time.sleep(3)
    password=driver.find_element_by_xpath('//*[@id="password"]')
    password.send_keys(param.linked_password)
    time.sleep(3)
    login=driver.find_element_by_class_name('login__form_action_container')
    login.click()
    time.sleep(3)
    driver.get("https://www.google.com")
    driver.maximize_window() 
    time.sleep(5)
    search = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    search.send_keys(param.search_query)
    recherche_google = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]')
    recherche_google.click()
    time.sleep(10)
    #recherche_google.send_keys(Keys.RETURN)

    return driver

#login_search()

def get_page_links(driver):
    soup = BeautifulSoup(driver.page_source,features="html5lib")
    page_list = []
    tr = soup.find('tr')
    for td in tr.find_all('td'):
        for a in td.find_all('a'):
            print("https://www.google.com"+a['href'])
            page_list.append("https://www.google.com"+a['href'])
    return page_list
#get_page_links(search_g())


def get_detail_links(page_list):
    l=page_list
    for link in range(len(l)-7):
        driver.get(page_list[link])
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source,features="html5lib")
        link_list = []
        div=soup.find('div',id='search')
        for a in div.find_all('a'):
            if a['href'].startswith('https://uk.linkedin.com'):
                print(a['href'])
                link_list.append(a['href'])
    return link_list

#get_detail_links(get_page_links(search_g()))

def get_profile_infos(link_list):
    l=link_list
    for link in l:
        driver.get(link)
        soup = BeautifulSoup(driver.page_source,features="html5lib")
        elem = soup.find('div',class_='flex-1 mr5')
        h2_profile = elem.find('h2').get_text().strip()
        ul_name = elem.find_all('ul')[0].find('li').get_text().strip()
        ul_loc = elem.find_all('ul')[1].find('li').get_text().strip()
        ul_connections = elem.find_all('ul')[1].find_all('li')[1].get_text().strip()
        div=soup.find_all('div',class_="pv-top-card__photo-wrapper ml0")
        img_url = div[0].find('img')['src']
        print(h2_profile)
        print(ul_name)
        print(ul_loc)
        print(ul_connections)
        print(img_url)
        data_l = [[]]
        data_l.append([h2_profile,ul_name,ul_loc,ul_connections,img_url])


        writer_obj = csv.writer(open(param.file_name,'w'))
        list_fields = ['Job Title','Name','Location','Number_Connections','img_link']
        writer_obj.writerow(list_fields)
        for obj in data_l:
            writer_obj.writerows(obj)
    return writer_obj

#get_profile_infos()

def get_pro_image(list_img_url):
    for src in list_img_url:
        resp = requests.get(src,stream='True')
        file = open('local_file.jpg', 'wb')
        resp.raw.decode_content = True
        shutil.copyfileobj(resp,file)
        del resp
        print('image download done!!')
   
get_profile_infos(get_detail_links(get_page_links(login_search())))
