from selenium import webdriver
import tensorflow as tf
import string
from time import sleep
import tqdm
import cv2
import os
import numpy as np
import time


import shutil

def read_captcha_yangming(path):
    img = cv2.imread(path, 0)
    img = cv2.resize(img, (67,25), cv2.INTER_AREA)
    img = img/255.0
    pred = model_yangming.predict(img[np.newaxis, :])
    ret = ''.join([ALPHABET_ALL[np.argmax(pred[i][0])] for i in range(NUM_OF_LETTERS)])
    return ret

def refresh_page():
    chrome.get("https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx")
    sleep(1.5)
    print('\r\nCurrent URL: ', chrome.current_url)

ALPHABET_ALL = string.ascii_uppercase + '0123456789'
NUM_OF_LETTERS = 4

model_yangming = tf.keras.models.load_model('./model_yangming')


chrome_options = webdriver.chrome.options.Options()
# chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument("--disable-notifications")
chrome = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
chrome.delete_all_cookies()
# YMLUW490400325

MAX_QUANTITY = 100000
# current = 255
# current = 570
# current = 2405
# current = 2543
# current = 3202
# current = 8258
# current = 9400
current = 17185


refresh = True

refresh_page()

while current <= MAX_QUANTITY:
    current += 1
        
    print('__________________________________________________________')
    t0 = time.time()
    # path = "./data/yangmin_{0}.jpg".format(current)
    path = "./hoang_fail/yangmin_{0}.jpg".format(current)
    # successful_path = "./successful_captchas/yangmin_{0}.jpg".format(current)
    successful_path = "./hoang_pass/yangmin_{0}.jpg".format(current)
    print(f'{path} start')
    
    try:
        print(f'path: {chrome.current_url}')

        # if refresh:
        #     refresh_page()

        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        captcha_element = chrome.find_element_by_id('ContentPlaceHolder1_image_CAPTCHA')
        captcha_element.screenshot(path)

        bl_radio = chrome.find_element_by_id('ContentPlaceHolder1_rdolType_1')
        bl_radio.click()

        bl_input = chrome.find_element_by_id('ContentPlaceHolder1_num1')
        bl_input.send_keys('YMLUW490400325')

        input_element = chrome.find_element_by_id('ContentPlaceHolder1_txtVcode')
        t1 = time.time()

        captcha_str = read_captcha_yangming(path)

        input_element.send_keys(captcha_str)
        print(f'predict time: {time.time() - t1}')

        # sleep(15)
        print(f'middle_time: {time.time() - t0}')
        btn_track = chrome.find_element_by_id('ContentPlaceHolder1_btnTrack')
        btn_track.click()
        sleep(0.8)

        # current += 1
        # refresh == False

        # if pass
        if chrome.current_url != 'https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx': 
            # current -= 1
            successful_path_with_OCR_str ="./hoang_pass/yangmin_{0}_search__{1}.jpg".format(current, captcha_str)

            # shutil.move(path, successful_path)
            shutil.move(path, successful_path_with_OCR_str)

         

            # os.remove(path)
            # refresh = True
            print(f'{path} remove')
            refresh_page()

        else:
            failed_path_new= "./hoang_fail/yangmin_{0}_search__{1}.jpg".format(current, captcha_str)
            shutil.move(path, failed_path_new)


        
        print(f'{path} end')
        print(f'process time: {time.time() - t0}')
  
    except:
        if chrome.current_url == 'https://www.yangming.com/VerifyYourID.aspx':
            print(f'path: {chrome.current_url}')

            captcha_element = chrome.find_element_by_id('image_CAPTCHA')
            captcha_element.click()
            sleep(0.5)
            captcha_element.screenshot(path)

            input_element = chrome.find_element_by_id('txtVcode')
            input_element.clear()

            

            captcha_str = read_captcha_yangming(path)
            input_element.send_keys(captcha_str)

            btn_verify = chrome.find_element_by_id('btnVerify')
            btn_verify.click()
            sleep(0.8)

            if chrome.current_url != 'https://www.yangming.com/VerifyYourID.aspx': 

                successful_path_with_OCR_str ="./hoang_pass/yangmin_{0}_verified__{1}.jpg".format(current, captcha_str)

                # shutil.move(path, successful_path)
                shutil.move(path, successful_path_with_OCR_str)


                print(f'{path} remove')
                refresh_page()
                sleep(1)
            else:
                failed_path_new= "./hoang_fail/yangmin_{0}_verify__{1}.jpg".format(current, captcha_str)
                shutil.move(path, failed_path_new)


        else:
            print(f'error url: {chrome.current_url}')
            print("An exception occurred")
            # time.sleep(60)
            chrome.delete_all_cookies()
            refresh_page()

# sleep(10)
chrome.close()