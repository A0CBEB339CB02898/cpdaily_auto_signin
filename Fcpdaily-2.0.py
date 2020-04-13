# -*- coding: utf-8 -*-
# python 3.7.0

import time
import requests
import configparser
import login
import creatExtention


#本脚本仅供学习交流，否则后果自负
#仅需修改config.ini对应内容

#必要数据
# username
# password
# longitude
# latitude
# abnormalReason 
# position 

#get_cookie函数不会判断密码错误的问题

def Multiple_signIn_controller():
    config = configparser.ConfigParser()
    config.read("config.ini",encoding="utf-8")
    nop=config.sections().__len__()-1
    while nop>=0:
        c=config[config.sections()[nop]]

        print(c["username"]+" 签到中")

        globle_cookie = login.login(c["username"],c["password"])

        if globle_cookie!="0":
            sign_in(globle_cookie,c["longitude"],c["latitude"],c["abnormalReason"],c["position"],creatExtention.create_cpdaily_extension(c["longitude"],c["latitude"],c["username"]))
        nop=nop-1
    print("签到队列已完成,程序将在10秒后关闭")
    time.sleep(10)

def get_signInstanceWid(global_cookie):


    url = 'https://gdou.cpdaily.com/wec-counselor-sign-apps/stu/sign/getStuSignInfosInOneDay'

    headers={
    'Host': 'gdou.cpdaily.com',
    'Connection':'keep-alive',
    'Content-Length': '2',
    'accept': 'application/json, text/plain, */*',
    'Origin': 'https://gdou.cpdaily.com',
    'x-requested-with': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; vivo xplay6 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 yiban/8.1.11 cpdaily/8.1.11 wisedu/8.1.11',
    'content-type': 'application/json',
    'Referer': 'https://gdou.cpdaily.com/wec-counselor-sign-apps/stu/mobile/index.html?timestamp=1584597152126',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': global_cookie
    }

    body={}

    r = requests.post(url,headers=headers,json=body)

    if r.json()['datas']['unSignedTasks']==[]:
        signinstanceWid="0"
    else:
        signinstanceWid = r.json()['datas']['unSignedTasks'][0]['signInstanceWid']

    return signinstanceWid

def sign_in(global_cookie,longitude,latitude,abnormalReason,position,Extension):
    url = 'https://gdou.cpdaily.com/wec-counselor-sign-apps/stu/sign/submitSign'

    headers={
    'tenantId': '1018762497675547',
    'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.4; vivo xplay6 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 yiban/8.1.11 cpdaily/8.1.11 wisedu/8.1.11',
    'CpdailyStandAlone': '0',
    'extension': '1',
    'Cpdaily-Extension':Extension,
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': '188',
    'Host': 'gdou.cpdaily.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Cookie': global_cookie
    }

    signInstanceWid = get_signInstanceWid(global_cookie)

    body={"signInstanceWid":signInstanceWid,"longitude":longitude,"latitude":latitude,"isMalposition":1,"abnormalReason":abnormalReason,"signPhotoUrl":"","position":position}
    
    if signInstanceWid=="0":
        print("今天已签到")
    else:
        r = requests.post(url,headers=headers,json=body)
        if r.json()['message'] =='SUCCESS':
            print("签到成功")
        else:
            print("签到失败，有可能不在签到时间内或出现未知错误。请自行调试")
            print("详细信息:"+r.json()['message'])
    # print("等待5秒")
    time.sleep(5)

if __name__ == "__main__":
    Multiple_signIn_controller()