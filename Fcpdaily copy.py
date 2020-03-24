# -*- coding: utf-8 -*-
# python 3.7.0
#
from selenium import webdriver
from time import sleep
from PIL import Image, ImageEnhance
import pytesseract
import re
import requests
#填充用户名，密码
#填充浏览器驱动
#自行抓包或者查询自己签到位置的经纬度及地名，将作为签到位置提交
#signin函数中body的abnormalReason参数为签到时输入的文本，默认为一个空格
#若验证码识别率过低可以根据生成的captcha_pic效果自行调整二值化阈值
#本脚本仅供学习交流，否则后果自负

#该账号密码为http://authserver.gdou.edu.cn/authserver/login处的账号与密码
username = 'Enter your username here'
password = 'Enter your password here'


def get_cookie():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    # 浏览器驱动位置，请自行配置并输入路径
    driver = webdriver.Chrome(r'浏览器驱动路径/chromedriver.exe',chrome_options=option)
    driver.maximize_window()
    try_time = 0
    while True:
        driver.get("http://authserver.gdou.edu.cn/authserver/login?service=https%3A%2F%2Fgdou.cpdaily.com%2Fportal%2Flogin")
        # 等待
        driver.implicitly_wait(5) 

        captcha_pic = "./captcha_pic.png"
        captcha_pic_bef = './captcha_pic_bef.png'


        #截屏
        driver.get_screenshot_as_file(captcha_pic)

        size = driver.find_element_by_id('captchaImg').size

        # 手动修正验证码位置,如果发现验证码识别率低可以考虑自行修改
        left = 687
        top =  250
        right = 688 + size['width'] -3
        bottom = 251 + size['height'] -3

        # 验证码裁剪
        img = Image.open(captcha_pic).crop((left, top, right, bottom))
        img.save(captcha_pic)

        #图像处理
        img = Image.open(captcha_pic)

        # img = img.convert('RGBA')  # 转换模式：L | RGB
        # img = img.convert('L')  # 转换模式：L | RGB
        # img = ImageEnhance.Contrast(img)  # 增强对比度
        # img = img.enhance(2.0)  # 增加饱和度

        #二值化
        img = img.convert('L')
        threshold = 160  # 设定阈值

        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        img = img.point(table,'1')

        img.save(captcha_pic_bef)

        # pytesseract识别
        img = Image.open(captcha_pic_bef)
        captcha = pytesseract.image_to_string(img)
        #正则表达式优化
        captcha = re.sub(r'\W+', '', captcha).strip()
        
        print('验证码:',captcha)

        # 定位输入框
        username_box = driver.find_element_by_id('username')
        password_box = driver.find_element_by_id('password')
        captcha_box =driver.find_element_by_id('captchaResponse')

        #清空输入框
        username_box.clear()
        password_box.clear()
        captcha_box.clear()

        #输入内容
        username_box.send_keys(username)
        password_box.send_keys(password)
        captcha_box.send_keys(captcha)

        driver.find_element_by_xpath('//*[@id="login_form1"]/div/ul/p[4]/button').click()

        #尝试次数
        try_time=try_time+1

        #判断是否登录成功 跳出循环
        if driver.get_cookies()[0]['name']=='MOD_AUTH_CAS':
            break
            
    #组装cookie
    login_cookie = driver.get_cookies()
    MOD_AUTH_CAS = login_cookie[0]['value']
    acw_tc       = login_cookie[1]['value']

    signin_cookie = 'acw_tc={0}; MOD_AUTH_CAS={1}; clientType=cpdaily_student; tenantId=1018762497675547; sessionToken=7155a083-f70c-4e54-9d17-a97065b26c0d'.format(acw_tc,MOD_AUTH_CAS)
    print('尝试次数:',try_time)
    print('识别率:',100/try_time,'%')
    print("signin_cookie:"+signin_cookie)

    return signin_cookie
#每天的签到任务都有一个wid并且不递增，要用该请求获取
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
    signINstanceWid = r.json()['datas']['unSignedTasks'][0]['signInstanceWid']
    return signINstanceWid

def sign_in(global_cookie):
    url = 'https://gdou.cpdaily.com/wec-counselor-sign-apps/stu/sign/submitSign'

    headers={
    'tenantId': '1018762497675547',
    'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.4; SM-G9350 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.12.4',
    'CpdailyStandAlone': '0',
    'extension': '1',
    'Cpdaily-Extension': 'CEzs4zRiNZDRs6kUbgbXcfy038GONsXOnuU5brmSNbrq779Z06Ld4aaOhJXP knEjShqKP3hIxaT3NvYekc++1so/qobhD6N9JhpdcWeQHO9SdRZiJMoY2oqs nwB2lGKX+1GAiAcR8ddEyagdfOOXKSpmQUzIUDM/+hKlEbZsm/eZUfgrJpjX ZUXdvT9WEFRT5y5GACLegKRGhs0rhdNH4iSzh2+46hyZLUiz+ep84SzD5m/q FP71ssX+ZooufKeeJ8uYpjVMZIw=',
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': '188',
    'Host': 'gdou.cpdaily.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Cookie': global_cookie
    }
#请自行修改该处的经纬度和地址
    body={"signInstanceWid":get_signInstanceWid(global_cookie),"longitude":113.2457494300,"latitude":23.1303438200,"isMalposition":1,"abnormalReason":" ","signPhotoUrl":"","position":"广东省广州市荔湾区中山八路29号"}

    r = requests.post(url,headers=headers,json=body)
    if r.json()['message'] =='SUCCESS':
        print("签到成功")

if __name__ == "__main__":
    global_cookie = get_cookie()
    sign_in(get_cookie)
