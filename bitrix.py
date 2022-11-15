# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 07:30:42 2022

@author: iri
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium import webdriver
import time
import secrets
import os  # , threading
import logging

class selenium_and_bitrix(object):
    
    driver = webdriver
    change_os = {'posix': r'/home/iri/geckodriver', 'nt': os.getcwd() + "\\geckodriver.exe"}

    logging.basicConfig(filename='bitrix.log', level=logging.INFO)
    
    def __init__(self):

        # change_os = {'posix': r'/home/iri/geckodriver', 'nt': os.getcwd() + "\\geckodriver.exe"}
        self.driver = self.driver.Firefox(executable_path=self.change_os[os.name])

        pass
        
        
    def repassword(self, login, password):

        self.driver.get('https://bitrix24.net/?start_change_password=yes')
        self.driver.set_window_size(1800, 1000)
        time.sleep(0.5)
        self.driver.find_element(By.ID, "login").click()
        self.driver.find_element(By.ID, "login").send_keys(login)
        time.sleep(0.5)
        self.driver.find_element(By.ID, "login").send_keys(Keys.ENTER)
        time.sleep(0.5)
        try:
            if self.driver.find_element(By.CSS_SELECTOR, ".b24-network-auth-form-field-error").is_displayed():
                logging.error(time.ctime() + " Логин не подошел: " + login)
                return 'Логин не подошёл'
        except:
            print('Login ok')
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(0.5)
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
        time.sleep(0.5)
        try:
            if self.driver.find_element(By.CSS_SELECTOR, ".b24-network-auth-form-field-error").is_displayed():
                logging.error(time.ctime() + " ст.пароль не подходит: " + login + ' ' + password)
                return 'Старый пароль не подходит'
        except:
            print('Password ok')
        time.sleep(3)
        self.driver.switch_to.frame(0)
        time.sleep(3.5)
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(0.5)

        new_passwd = self.passwd_gen()
        print(login, new_passwd)

        self.driver.find_element(By.ID, "new_password").click()
        self.driver.find_element(By.ID, "new_password").send_keys(new_passwd)
        self.driver.find_element(By.ID, "new_password_confirm").click()
        self.driver.find_element(By.ID, "new_password_confirm").send_keys(new_passwd)
        time.sleep(0.5)
        self.driver.find_element(By.NAME, "SAVE_PASSWORD").click()
        # self.driver.switch_to.default_content()
        time.sleep(2)
        logging.info(time.ctime() + ' смена пароля: ' + login + ' - ' + new_passwd + " | старый пароль:" + password)
        return new_passwd

    def passwd_gen(self, pl=8):
        alphabet = 'abcdefghjknopqrstuvwxyzABCDEFGHJKMNOPQRSTUVWXYZ1234567890'

        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(pl))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password)):
                break
        return password
        
    def teardown_method(self):
        self.driver.quit()
        
if __name__ == "__main__":

    # bx = selenium_and_bitrix()
    # print(bx.repassword('bars@holdweb.ru', 'password'))
    # bx.teardown_method()
    pass