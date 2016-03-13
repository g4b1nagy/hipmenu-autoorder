import datetime
import importlib
import time
import traceback

import requests
from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains


config = importlib.import_module('config')
config = {key: getattr(config, key) for key in dir(config) if key.isupper()}


def login_to_facebook(driver):
    driver.get('https://www.facebook.com/')
    time.sleep(5)
    driver.find_element_by_css_selector('#email').send_keys(config['FACEBOOK']['email'])
    driver.find_element_by_css_selector('#pass').send_keys(config['FACEBOOK']['password'])
    driver.find_element_by_css_selector('#pass').send_keys('\n')
    time.sleep(5)


def login_to_hipmenu(driver):
    driver.get('https://www.hipmenu.ro/')
    time.sleep(5)
    # use the new version of hipMenu
    driver.add_cookie({'name': 'hip_rollout', 'value': '2', 'path': '/'})
    driver.refresh()
    time.sleep(5)
    driver.find_element_by_css_selector('#h-profilelogin').click()
    time.sleep(5)
    driver.find_element_by_css_selector('#loginCtrl-facebookId').click()
    time.sleep(5)


def get_order_url(driver):
    driver.find_element_by_css_selector('#h-addrListPicker-addressNameId').send_keys(config['HIPMENU']['delivery_address']['street'])
    driver.find_element_by_css_selector('#h-addrListPicker-addressNumberId').send_keys(config['HIPMENU']['delivery_address']['number'])
    driver.find_element_by_css_selector('#h-addrListPicker-btnFindRestaurantsId').click()
    time.sleep(5)
    driver.get(config['HIPMENU']['restaurant_url'])
    time.sleep(5)
    driver.find_element_by_css_selector('#h-restInfoPanel-createGroupId').click()
    time.sleep(5)
    driver.find_element_by_css_selector('#hd-grpEntry-left-submit3Id').click()
    time.sleep(5)
    order_url = driver.find_element_by_css_selector('#hd-grpEntry-left-urlId').get_attribute('value')
    if order_url is None:
        raise ValueError('Invalid order URL')
    return order_url


def login_to_skype(driver):
    driver.get('https://web.skype.com/')
    time.sleep(5)
    driver.find_element_by_css_selector('#username').send_keys(config['SKYPE']['username'])
    driver.find_element_by_css_selector('#password').send_keys(config['SKYPE']['password'])
    driver.find_element_by_css_selector('#password').send_keys('\n')
    # Skype is slow, be patient with Skype
    time.sleep(20)


def send_skype_message(driver, message):
    xpath = '//span[contains(text(), "{}")]'.format(config['SKYPE']['conversation_title'])
    driver.find_element_by_xpath(xpath).click()
    time.sleep(5)
    ActionChains(driver).send_keys(message).send_keys('\n').perform()
    time.sleep(5)


if __name__ == '__main__':
    try:
        driver = Firefox()
        driver.implicitly_wait(10)
        login_to_facebook(driver)
        login_to_hipmenu(driver)
        order_url = get_order_url(driver)
        message = 'Apetit => {} Order will be closed at 10:55. This is an automated message via https://github.com/g4b1nagy/hipmenu-autoorder'.format(order_url)
        login_to_skype(driver)
        send_skype_message(driver, message)
    except Exception as e:
        print(datetime.datetime.now())
        print(traceback.format_exc())
        print()
        payload = {
            'api_key': config['NEXMO']['api_key'],
            'api_secret': config['NEXMO']['api_secret'],
            'to': config['NEXMO']['phone_number'],
            'from': 'hipmenu-autoorder',
            'text': 'Error sending hipMenu order :(',
        }
        # requests.get('https://rest.nexmo.com/sms/json', params=payload)
