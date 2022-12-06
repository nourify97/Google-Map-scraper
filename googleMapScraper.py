'''
Google Map Scraper Using Selenium
By Nourify 16 Nov, 2022
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlparse

import csv
import time

big_usa_cities = ['New York', 'Los Angeles']

pages = 2
search_for = 'Doctor in'
google_url = 'https://www.google.com'

for city in big_usa_cities:
    search_term = search_for
    output_filename = search_term.replace(" ", "_")
    header = ["title", "website"]
    data = []


    search_term = search_term + ' ' + city
    output_filename = (output_filename + '_' + city.replace(" ", "") + '.csv').lower()

    print(search_term)
    print(output_filename)

    options = webdriver.ChromeOptions()
    #options.add_experimental_option("detach", True)
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.get(google_url)

    driver.find_element(By.XPATH, '//*[@id="L2AGLb"]/div').click()

    driver.implicitly_wait(2)
    driver.find_element(By.NAME,"q").send_keys(search_term + Keys.ENTER)
    more = driver.find_element(By.TAG_NAME,"g-more-link")
    more_btn = more.find_element(By.TAG_NAME,"a")
    more_btn.click()
    time.sleep(6.5)

    website_xpath = '/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[4]/c-wiz/div/div/a[1]'

    for page in range(2, pages+1):
        elements = driver.find_elements(By.CSS_SELECTOR, 'div#search a[class="vwVdIc wzN8Ac rllt__link a-no-hover-decoration"')
        counter = 1
        for element in elements:
            element.click()
            print('item click... 5 seconds...')
            time.sleep(3.5)

            #title
            title = driver.find_element(By.CSS_SELECTOR,'h2[data-attrid="title"]')
            print('\n')
            print('title: ', title.text)

            #website
            try:
                temp_obj = driver.find_element(By.XPATH, website_xpath)
                website = temp_obj.get_attribute('href')
            except NoSuchElementException:
                website =""
                print('Im here')
            if (website != "") :
                website = urlparse(website).scheme + '://' + urlparse(website).hostname
            else : website = 'No website'
            print('website:', website)


            row = [title.text, website]
            data.append(row)
            counter+=1
        try:
            page_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Page ' + str(page) + '"]')
            page_button.click()
            print('page click... 10 seconds...')
            time.sleep(10)
        except NoSuchElementException:
            break

    with open(output_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)
