import requests
from bs4 import BeautifulSoup
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import imageRec
#模拟登陆 获取cookie


max_tryTime=7
#登录尝试最大次数

def login(username,password):
    """
     模拟登录
     :param username: 学号
     :param password: 密码-今日校园学工号登录的密码
     :return: (str)sign_cookie
    """
    urllib3.disable_warnings(InsecureRequestWarning)
    session = requests.session()

    login_url = "https://authserver.gdou.edu.cn/authserver/login?service=https%3A%2F%2Fgdou.cpdaily.com%2Fportal%2Flogin"

    captcha_url = 'https://authserver.gdou.edu.cn/authserver/captcha.html'

    lt = BeautifulSoup(session.get(login_url,verify=False).text, features='html.parser').select_one('input[name="lt"]')['value']
    try_time = 0
    while True:
        try_time = try_time+1
        with open("captcha_pic.png","wb+") as f:
                f.write(session.get(captcha_url,verify=False).content)

        captcha=imageRec.imageRecognition()
        
        body = {
            'username': username,
            'password': password,
            'captchaResponse': captcha,
            'lt': lt,
            'execution': 'e1s1',
            '_eventId': 'submit',
            'rmShown':'1'
        }
        s = session.post(login_url,data=body,verify=False)

        wrongMes = BeautifulSoup(s.text,features='html.parser').select_one(".errMsg").text

        cookies=requests.utils.dict_from_cookiejar(s.cookies)
        if 'MOD_AUTH_CAS' in cookies:
            #登录成功
            MOD_AUTH_CAS = cookies['MOD_AUTH_CAS']
            acw_tc       = cookies['acw_tc']
            signin_cookie = 'acw_tc={0}; MOD_AUTH_CAS={1}; clientType=cpdaily_student; tenantId=1018762497675547; sessionToken=7155a083-f70c-4e54-9d17-a97065b26c0d'.format(acw_tc,MOD_AUTH_CAS)
            print('识别率:',100/try_time,'%')
            break
        
        elif wrongMes=='\n您提供的用户名或者密码有误\n':
            signin_cookie="0"
            print(wrongMes)
            break
        
        #限制最大尝试数
        elif try_time>max_tryTime:
            print("超过最大尝试次数，可能出现未知错误")
            signin_cookie="0"
            break

    return signin_cookie

if __name__ == "__main__":
    login('2222','2222')