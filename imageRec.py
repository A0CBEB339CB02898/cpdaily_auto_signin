from PIL import Image, ImageEnhance
import pytesseract
import re

#验证码识别模块 
#会在运行目录下读取captcha并且生成处理后的captcha_pic_aft 识别整理后输出验证码
def imageRecognition():
    captcha_pic = "./captcha_pic.png"
    captcha_pic_aft = './captcha_pic_aft.png'

    threshold = 120  # 默认阈值为160

    #图像处理
    img = Image.open(captcha_pic)

    #二值化
    img = img.convert('L')
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    img = img.point(table,'1')


    img.save(captcha_pic_aft)

    # pytesseract识别
    img = Image.open(captcha_pic_aft)
    captcha = pytesseract.image_to_string(img)
    #正则表达式优化
    captcha = re.sub(r'\W+', '', captcha).strip()
    
    print('验证码:',captcha)
    return captcha
    
if __name__ == "__main__":
    imageRecognition()