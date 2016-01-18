__author__ = 'yezier'
import requests
login_link = 'http://fridge.insomnihack.ch/login'
from selenium import webdriver
from selenium.webdriver.common.by import By
import itertools
import string
from xvfbwrapper import Xvfb

def get_crf_token():
    s = requests.Session()
    r = s.get(login_link)
    return s.cookies

def register_user(username, password, cookies):
    s = requests.Session()
    crf_token = cookies['csrftoken']
    register_link = "http://fridge.insomnihack.ch/register"
    payload = {'username': username, 'password': password, 'email': '', 'description': '', 'csrfmiddlewaretoken': crf_token}
    r = s.post(register_link, data=payload, cookies=cookies, headers=dict(Referer=login_link))
    print r.status_code

def set_up_driver():
    driver = webdriver.Firefox()
    driver.implicitly_wait(3)
    driver.set_window_size(1920, 1080)
    return driver

def log_in(username, password, driver):

    driver.get(login_link)
    while True:
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        if driver.find_elements(By.XPATH, "//img[@class='fridge']"):
            break
    return driver

def search_for_food(food, driver):
    driver.find_elements(By.NAME, 'term')[1].clear()
    driver.find_elements(By.NAME, 'term')[1].send_keys(food)
    driver.find_elements(By.XPATH, "//input[@value='Search']")[1].click()
    hash = driver.current_url
    driver.back()
    return hash.split('/')[-2]

def search_for_users(users, driver):
    driver.find_elements(By.NAME, 'term')[0].clear()
    driver.find_elements(By.NAME, 'term')[0].send_keys(users)
    driver.find_elements(By.XPATH, "//input[@value='Search']")[0].click()
    hash = driver.current_url
    driver.back()
    return hash.split('/')[-2]

xvfb = Xvfb(width=1920, height=1080)
xvfb.start()
driver = set_up_driver()
crf_token = get_crf_token()
register_user('adamoadamo', 'password', crf_token)
charset = string.printable # comment after printable char not found
#charset = "".join([chr(i) for i in xrange(256)]) # uncomment after printable char not found
log_in('adamoadamo', 'password', driver)
res = itertools.product(charset, repeat=1) # 1 is the length of your result.
for i in res:
    x = ''.join(i)
    hash = search_for_food('aaaaaaaaaaaaaaaaaaaaaaaa'+x+'aaaaaaaaaaaaaaa', driver)
    #hash = search_for_food('aaaaaaaaaaaaaaaaaaaaaaa|'+x+'aaaaaaaaaaaaaa', driver) # after find first letter post string
    #hash = search_for_food('aaaaaaaaaaaaaaaaaaaaaa|t'+x+'aaaaaaaaaaaaa', driver) # after find second letter post string etc.
    a = hash[32:64]
    b = hash[64:96]
    print x # comment after printable char not found
    # print ":".join("{:02x}".format(ord(c)) for c in x) # uncomment after printable char not found
    if a == b:
        print a, b
        break
driver.quit()
xvfb.stop()
