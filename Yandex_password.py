 #!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 22:03:42 2021

@author: Iri
"""
import requests
# import json
import pandas as pd
import random
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter.ttk as ttk
# import os  # , threading



class MailEdit(object):
    api_url = 'https://pddimp.yandex.ru/api2/admin/'

    def __init__(self, token_map):
        self.token_map = token_map  # Карта {domain:token}
        #self.domain_check()

    def domain_check(self):
        domain = list(self.token_map.keys())
        print('Проверка доменов')
        for i, y in enumerate(domain):
            values = domain[i]
            request_url = self.api_url+"domain/registration_status?domain="+values
            response = requests.get(request_url, headers={
                                    'PddToken': self.token_map[values]})
            if response.status_code == 200:
                ttx = response.json()['domain'] + " : √ ок"
                # print(ttx)
                tklable.insert(1.0, chars=ttx)
                tklable.insert(1.0, chars=' \n')
            else:
                ttx = response.json()['domain'] + " : ☻ домен не прошел проверку"
                # print(ttx)
                tklable.insert(1.0, chars=ttx)
                tklable.insert(1.0, chars=' \n')

    def mail_edit(self, account, domain):
        password = self.password_gen()
        response_url = self.api_url + "email/edit?domain=" + domain + "&login=" + account + "&password=" + password
        response = requests.post(response_url, headers={
                                 'PddToken': self.token_map[domain]})
        if response.status_code == 200:
            if response.json()['success'] == "error":
                #print("Ошибка:", response.json()['error'])
                password = 'Пароль не установлен'
                return password, response.json()['error']
            else:
                return password, response.json()['login'], response.json()['success']
        else:
            print('Что-то пошло не так')

    def password_gen(self, length=8):
        chars = 'abcdefghjknopqrstuvwxyzABCDEFGHJKMNOPQRSTUVWXYZ1234567890'
        password = ''
        for i in range(length):
            password += random.choice(chars)
        return password


token_map = {
    'mskconsult.ru' : 'BDY6W4BK3ENPRD4FXSMQUAAOTOASYT2QXMYXSJBPT52QK3TLJXHA',
    'centr-sro.com' : 'PP2TNVNDUIXBV6FMDS4YRAVHW7QPYOJ7WKDYV5PZAKFG7NDF7L7A',
    'info.spbmipk.com' : '2XVRXXRT6BN72OV7YLTYF3Q2ZWFZA5QS54E3D5EHBAHMICT6NVIQ',
    '1mchs.ru' : '6UKJOK7X2G7LBVYYZ4YQ4WOEAVOGJZZ2LDZL5KFHEIBQJXPBQVHA',
    'elc1.ru' : 'MZOH5D2OGKMOFTRIXILEF2ROHRAURXR3X3ARN7BXKQWZSPY4LHHQ',
    'centrsro24.ru' : '6SO3HH6N7JHRSRBVMKNU43KSD4JECYE4PXDBT4LOLCMAOY37W5DA',
    'abs-spb24.ru' : 'C6U73Z6XE6PR6XRJ64E3PMFEROCWRUY4U4FBXQRKMVJASTYP4RBA',
    'rest-vcl.ru' : 'BTHTYNFIXNMGLLNRFICYOAJVBLQV5H44I2FQR7DCAYQOJ5QQKU4A',
    'kp-abs.ru' : 'K5VUXJ66JRIAWQOL62FRU67QPTDR4YPTMDOCUJLIQEJ2YKYE76GQ',
    'mchs-mlc.ru' : 'OQDFOGQ55JNWS54FUSRW2RRTF5223T3ZLK56IZGFH7SOHRONEGUQ',
    'msksro.su' : '26R3TC74ZBCNUWD5A4UG4IUW4P6FA3RBDOBQ3H6NACVHOADZG6JA',
    'mskcentr-sro.ru' : 'MWLIOLTWNXOG3JP3MKRPTV4TXLJ2IHHOKJWMEG3VC6PDUHLM5ECQ',
    'result.com.ru' : 'C63Z6MB7JUC2J7JA24LJB45VGTO2BOXEDKXPS6E63ZZACM3WYIGQ',
    'lic-rest24.ru' : '6RZYGYLVDD7MGDWDSDG3K5QA5AOGSVHB3F6OTTUPXRXKLGXTOZPA',
    'srocentr24.com.ru' : 'EAIHIVUTCSGCOMKH4PXEHMNG732R4SWA6PJ5FJZXH67ZN6QIELJQ',
    'spmipk.com' : '5P56U5WGFBE36L6CD6CKJNCL7BNZYBSLZ2BBMZVGPAMJXBMJJTZQ',
    'mchs-vcl.ru' : 'P5OBFXRY64XKOP6QTW6EI275CNXQ3TVXNX2U7MUHOLEMO2WFJGYA',
    'rest-mlc.ru' : 'JVNZUPLALIYQ3MKQIDFMCPABTDX4USOFS572VNT47AV3HP6JRRLA',
    'lic-mchs24.ru' : 'ZZQMPO7TDAJUYHQUMCH7AYM2DGPMYAKDMLN6CINKN5F7VX7TEQKA',
    'centr-kyrs.ru' : '2IUXRDJQNSNFNTOGJYQT42SNGMKYHXHJHSTST2SPLS7SC7FHMY7Q',
    'absolutspb.com.ru' : 'UECS5Y2E2SAMSMG6DPWWBPITDL35ZA4372PHKJX5IY75J53FVKJA',
    'sro-mkc.ru' : 'Z47SS6JP6PSYHW44PJW46XYT53GZNVI2S3HT7PE5VEW3N5CUY7AQ',
    'mcs-sro.ru' : 'C437SWHOTQ7JJKHYSAKVYGJAWYT46GMOAOF46XKJF2LLKI53OG2A',
    'obr-mlc.ru' : 'HKWCSP6LTIHARVKKMJ367IZHDSWFURQS3ZKGNUUWBXLTDITU32IA',
    'total-business.ru' : '52V3PUZK3MK2PQMNSDGFAG7FTJWFEWFHMIKTSH7WFQL2YU75QVAQ',
    'mlc-rf.ru' : 'X7DSSZSSJ3UZP2YGCUVKZAZPXPZLO2XOLFXKVSSHHREVVELVNQ2Q',
    'mcssro.ru' : '35H2U323YNGIZGQBGY5XFK4JKS3CH7X5LOQEDQFBGAIYQTIAAUXA',
    'total-consulting.ru' : '2QTW2VEXIN6KKN2PJAQ6VYHMIOA4HHDRS7MG2UIYVMADJUI3JYIA',
    'sro-mcs.ru' : 'SXAGDRWAUXFLLOTNXDVYILPB5E3DHNEYDN2SY2YIFUZHZCMFLWQA',
    'mskcentr.su' : 'JGFIL7NKOZYJWH7HB2ZSCYHB7DGHIYB7KVBBXO3BJS3L5JCBSE6A',
    'dpo-academ.ru' : '7KIKQAGG3EB7J5HDJYXI5ZNXZH7VS6HEAHSC27DAOWOD3VODQBOA',
    'centr-sros.ru' : 'VZLXZRPSPKQ5YGJF2QWWSUNMEVD2YYY5M4TBNU5367HMDQ2EORIQ',
    'sro-abs.ru' : 'ML3THXF3YXZMSML3E3BDLXZFZXQULHJTBAXZTIASVG2UNDSPGOCA',
    'obraz-lic24.ru' : 'FNCD62E3THPC7E65RLN6XWDOA6XDLDGMAA74A2E4THZC5BS4PAVQ',
    'vcl-mchs.ru' : '2ENTE6JGYK7C6G3264OWQSZZS3DBX36NQU4ZUL5DPQYEUJX4J36A',
    'lice-mchs.ru' : 'OJV2JX726XPLZQFXOLW45WG4N5POKPQTOOYCONBVXBX2I4PHJMXQ',
    'lic-medi.ru' : 'QHP6EDQS22TO6FGLCB33BOSOXS7WPCFI6FKHTJPP7BNROJN2FBSQ',
    'moscow-dpo.ru' : 'D5XBAHLTPTBYESR7MIW2GAH7OUFELOBBONMZOMZ63VSHD6ITP4OQ',
    'lic-farm.ru' : 'L2NF3VZMSMRWBHTK4EFEE2RLNE7QH64E6MVZETTSE5KUFO3TJURQ',
    'hold-web.ru' : 'IQ3N5JQDPTGLMF2I2GQFEJRJ53ZNDONVF2566AEZ7GBYKNTKPLWQ',
    'vcl-rf.ru' : 'BHFP5Z6G5QFPDQBXRHJD3RLNQM2P4ZC6YIH263VUVWERISUWJO4Q',
    'spb-ipk.com' : 'L6KCXZCCT2T6BFLNUTR5AVJPZQBVGNRC7HS7BD4OVYTNTTM24HNA',
    'spmipk.biz' : 'RDG6MXWPSI62K5ZMHLW75QCIUCG3SQYVY6AWJEHDHODLMEIZE54A',
    'dpo-distance.ru' : 'V7C2JBGFTZQ7CZLJXRJPGY24GBUFEHE6EMJR7TEZT274QXLHIZ4Q',
    'sros-centr.ru' : 'AZJ6BIVE4FE6MNPUWPETBTXEDIJ7TMSKXLLUH2KA7SYLGX2NXN7Q',
    'sroabs.ru' : 'YZNE642FTSFFCV62QGLHY52YK5NVBAZDSMV255CZTN7LNGODJXCA',
    'absspb.ru' : 'IYJ7HMLAZWKR5NDJNEBV5E37ZB527TV6OLLOO6GMN3AHMUVH5WUA',
    'vcl-rest.ru' : 'IVTE2PTMKXVVEYLJFVBSDW456FIC4TYGFZZZSPD2FXB2IAZ6GPMQ',
    'spb-institut.ru' : 'QQ3O7IF2QXOFDJG45HRKCHNBZYPXLUREZBBFPA4KWGFTBBFWWQWQ',
    'mkc-sro.ru' : 'QOGYPN4CSMCSMINJ7NZO3GZ63XYAOTUCMFTW2MAJFJI55N527CMA',
    'spb-instit.ru' : 'O5S2HG2R4Q7XK3PF4EL26CLPTFLGA427ORAFQPUCSUL47SIJXZYQ',
    'moskvacentrsro.ru' : 'Z5YOTCIT3YBIKRTWRWVHOABSD67QCPICUMCCYAYUCFFA57QQC2DA',
    'centrsrogroup.ru' : 'LY2V3AEYSNLAY2LZEU7FIH54ARCYBKNK3Y32GYXYBOB7XXUKC4SQ',
    'expertsro24.ru' : 'VFI6A4WURE7O6P5RKFYXOQOAQZR52ZXRQMSUPUDH4TTYCUVHCMBA',
    'lice-rest.ru' : 'LNC3QQCXMSIDHTXTCN6Z3TMIBN7AMGV7TM6CCWO5D57SUCGU2CJQ',
    'licens-world.ru' : 'AIPNFGCGCYMT7CZR2B7PYHEXLP5OOQWRFHFW3G5TJCAJSSJ7PSZA',
    'licensworld.ru' : '3HEPBT3OX3K5AEZVIWL6N6JIXARN6BZYWS34CTEJKAHZOQTR5GXA',
    'www.centrsro24.ru' : '5OP4M4XID2GSLKQXPOKVJP5BRR46ETLIAHP2PSTPG5UEB5WLEKUQ',
    'holdexp.ru' : 'YWGQKB376PQ5CY77EP5DTD25OYY4ZRPB6T6GPPHGJGMW6KIB5QIA',
    'total-consult.ru' : 'ZKQKPXZQHXLNRXFDPVQ5JPLYRI6Z43MI7SWYGS7DITUYNJW2RZYA',
    'institut-pk.ru' : '4IKQOHYDSNJA3KOKHFQ6CNPD36GGR3V3CVOGVEPVQI4XQBYO6DSA',
    'sp-mipk.ru' : 'L5SSK4T4GEC2AKWP4VKSWBNPCEGEMLHOVZAHE7THNHZ7M2FGBP2Q',
    'edsro.center' : 'SQ6UI4CMPUW2KVVXQLZZJ7YJKYWRST7F2QONURHS5NJDWIOTPMWA',
    'abs-spb.com' : 'GEAGKHRLOTYADLHGOX5CPWVUNMRZNO7YKVWWZCYWQFQNYMRDOLMQ',
    'spb.centr-sro.com' : 'U3JBM5FILJZJIKDC7QAUIXHBUMLJROK4I2FR3KOO6JPMTCOJLZMA',
    'sro.abs-spb.com' : 'WAHXVFWIFNWNN6UTIRHL37WJUSMCHDFWFM26WWBJOHJ2NMGWK5BQ',
    'absolut-spb.com' : 'RGP5HSPGGIFXMVYTEYBTQNNFUTFLM3AY4VEQNNIAMSJPXGSSEFCQ',
    'olymp-law.ru' : '5K7HKEYMG5AJ2AKU35HZXACEUJM4QOU63LP5UULPDYNR2YKSGGVA',
    'licenzia-rf.ru' : 'S4KVR4RPDFLTDBFT633US3NZIIJKRS472Y7UFO6V26YO3MKHMD4Q',
    'birzha-sro.ru' : 'KBZA6HX5HUUGZN3RYJSGAJCDMQTWADQEMZCGHD7X2DR5GLPZ23OA',
    'spmipk.ru' : '3EF2FZN2PB2OG2OH4VSYEYYGE346IBJPNIN26GNEEXURJ65K6XHQ',
    'holdexp.ru' : 'YWGQKB376PQ5CY77EP5DTD25OYY4ZRPB6T6GPPHGJGMW6KIB5QIA',
    'holdweb.ru' : 'OQK73WKPHS5USCE4GQCJZZY5YGOZD6XDTJNQEFFSQ5SXVVZPF5QQ',
    'spmipk.org' : 'FYZHQFSKQ23LGT7EDXJUFKTPYOYAUNTDLVTUXNEKVDJULJFY23VA',
    'edsromail.ru' : 'HQGIRB5HDNLO2MT4J2AVBRTXSLBNQVRL2V4CZETDAAHHRJXWN5YQ',
    'obr-e.ru' : 'YMLYEOQVABQ4EXPGHBK6VQ3HH4NX3ZJIEQ3LUZ776CN7LVYCUJNA',
    'expertcons.ru' : 'Z7TOYXSMG3QBOVQ57YQLZOS56GWJOPHZCURUNVHPA2R55K2EBO2A',
    'centrconsal.ru' : 'HKNE3Q6SE4NK76O4SWHCKJKTP2RGFQ5RE5JLVZQOJKOLN32X6UDA',
    'mid-pk.ru' : 'N6XAZEK7INT44S2DK67TD6PECH7PWKAUEE7NXUTDHDOXFWLPSAZQ',
    'edsro.center' : 'SQ6UI4CMPUW2KVVXQLZZJ7YJKYWRST7F2QONURHS5NJDWIOTPMWA',
    'licen-center.ru' : 'XLHA6XEQYYQMXSIDDB7WR4JWKVSUF3IN4YJSPSJ3VDCSJOEXX5WQ',
    'umipk-portal.ru' : 'BSA7C7NU23PVFSLUKDXCDSZQ362GCS6N5Y5MXRXKE22JKZE6KWEA',
    'happymsc.ru' : 'LNQ4D2YRTV5RBLUBBSARTGVMXOXMEDTLEWG2YB2MJQCOCGNN7HQA',
    'holdexp.yaconnect.com' : 'OQK73WKPHS5USCE4GQCJZZY5YGOZD6XDTJNQEFFSQ5SXVVZPF5QQ'

}
def file_change():
    file = filedialog.askopenfilename()
    txt.insert(0, file)

def passwd_r():
    
    df_accounts = pd.read_excel(txt.get())
    df_accounts['Mail_login'] = df_accounts['Mail_login'].str.replace('holdweb.ru', 'holdexp.yaconnect.com', regex=True)
    df_accounts['Name_domain'] = df_accounts['Mail_login'].str.split("@")
    
    my_domain = ['mskconsult.ru', 'holdexp.yaconnect.com', 'centr-sro.com', 'info.spbmipk.com', '1mchs.ru', 'elc1.ru', 'centrsro24.ru', 'abs-spb24.ru', 'rest-vcl.ru', 'kp-abs.ru', 'mchs-mlc.ru', 'msksro.su', 'mskcentr-sro.ru', 'result.com.ru', 'lic-rest24.ru', 'srocentr24.com.ru', 'spmipk.com', 'mchs-vcl.ru', 'rest-mlc.ru', 'lic-mchs24.ru', 'centr-kyrs.ru', 'absolutspb.com.ru', 'sro-mkc.ru', 'mcs-sro.ru', 'obr-mlc.ru', 'total-business.ru', 'mlc-rf.ru', 'mcssro.ru', 'total-consulting.ru', 'sro-mcs.ru', 'mskcentr.su', 'dpo-academ.ru', 'centr-sros.ru', 'sro-abs.ru', 'obraz-lic24.ru', 'vcl-mchs.ru', 'lice-mchs.ru', 'lic-medi.ru', 'moscow-dpo.ru', 'lic-farm.ru', 'hold-web.ru', 'vcl-rf.ru', 'spb-ipk.com', 'spmipk.biz', 'dpo-distance.ru', 'sros-centr.ru', 'sroabs.ru', 'absspb.ru', 'vcl-rest.ru', 'spb-institut.ru', 'mkc-sro.ru', 'spb-instit.ru', 'moskvacentrsro.ru', 'centrsrogroup.ru', 'expertsro24.ru', 'lice-rest.ru', 'licens-world.ru', 'licensworld.ru', 'www.centrsro24.ru', 'holdexp.ru', 'total-consult.ru', 'institut-pk.ru', 'sp-mipk.ru', 'edsro.center', 'abs-spb.com', 'spb.centr-sro.com', 'sro.abs-spb.com', 'absolut-spb.com', 'olymp-law.ru', 'licenzia-rf.ru', 'birzha-sro.ru', 'spmipk.ru', 'holdexp.ru', 'holdweb.ru', 'spmipk.org', 'edsromail.ru', 'obr-e.ru', 'expertcons.ru', 'centrconsal.ru', 'mid-pk.ru', 'edsro.center', 'licen-center.ru', 'umipk-portal.ru', 'happymsc.ru']
    
    app = MailEdit(token_map)
    for i, l in enumerate(df_accounts.Name_domain):
        if type(l) == float: #Проверяем является ячейка адресом почты
            a = ('Это не почта', l, 'no') # Это не адрес почты отправляем сообшение вместо пароля
            # print(a)
            tklable.insert(1.0, chars=str(a))
            tklable.insert(1.0, chars=' \n')
            df_accounts['New_password'][i] = a[0]
            continue
        if len(l) < 2: #Проверяем является ячейка адресом почты
            a = ('Это не почта', l, 'no') # Это не адрес почты отправляем сообшение вместо пароля
            # print(a)
            tklable.insert(1.0, chars=str(a))
            tklable.insert(1.0, chars=' \n')
            df_accounts['New_password'][i] = a[0]
            continue
    
        domain = l[1]
        
        if domain in my_domain: #Проверяем наш это домен или нет
            account = df_accounts['Mail_login'][i]
        else: # Если домен не наш отправляем сообщение вместо пароля
            a = ('Не верный домен', domain, 'no')
            # print(a)
            tklable.insert(1.0, chars=str(a))
            tklable.insert(1.0, chars=' \n')
            df_accounts['New_password'][i] = a[0]
            continue
        
        account = df_accounts['Mail_login'][i]
        a = app.mail_edit(account, domain)
        # print(str(a))
        tklable.insert(1.0, chars=str(a))
        tklable.insert(1.0, chars=' \n')
        df_accounts['New_password'][i] = a[0]
        
    del(df_accounts['Name_domain'])
    df_accounts['Mail_login'] = df_accounts['Mail_login'].str.replace('holdexp.yaconnect.com', 'holdweb.ru', regex=True)
    df_accounts.to_excel("Пароли яндекса.xlsx", index=False)
    messagebox.showinfo("bitrix", "Смена паролей завершена")

window = Tk()
window.title("Смена паролей Yandex`a")
lbl = Label(window, text="Вsберите файл Excel с указанными\n логинами от почты Yandex")
lbl.grid(column=0, row=0)
txt = Entry(window, width=30)
txt.grid(column=0, row=1)
btnfile = Button(window, text="Выбрать файл", command=file_change)
btnfile.grid(column=1, row=1)
btn = Button(window, text="Начать смену паролей", command=passwd_r)
btn.grid(column=0, row=4)
tklable = scrolledtext.ScrolledText(window, width=45, height=15)
tklable.grid(columnspan=2, row=5)
window.mainloop()
