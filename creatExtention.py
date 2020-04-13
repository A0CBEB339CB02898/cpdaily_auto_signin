from pyDes import des,CBC,PAD_PKCS5
import uuid
import base64


# DES加密
def encrypt(s, key='ST83=@XV'):
    key = key
    iv = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    encrypt_str = k.encrypt(s)
    return base64.b64encode(encrypt_str).decode()


# 生成Cpdaily-Extension关键签到参数
def create_cpdaily_extension(lon, lat, uid):
    """
     headers中的CpdailyInfo参数
     :param lon: 定位经度
     :param lat: 定位纬度
     :param uid: 学生学号
     :return: Cpdaily-Extension
    """
    s = r'{"systemName":"android","systemVersion":"8.1.0","model":"16th",' \
        r'"deviceId":"' + str(uuid.uuid1()) + '","appVersion":"8.1.11","lon":' \
        + str(lon) + ',"lat":' + str(lat) + ',"userId":"' + str(uid) + '"}'
    extension = encrypt(s)
    return extension

if __name__ == "__main__":
        create_cpdaily_extension('2222', '2222', '2222')