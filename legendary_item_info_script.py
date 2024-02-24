from bs4 import BeautifulSoup
# import requests
# import PIL.Image
# import urllib3
import pandas as pd
from requests_html import HTMLSession
import time 
from selenium import webdriver
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os 
import asyncio
# from pyppeteer import launch
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import json
import csv

def grab_html(url):
    # Define the Chrome webdriver options
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--allow-insecure-localhost")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    options.add_argument('ignore-certificate-errors')
    options.add_argument('ignore-ssl-errors')
    options.add_argument('ignore-certificate-errors-spki-list')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('log-level=3') # Silences all but fatal errors - added to silence ssl and handshake errors
    options.page_load_strategy = "none" # By default, Selenium waits for all resources to download before taking actions. However, we don't need it as the page is populated with dynamically generated JavaScript code.
    driver = webdriver.Chrome(options=options) # Pass the defined options objects to initialize the web driver
    # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
    # driver.implicitly_wait(5)
    
    
    return driver 

def main():
  
    chrome_driver_path = "C:\Program Files (x86)\chromedriver.exe"
    ## WEB SCRAPING ##
    current_db = "relics" # "weapons" "shields" "grenade-mods" "class-mods" "relics"
    if current_db == "weapons":
        url = "http://www.lootlemon.com/db/borderlands-2/weapons"
        keys = ['alt', 'title', 'width', 'height', 'loading', 'src', 'data-rarity', 'data-name', 'data-type', 'data-manufacturer', 'data-elements', 'data-content', 'data-sources', 'data-locations', 'data-advanced']
        header = ['data-name', 'data-rarity', 'title', 'data-type', 'data-manufacturer', 'data-elements', 'data-content', 'data-sources', 'data-locations']
        header_indices = [1,6,7,8,9,10,11,12,13]
        removed_keys = [0,2,3,4,5,14]
    elif current_db == "shields":
        url = "http://www.lootlemon.com/db/borderlands-2/shields"
        keys = ['alt', 'title', 'width', 'height', 'loading', 'src', 'data-rarity', 'data-name', 'data-type', 'data-manufacturer', 'data-elements', 'data-content', 'data-sources', 'data-locations', 'data-advanced']
        header = ['data-name', 'data-rarity', 'title', 'data-type', 'data-manufacturer', 'data-elements', 'data-content', 'data-sources', 'data-locations']
        header_indices = [1,6,7,8,9,10,11,12,13]
        removed_keys = [0,2,3,4,5,14]
    elif current_db == "grenade-mods":
        url = "http://www.lootlemon.com/db/borderlands-2/grenade-mods"
        keys = ['alt', 'title', 'width', 'height', 'loading', 'src', 'data-rarity', 'data-name', 'data-type', 'data-manufacturer', 'data-elements', 'data-content', 'data-sources', 'data-locations', 'data-advanced']
        header = ['data-name', 'data-rarity', 'title', 'data-type', 'data-manufacturer', 'data-elements', 'data-content', 'data-sources', 'data-locations']
        header_indices = [1,6,7,8,9,10,11,12,13]
        removed_keys = [0,2,3,4,5,14]
    elif current_db == "class-mods":
        url = "http://www.lootlemon.com/db/borderlands-2/class-mods"
        keys = ['alt', 'title', 'width', 'height', 'loading', 'src', 'data-rarity', 'data-name', 'data-class', 'data-manufacturer', 'data-content', 'data-sources', 'data-locations', 'data-advanced']
        header = ['data-name', 'data-rarity', 'title', 'data-class', 'data-manufacturer', 'data-content', 'data-sources', 'data-locations']
        header_indices = [1,6,7,8,9,10,11,12]
        removed_keys = [0,2,3,4,5,13]
    elif current_db == "relics":
        url = "http://www.lootlemon.com/db/borderlands-2/relics"
        keys = ['alt', 'title', 'width', 'height', 'loading', 'src', 'data-rarity', 'data-name', 'data-type', 'data-content', 'data-sources', 'data-locations', 'data-advanced']
        header = ['data-name', 'data-rarity', 'title', 'data-type', 'data-content', 'data-sources', 'data-locations']
        header_indices = [1,6,7,8,9,10,11]
        removed_keys = [0,2,3,4,5,12]
    else:
        print("INVALID database choice, setting db to weapons")
        url = "http://www.lootlemon.com/db/borderlands-2/weapons"


    output_csv = "db_" + current_db + "_unique.csv"
    driver = grab_html(url)
    
    

    driver.get(url)

    time.sleep(8)
   
    selenium_fullpage = driver.page_source
    selenium_fullpage = str(selenium_fullpage).replace('\x80', "").replace('\x93',"").replace('\x8d',"").replace('\x9f',"").replace('\u200d',"").replace('\U0001f9e1',"")
    driver.close()

    print(selenium_fullpage)
    soup = BeautifulSoup(selenium_fullpage, features="html.parser")
    table = soup.find('div', class_ = 'db_table')
    header_array = table.find_all('div', class_ = 'db_sort-button')
    headers = [ each_col_header.text for each_col_header in header_array ]
    df = pd.DataFrame(columns = headers)

    inner_table = soup.find('div', class_ = 'w-dyn-items')
    
    row_array = soup.find_all('img', attrs={"alt":['Discoverable icon', 'Quest Item icon', 'Dedicated Drop icon', 'Quest Reward icon', 'Unobtainable icon', 'Shop Item icon', 'World Drop icon']})

    row_data = []
    loop_row_data = []
    count = 0


    
    
    with open(output_csv, 'w', newline='') as weapons_db:
        wr = csv.writer(weapons_db)
        wr.writerow(header)
        print(row_array[0].attrs)
        print(row_array[0].attrs.keys())
        for each_row in row_array: # Quest, Boss, Rare Spawn, Named Enemy, Unqiue, Raid Boss, Shop, Location. Enemy
            
          
            loop_row_data = each_row.attrs
            loop_row_vals = list(loop_row_data.values())
            loop_row_vals = [s.strip() for s in loop_row_vals]
            for removed_key in reversed(removed_keys):
                del loop_row_vals[int(removed_key)]
            temp = loop_row_vals[0]
            loop_row_vals[0] = loop_row_vals[2]
            loop_row_vals[2] = temp
          
            row_data += loop_row_vals
            wr.writerow(loop_row_vals)
        
     
        print(row_data[0])
        print(len(row_array))
        print(count)
        # print(len(row_array))
        ## ASCII Art ##
        # url = "https://www.lootlemon.com/db/borderlands-2/weapons"
        # image = requests.get(url, stream=True).raw
        # #image = PIL.Image.open(requests.get(url, stream=True).raw)
        # print(image)

    
    

if __name__ == '__main__':
    main()