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
    
    lt_headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'authserver.gdou.edu.cn',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    lt = BeautifulSoup(session.get(login_url,headers=lt_headers,verify=False).text, features='html.parser').select_one('input[name="lt"]')['value']
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

        
        #获取网页中的错误提示
        wrongMes = BeautifulSoup(session.post(login_url,data=body,verify=False).text,features='html.parser').select_one(".errMsg")

        cookies=requests.utils.dict_from_cookiejar(session.cookies)

        if 'MOD_AUTH_CAS' in cookies:
            #登录成功
            MOD_AUTH_CAS = cookies['MOD_AUTH_CAS']
            acw_tc       = cookies['acw_tc']
            signin_cookie = 'acw_tc={0}; MOD_AUTH_CAS={1}; clientType=cpdaily_student; tenantId=1018762497675547; sessionToken=7155a083-f70c-4e54-9d17-a97065b26c0d'.format(acw_tc,MOD_AUTH_CAS)
            print('识别率:',100/try_time,'%')
            break
        
        elif type(wrongMes)!=None:
            if wrongMes.text=='\n您提供的用户名或者密码有误\n':
                signin_cookie="0"
                print(wrongMes.text)
                break
        
        #限制最大尝试数
        elif try_time>max_tryTime:
            print("超过最大尝试次数，可能出现未知错误")
            signin_cookie="0"
            break

    return signin_cookie

if __name__ == "__main__":
    login('2222','2222')

