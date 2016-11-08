import datetime
import importlib
import logging
import time
import traceback

import requests
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


config = importlib.import_module('config')
config = {key: getattr(config, key) for key in dir(config) if key.isupper()}
logging.basicConfig(format='%(asctime)s - %(message)s')


def login_to_facebook(driver):
    driver.get('https://www.facebook.com/')
    time.sleep(7)
    driver.find_element_by_css_selector('#email').send_keys(config['FACEBOOK']['email'])
    driver.find_element_by_css_selector('#pass').send_keys(config['FACEBOOK']['password'])
    driver.find_element_by_css_selector('#pass').send_keys('\n')
    time.sleep(7)


def login_to_hipmenu(driver):
    driver.get('https://www.hipmenu.ro/')
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#h-profilelogin'))
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#loginCtrl-facebookId'))
    time.sleep(7)


def get_order_url(driver):
    driver.get(config['HIPMENU']['restaurant_url'])
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#h-restInfoPanel-createGroupId'))
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#hd-grpEntry-left-continueId'))
    time.sleep(7)
    order_url = driver.find_element_by_css_selector('#hd-grpEntry-left-urlId b').text
    if order_url is None:
        raise ValueError('Invalid order URL')
    return order_url


def login_to_skype(driver):
    driver.get('https://web.skype.com/')
    time.sleep(7)
    driver.find_element_by_css_selector('#username').send_keys(config['SKYPE']['username'])
    driver.find_element_by_css_selector('#username').send_keys('\n')
    time.sleep(7)
    driver.find_element_by_css_selector('#i0118').send_keys(config['SKYPE']['password'])
    driver.find_element_by_css_selector('#i0118').send_keys('\n')
    # Skype is slow, be patient with Skype
    time.sleep(25)


def send_skype_message(driver, message):
    # click on the conversation
    for a in driver.find_elements_by_css_selector('a'):
        if config['SKYPE']['conversation_title'] in a.text:
            driver.execute_script('arguments[0].click()', a)
    time.sleep(7)
    # click on the last textarea
    driver.execute_script('arguments[0].click()', driver.find_elements_by_css_selector('#textarea-bindings textarea')[-1])
    time.sleep(7)
    ActionChains(driver).send_keys(message).send_keys('\n').perform()
    time.sleep(7)


def wait():
    now = datetime.datetime.now()
    while now.hour < config['HIPMENU']['order_time']['hour'] or now.minute < config['HIPMENU']['order_time']['minute']:
        time.sleep(60)
        now = datetime.datetime.now()


def send_order(driver, order_url):
    driver.get(order_url)
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#hd-grpEntry-left-submit1Id'))
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#cartPointer'))
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#h-cartcontent-conf-119'))
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#h-cartsum-checkout'))
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#h-chkaddr-mainAddrId'))
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#h-chkpay-kittyOptionNoId'))
    time.sleep(7)
    driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#h-chktime-mainTimeId'))
    time.sleep(7)
    if not config['TEST']:
        driver.execute_script('arguments[0].click()', driver.find_element_by_css_selector('#h-checkout-sendOrderBtnId'))
    time.sleep(7)


def send_sms(message):
    payload = {
        'api_key': config['NEXMO']['api_key'],
        'api_secret': config['NEXMO']['api_secret'],
        'to': config['NEXMO']['phone_number'],
        'from': 'hipmenu-autoorder',
    }
    payload['text'] = message
    if not config['TEST']:
        requests.get('https://rest.nexmo.com/sms/json', params=payload)


if __name__ == '__main__':
    try:
        logging.info('starting up')
        display = Display(visible=0, size=(1366, 768))
        display.start()
        driver = webdriver.Chrome(config['CHROMEDRIVER_PATH'])
        driver.set_window_size(1366, 768)
        driver.implicitly_wait(10)
        logging.info('login to facebook')
        login_to_facebook(driver)
        logging.info('login to hipmenu')
        login_to_hipmenu(driver)
        logging.info('get order url')
        order_url = get_order_url(driver)
        logging.info('order_url: {}'.format(order_url))
        message = '{} => {} Order will be sent at {}:{}. This is an automated message via https://github.com/g4b1nagy/hipmenu-autoorder'.format(
            config['HIPMENU']['restaurant_name'],
            order_url,
            config['HIPMENU']['order_time']['hour'],
            config['HIPMENU']['order_time']['minute'],
        )
        logging.info('login to skype')
        login_to_skype(driver)
        logging.info('send skype message')
        send_skype_message(driver, message)
        logging.info('wait for it')
        wait()
        logging.info('send order')
        send_order(driver, order_url)
        logging.info('THE END')
    except Exception as e:
        print(traceback.format_exc())
    finally:
        driver.quit()
        display.stop()
