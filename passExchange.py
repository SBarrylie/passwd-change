# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 07:41:16 2022

@author: iri
"""

import requests
import sys
import pandas as pd
import random
import configparser
import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import QSize
from PyQt5 import uic, QtWidgets
from passTools import Ui_PassTools
import bitrix as bx
import threading
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


class mywindow(QtWidgets.QMainWindow):
    api_url = 'https://pddimp.yandex.ru/api2/admin/'

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_PassTools()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('key.ico'))
        self.ui.pushButton_6.clicked.connect(self.password_Generator)
        self.ui.pushButton_8.clicked.connect(self.copy_password_gen)
        self.ui.pushButton_4.clicked.connect(self.copy_password_ya)
        self.ui.copy_pass.clicked.connect(self.copy_password_b24)
        self.ui.pushButton.clicked.connect(self.yandexFileDialog)
        self.ui.pushButton_3.clicked.connect(self.start_thr)
        self.ui.b24_in_file_btn.clicked.connect(self.b24FileDialog)
        self.ui.pushButton_2.clicked.connect(self.pd_changeMail)
        self.ui.commandLinkButton.clicked.connect(open_ya_xlsx)
        self.ui.yandex_account_file.clicked.connect(self.open_old_ya_xlsx)
        self.ui.commandLinkButton_2.clicked.connect(open_b24_log)
        self.ui.b24_open_new_file.clicked.connect(open_b24_xlsx)
        self.ui.b24_account_file.clicked.connect(self.open_old_b24_xlsx)
        self.ui.change_one_pass_b24.clicked.connect(self.one_pass_B24)
        self.ui.b24_start_pass_xls.clicked.connect(self.read_xl_change_b24)
        
    def start_thr(self):
        th1 = threading.Thread(target=self.change_mail)
        th1.start()
        
    def one_pass_B24(self):
        b24_app = bx.selenium_and_bitrix()
        try:
            passwd = b24_app.repassword(login=self.ui.input_line_b24.text(), password=self.ui.lineEdit_3.text())
        except:
            passwd = 'Ошибка'
        b24_app.teardown_method()
        self.ui.b24_one_new_pass.setText(passwd)
        
    def read_xl_change_b24(self):
        df_pass = pd.read_excel(self.ui.b24_in_file.text())
        df_pass.fillna('skip', inplace=True)
        df_pass.columns = ['Account', 'oldPassword','newPassword']
        for i, y in enumerate(df_pass['Account']):
            if y == 'skip':
                print('skip', y)
                continue
            b24_app = bx.selenium_and_bitrix()
            try:
                passwd = b24_app.repassword(df_pass.loc[i][0], df_pass.loc[i][1])
            except:
                passwd = 'Ошибка'
            df_pass['newPassword'][i] = passwd
            b24_app.teardown_method()
        fileHandler = open(os.getcwd() + '\\xlsx\\b24_new_pswd.xlsx', "r")
        if fileHandler.closed == False:
            self.file_error()
        fileHandler.close()
        df_pass.to_excel(os.getcwd() + '\\xlsx\\b24_new_pswd.xlsx')
        self.final()
        
    def password_gen(self, length=8):
        '''Простой генератор пароля'''
        chars = 'abcdefghjknopqrstuvwxyzABCDEFGHJKMNOPQRSTUVWXYZ1234567890'
        password = ''
        for i in range(length):
            password += random.choice(chars)
        return password

    def password_Generator(self):
        password = password_gen(length=self.ui.spinBox.value())
        self.ui.passGen_6.setText(password)

    def copy_password_gen(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.ui.passGen_6.text())

    def copy_password_ya(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.ui.label_5.text())
        
    def copy_password_b24(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.ui.b24_one_new_pass.text())

    def yandexFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')[0]
        self.ui.lineEdit.setText(fname)

    def b24FileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')[0]
        self.ui.b24_in_file.setText(fname)

    def read_token(self, domain):
        '''Parameters
        ----------
        domain : string
            Домен типа example.ru
        Returns
        -------
        result : string
            токен от домена '''

        config = configparser.ConfigParser()
        config.read('token.ini')
        try:
            result = config.get('token', domain)
        except:
            print(f"У нас нет такого домена: {domain}")
            result = False

        return result

    def changePassword(self, domain, account):
        """
        Меняет пароль на почте яндекса для домена. "mail@holdweb.ru"
        Parameters
        ----------
        domain : string
            домен привязанный к почте яндекса, после @
        account : string
            аккаунт, перед @

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        token = read_token(domain)   # вызывает из ini файла токен домена
        if token:
            password = password_gen()  # генерирует пароль
            response_url = api_url + "email/edit?domain=" + \
                domain + "&login=" + account + "&password=" + password
            response = requests.post(response_url, headers={
                                     'PddToken': token})  # Запрос смены пароля
            if response.status_code == 200:
                if response.json()['success'] == "error":
                    #print("Ошибка:", response.json()['error'])
                    print('Пароль не установлен. логин не подошел?')
                    return False, "error login"
                else:
                    return password, response.json()['login']
            else:
                print("не удалось сменить пароль", response.status_code)
                return False, "error network"
        else:
            return False, "error domain"
    
    def pd_changeMail(self):
        dfAccounts = pd.read_excel(self.ui.lineEdit.text())
        dfAccounts.columns = ['mail', 'password']
        dfAccounts.fillna(value="skip", inplace=True)
        dfAccounts['domain'] = dfAccounts['mail'].str.split("@")
        for i, l in enumerate(dfAccounts.domain):
            if len(l) == 2:
                password = self.changePassword(l[1], l[0])
                if password[0]:
                    dfAccounts.loc[i][1] = password[0]
                else:
                    dfAccounts.loc[i][1] = password[1]
            else:
                dfAccounts.loc[i][1] = "не почта"
        del(dfAccounts['domain'])
        self.file_error()
        dfAccounts.to_excel(os.getcwd() + '\\xlsx\\new_password.xlsx')
        self.final()
    
    def final(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Смена паролей завершена")
        msgBox.setWindowTitle("Уведомление")
        msgBox.exec_()
    
    def file_error(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Закройте Excel файл и нажмите OK")
        msgBox.setWindowTitle("Ошибка")
        msgBox.exec_()
        
    def change_mail(self):
        try:
            email = self.ui.lineEdit_2.text()
            account, domain = email.split('@')
            result = self.changePassword(domain, account)
            if result[0]:
                self.ui.label_5.setText(result[0])
            else:
                self.ui.label_5.setText(result[1])
        except:
            self.ui.label_5.setText('не почта')
    
    def open_old_ya_xlsx(self):
        os.startfile(os.getcwd() + '\\xlsx\\mails.xlsx')
        self.ui.lineEdit.setText(os.getcwd() + '\\xlsx\\mails.xlsx')
    
    def open_old_b24_xlsx(self):
        os.startfile(os.getcwd() + '\\xlsx\\b24s.xlsx')
        self.ui.b24_in_file.setText(os.getcwd() + '\\xlsx\\b24s.xlsx')


api_url = 'https://pddimp.yandex.ru/api2/admin/'

def open_ya_xlsx():
    os.startfile(os.getcwd() + '\\xlsx\\new_password.xlsx')
    

    
def open_b24_log():
    os.startfile('bitrix.log')

def open_b24_xlsx():
    os.startfile(os.getcwd() + '\\xlsx\\b24_new_pswd.xlsx')
    


def read_token(domain):
    '''
    Parameters
    ----------
    domain : string
        Домен типа example.ru
    Returns
    -------
    result : string
        токен от домена
    '''
    config = configparser.ConfigParser()
    config.read('token.ini')
    try:
        result = config.get('token', domain)
    except:
        print(f"У нас нет такого домена: {domain}")
        result = False

    return result


def add_token(domain, token):
    '''
    Добавляет новый домен и токен к нему
    Parameters
    ----------
    domain : string
        Домен типа example.ru
    token : string
        строка токена. Получить модно по ссылке
        https://pddimp.yandex.ru/api2/admin/get_token
    '''
    config = configparser.ConfigParser()
    config.read('token.ini')
    config.set('token', domain, token)

    with open('token.ini', 'w') as config_file:
        config.write(config_file)


def password_gen(length=8):
    '''
    Простой генератор пароля
    '''
    chars = 'abcdefghjknopqrstuvwxyzABCDEFGHJKMNOPQRSTUVWXYZ1234567890'
    password = ''
    for i in range(length):
        password += random.choice(chars)
    return password


def changePassword(domain, account):
    """
    Меняет пароль на почте яндекса для домена. "mail@holdweb.ru"
    Parameters
    ----------
    domain : string
        домен привязанный к почте яндекса, после @
    account : string
        аккаунт, перед @

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    token = read_token(domain)   # вызывает из ini файла токен домена
    if token:
        password = password_gen()  # генерирует пароль
        response_url = api_url + "email/edit?domain=" + \
            domain + "&login=" + account + "&password=" + password
        response = requests.post(response_url, headers={
                                 'PddToken': token})  # Запрос смены пароля
        if response.status_code == 200:
            if response.json()['success'] == "error":
                #print("Ошибка:", response.json()['error'])
                print('Пароль не установлен. логин не подошел?')
                return False, "login", response.text
            else:
                return password, response.json()['login'], response.json()['success']
        else:
            print("не удалось сменить пароль", response.status_code)
            return False, "status_code"
    else:
        return False, "domain"



if __name__ == "__main__":

    # app = QApplication(sys.argv)
    # ex = Example()
    # sys.exit(app.exec_())
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec_())
