from urllib.parse import urlparse

import selenium.common.exceptions as sel_excepts
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from . import fed_res

lst_msgs = []
child_lst = []
selenium_message = []


async def get_driver():
    options = Options()
    options.headless = False
    driver = webdriver.Chrome('/home/driver220v/Documents/ChromeDriver/chromedriver', options=options)
    return driver


async def load_initial_page(driver, company_name):
    # url_req = 'https://fedresurs.ru/search/entity?name=<company_name>'
    url_req = f'{fed_res}={company_name}'
    driver.get(url_req)
    # wait until full list of companies will be loaded
    wait = WebDriverWait(driver, 10)  # timeout 10 sec
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "td_name")))
    # List is loaded. Return html code
    html = driver.execute_script('return document.documentElement.outerHTML')
    return html


async def find_url_company(soup):
    # set company to None
    searched_company = None
    # Search for all href's in a list
    for anchor_link in soup.find_all('a'):

        href = anchor_link.get('href')
        # if href is string and string starts with /company
        # href = company/ca48285e-8e7c-43d0-aced-798b759c5949
        if type(href) == str and href.startswith('/company'):
            # urlparse(fed_res).scheme = https
            # urlparse(fed_res).netloc = fedresurs.ru
            # abs_path= https://fedresurs.ru/company/ca48285e-8e7c-43d0-aced-798b759c5949
            # todo input search page and click. Dont create abs_url
            abs_url = f'{urlparse(fed_res).scheme}://{urlparse(fed_res).netloc}{href}'
            searched_company = abs_url
            break
    return searched_company


async def load_messages(driver, searched_company):
    driver.get(searched_company)
    wait = WebDriverWait(driver, 10)  # timeout 30 sec

    while True:
        # wait until button is loaded
        try:
            # todo fix : if element doesn't exist anymore -> no need wait till timeout exceeds or button does not exist at all
            wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "button[class='btn btn_load_more']")))
        except sel_excepts.TimeoutException:
            break
        # find this button
        btn_to_click = driver.find_element_by_css_selector('button.btn.btn_load_more')
        # if this button exists click it
        if btn_to_click:
            btn_to_click.click()

        else:
            break
    html = driver.execute_script('return document.documentElement.outerHTML')
    return html


async def find_company_main(company_name):
    # wait untill we get webdriver
    global a
    driver = await get_driver()
    # get html page
    source = await load_initial_page(driver, company_name)

    soup = BeautifulSoup(source, features="lxml")
    searched_company = await find_url_company(soup)
    # open new tab
    driver.execute_script("window.open('');")
    # switch to newly opened tab
    driver.switch_to.window(driver.window_handles[1])
    # load page with all messages
    html_msgs = await load_messages(driver, searched_company)
    msgs = BeautifulSoup(html_msgs, features="lxml")

    # todo following part should be remastered
    # make like iterator
    for msg in msgs.find_all('div', class_="msg_item_body"):
        lst_msgs.append(msg)
    # make like iterator

    # how to click in javascript
    for child in lst_msgs:
        try:
            a = child.getText()

        except AttributeError:
            pass

        child_entries = child.find_all('a')

        if len(child_entries) > 1:
            for child in child_entries:
                child_lst.append(child)

        else:
            child_lst.append(*child.find_all('a'))
    print(child_lst)
    er = 0
    good = 0
    for i in child_lst:
        # print(dir(i))
        print(i.name)
        print('___' * 20)
        # if b.startswith('Сообщение'):
        msg_to_find = WebDriverWait(driver, 10, ).until(
            ec.visibility_of_element_located((By.TAG_NAME, i.name)))
        selenium_message.append(msg_to_find)
    for b in selenium_message:
        print(b)
        try:
            driver.get(b.click())
        except Exception as e:
            print(e)

    #     try:
    #         # msg_to_find.click()
    #         # driver.get(msg_to_find.click())
    #         tab = driver.execute_script("arguments[0].click()", msg_to_find)
    #         # driver.get(tab)
    #         good += 1
    #     except Exception as e:
    #         er += 1
    #         print(e)
    # print('good', good)
    # print('er', er)

    #     try:
    #         driver.get(msg_to_find.click())
    #     except Exception as t:
    #         print('----' * 15)
    #         print(child)
    #         print('t', t)

    # try:
    #
    #     msg_to_find = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
    #          ec.visibility_of_element_located((By.TAG_NAME, child.getText())))
    #     print('ok')
    # except Exception as e:
    #     print(e)

    # print('dir', dir(child))
    # print('child.name',child.name)

    # todo children may not be present on a page. However it is present \
    #  child.text is printed
    # msg_to_find = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
    #     ec.visibility_of_element_located((By.TAG_NAME, child.name)))
    # # msg_to_find = driver.find_element_by_tag_name(child.name)
    # driver.execute_script("window.open('');")
    # driver.switch_to.window(driver.window_handles[2])
    # msg_to_open = msg_to_find.click()
    # driver.get(msg_to_open)
