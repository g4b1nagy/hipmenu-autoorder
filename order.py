import datetime
import importlib
import time
import traceback

import requests
from pyvirtualdisplay import Display
from selenium.webdriver import FirefoxProfile, Firefox
from selenium.webdriver.common.action_chains import ActionChains


config = importlib.import_module('config')
config = {key: getattr(config, key) for key in dir(config) if key.isupper()}


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
    # use the new version of hipMenu
    driver.add_cookie({'name': 'hip_rollout', 'value': '2', 'path': '/'})
    driver.refresh()
    time.sleep(7)
    driver.find_element_by_css_selector('#h-profilelogin').click()
    time.sleep(7)
    driver.find_element_by_css_selector('#loginCtrl-facebookId').click()
    time.sleep(7)


def get_order_url(driver):
    driver.find_element_by_css_selector('#h-addrListPicker-addressNameId').send_keys(config['HIPMENU']['delivery_address']['street'])
    driver.find_element_by_css_selector('#h-addrListPicker-addressNumberId').send_keys(config['HIPMENU']['delivery_address']['number'])
    driver.find_element_by_css_selector('#h-addrListPicker-btnFindRestaurantsId').click()
    time.sleep(7)
    driver.get(config['HIPMENU']['restaurant_url'])
    time.sleep(7)
    driver.find_element_by_css_selector('#h-restInfoPanel-createGroupId').click()
    time.sleep(7)
    driver.find_element_by_css_selector('#hd-grpEntry-left-submit3Id').click()
    time.sleep(7)
    order_url = driver.find_element_by_css_selector('#hd-grpEntry-left-urlId').get_attribute('value')
    if order_url is None:
        raise ValueError('Invalid order URL')
    return order_url


def login_to_skype(driver):
    driver.get('https://web.skype.com/')
    time.sleep(7)
    driver.find_element_by_css_selector('#username').send_keys(config['SKYPE']['username'])
    driver.find_element_by_css_selector('#password').send_keys(config['SKYPE']['password'])
    driver.find_element_by_css_selector('#password').send_keys('\n')
    # Skype is slow, be patient with Skype
    time.sleep(25)


def send_skype_message(driver, message):
    xpath = '//span[contains(text(), "{}")]'.format(config['SKYPE']['conversation_title'])
    driver.find_element_by_xpath(xpath).click()
    time.sleep(7)
    # click on the last textarea
    driver.find_elements_by_css_selector('#textarea-bindings textarea')[-1].click()
    time.sleep(7)
    ActionChains(driver).send_keys(message).send_keys('\n').perform()
    time.sleep(7)


def send_order(driver, order_url):
    now = datetime.datetime.now()
    while now.hour < 10 or now.minute < 55:
        time.sleep(60)
        now = datetime.datetime.now()
    driver.get(order_url)
    time.sleep(7)
    driver.find_element_by_css_selector('#hd-grpEntry-left-submit1Id').click()
    time.sleep(7)
    driver.find_element_by_css_selector('#cartPointer').click()
    time.sleep(7)
    driver.find_element_by_css_selector('#h-cartsum-checkout').click()
    time.sleep(7)
    driver.find_element_by_css_selector('#h-checkout-delivery').click()
    time.sleep(7)
    driver.find_element_by_css_selector('#h-checkout-mainAddr').click()
    time.sleep(7)
    driver.find_element_by_css_selector('#h-checkout-kittyOptionNo').click()
    time.sleep(7)
    driver.find_element_by_css_selector('#h-checkout-mainTime').click()
    time.sleep(7)
    if not config['TEST']:
        driver.find_element_by_css_selector('#h-checkout-sendOrderBtn').click()
    time.sleep(7)


if __name__ == '__main__':
    payload = {
        'api_key': config['NEXMO']['api_key'],
        'api_secret': config['NEXMO']['api_secret'],
        'to': config['NEXMO']['phone_number'],
        'from': 'hipmenu-autoorder',
    }
    try:
        print(datetime.datetime.now())
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        profile = FirefoxProfile()
        # Skype rejects Iceweasel; fuck Skype
        profile.set_preference('general.useragent.override', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
        driver = Firefox(profile)
        driver.set_window_size(1920, 1080)
        driver.maximize_window()
        driver.implicitly_wait(10)
        print('login to facebook')
        login_to_facebook(driver)
        print('login to hipmenu')
        login_to_hipmenu(driver)
        print('get order url')
        order_url = get_order_url(driver)
        print(order_url)
        message = 'Apetit => {} Order will be closed at 10:55. This is an automated message via https://github.com/g4b1nagy/hipmenu-autoorder'.format(order_url)
        print('login to skype')
        login_to_skype(driver)
        print('send skype message')
        send_skype_message(driver, message)
        payload['text'] = 'hipMenu message sent. Good job!'
        if not config['TEST']:
            requests.get('https://rest.nexmo.com/sms/json', params=payload)
        print('send order')
        send_order(driver, order_url)
    except Exception as e:
        print(traceback.format_exc())
        payload['text'] = 'Error sending hipMenu order :('
        if not config['TEST']:
            requests.get('https://rest.nexmo.com/sms/json', params=payload)
    finally:
        driver.quit()
        display.stop()
