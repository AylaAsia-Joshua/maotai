#!/usr/bin/env python

import os
import platform
from time import sleep
import time
import random
from datetime import datetime as datetime

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = "D:\\Projects\\drivers\\chromedriver.exe"
PAYPASS = '901225'
# 添加一个变量或函数把抢购时间定义，是不是datetime变量更合适？
time_str = datetime.now().strftime("%Y-%m-%d")+" 20:00:00"
KILL_TIME = datetime.strptime(time_str,"%Y-%m-%d %H:%M:%S")

print(KILL_TIME)


def keep_wait(driver,ktime=KILL_TIME):
    while True:
        if (ktime - datetime.now()).seconds <=10:
            print(1)
            break
        if(datetime.now().microsecond%100000==0):
            print("当前时间{}持续等待".format(datetime.now()))


def before_keep_wait(driver,ktime=KILL_TIME):
    """
    抢购前等待函数
    """
    print('抢购前等待')
    while True:
        current_time = datetime.now()
        if(ktime-current_time).seconds > 180:
            print('刷新购物车网页，防止卡死')
            driver.get("https://cart.taobao.com/cart.htm")
            sleep(60)
        else:
            print('三分钟内开始抢购，准备开始')
            break


def isElementPresent(css_str):
      try:
          driver.find_element_by_css_selector(css_str)
          return True
      except Exception as e:
          return False


def wait_some_time():
    time.sleep(random.randint(300, 600) / 1000)


def secKill(driver):
    count = 0
    while True:
        count+=1
        print(count)
        WebDriverWait(driver,10,0.001).until(EC.presence_of_element_located((By.ID,'J_SelectAll1')))
        driver.find_element_by_id("J_SelectAll1").click()
        WebDriverWait(driver,0.3,0.001).until_not(EC.presence_of_element_located((By.CSS_SELECTOR,'a.submit-btn-disabled')))
        driver.find_element_by_css_selector('a.submit-btn').click()
        print("点击了结算按钮")
        
        while True:
            try:
                WebDriverWait(driver,1,0.0001).until(EC.presence_of_element_located((By.CSS_SELECTOR,'a.go-btn')))
                driver.find_element_by_css_selector('a.go-btn').click()
                print('done')
            except Exception as e:
                print("something wrong")
                wait_some_time()
                driver.back()
                break


def start_kill():


    options = webdriver.ChromeOptions()
    # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    options.add_experimental_option('excludeSwitches', ['enable-automation']) 
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 


    driver = webdriver.Chrome(executable_path=DRIVER_PATH,options=options)
    driver.get("https://cart.taobao.com/cart.htm")


    input("登录完回车")

    before_keep_wait(driver)
    keep_wait(driver)
    secKill(driver)


if __name__ == '__main__':
    a = """                               
功能列表：                                                                                
 1.开始
    """
    print(a)

    choice_function = input('请选择:')
    if choice_function == '1':
        start_kill()
    else:
        print('没有此功能')
        sys.exit(1)


