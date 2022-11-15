# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium import webdriver
import time
import secrets
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk
import os  # , threading
import logging


class selenium_bitrix(object):
    # driver = webdriver.Firefox(executable_path=change_os[self.os.name])
    change_os = {'posix': r'/home/iri/geckodriver', 'nt': os.getcwd() + "\\geckodriver.exe"}
    driver = ''

    def __init__(self):
        pass

    def setup_method(self):
        self.driver = webdriver.Firefox(executable_path=self.change_os[os.name])

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
                logging.error(time.ctime() + " Login error: " + login)
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
                logging.error(time.ctime() + " password error: " + login + ' ' + password)
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
        logging.info(time.ctime() + ' password change: ' + login + ' - ' + new_passwd + " | old password:" + password)
        self.driver.quit()
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

    def pswd_clicked(self):
        pass


def file_change():
    file = filedialog.askopenfilename()
    txt.insert(0, file)


def change_pswd():
    df_pass = pd.read_excel(txt.get())
    df_pass.fillna('skip', inplace=True)
    for i, y in enumerate(df_pass['Битрикс']):
        if y == 'skip':
            print('skip', y)
            continue
        app.setup_method()
        n_passw = app.repassword(df_pass.loc[i][0], df_pass.loc[i][1])
        df_pass['Новый пароль'][i] = n_passw
        app.teardown_method()
    df_pass.to_excel(os.path.dirname(txt.get()) + '\\Новые_пароли.xlsx')
    messagebox.showinfo("bitrix", "Смена паролей завершена")

bx = selenium_bitrix()
bx.setup_method()
bx.repassword('bars@holdweb.ru', 'password')

logging.basicConfig(filename='bitrix.log', level=logging.INFO)
app = selenium_bitrix()

window = Tk()
window.title("Программа смены паролей Bitrix24")
lbl = Label(window, text="Вsберите файл Excel с указанными\n логинами и паролями от Bitrix24")
lbl.grid(column=0, row=0)
txt = Entry(window, width=30)
txt.grid(column=0, row=1)
btnfile = Button(window, text="Выбрать файл", command=file_change)
btnfile.grid(column=1, row=1)
btn = Button(window, text="Начать смену паролей", command=change_pswd)
btn.grid(column=0, row=2)
window.mainloop()
