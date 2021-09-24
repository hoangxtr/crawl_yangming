from selenium import webdriver
from time import sleep
import tqdm
import os

chrome_options = webdriver.chrome.options.Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument("--disable-notifications")
chrome = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
# chrome.delete_all_cookies()
# YMLUW490400325
MAX_QUANTITY = 10
current = 0
while current <= MAX_QUANTITY:
    chrome.get("https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx")
    sleep(0.5)
    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    bl_radio = chrome.find_element_by_id('ContentPlaceHolder1_rdolType_1')
    bl_radio.click()

    bl_input = chrome.find_element_by_id('ContentPlaceHolder1_num1')
    bl_input.send_keys('YMLUW490400325')

    input_element = chrome.find_element_by_id('ContentPlaceHolder1_txtVcode')
    input_element.send_keys("ABCD")

    captcha_element = chrome.find_element_by_id('ContentPlaceHolder1_image_CAPTCHA')
    captcha_element.screenshot("./data/yangmin_{0}.jpg".format(current))

    sleep(15)

    btn_track = chrome.find_element_by_id('ContentPlaceHolder1_btnTrack')
    btn_track.click()
    sleep(1)

    current += 1
    if chrome.current_url != 'https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx': 
        current -= 1
        os.remove("./data/yangmin_{0}.jpg".format(current))
# sleep(10)
chrome.close()