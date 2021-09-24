from selenium import webdriver
import tensorflow as tf
import string
from time import sleep
import tqdm
import cv2
import os
import numpy as np

# from tensorflow.compat.v1 import ConfigProto
# from tensorflow.compat.v1 import InteractiveSession

# config = ConfigProto()
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)

def read_captcha_yangming(path):
    img = cv2.imread(path, 0)
    img = cv2.resize(img, (67,25), cv2.INTER_AREA)
    img = img/255.0
    pred = model_yangming.predict(img[np.newaxis, :])
    ret = ''.join([ALPHABET_ALL[np.argmax(pred[i][0])] for i in range(NUM_OF_LETTERS)])
    return ret

def refresh_page():
    chrome.get("https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx")
    sleep(0.5)

ALPHABET_ALL = string.ascii_uppercase + '0123456789'
NUM_OF_LETTERS = 4

model_yangming = tf.keras.models.load_model('/home/hoang/Desktop/Cyber/download_captcha/model_yangming')


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
refresh = True


while current <= MAX_QUANTITY:
    path = "./data/yangmin_{0}.jpg".format(current)
    print(f'{path} start')

    if refresh:
        refresh_page()

    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    captcha_element = chrome.find_element_by_id('ContentPlaceHolder1_image_CAPTCHA')
    captcha_element.screenshot(path)

    bl_radio = chrome.find_element_by_id('ContentPlaceHolder1_rdolType_1')
    bl_radio.click()

    bl_input = chrome.find_element_by_id('ContentPlaceHolder1_num1')
    bl_input.send_keys('YMLUW490400325')

    input_element = chrome.find_element_by_id('ContentPlaceHolder1_txtVcode')
    input_element.send_keys(read_captcha_yangming(path))

    sleep(15)

    btn_track = chrome.find_element_by_id('ContentPlaceHolder1_btnTrack')
    btn_track.click()
    sleep(2)

    current += 1
    refresh == False

    # if pass
    if chrome.current_url != 'https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx': 
        current -= 1
        os.remove(path)
        refresh = True
        print(f'{path} remove')
    
    print(f'{path} end')

# sleep(10)
chrome.close()