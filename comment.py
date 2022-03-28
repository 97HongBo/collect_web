# -*- coding: utf-8 -*-
# @Time    : 2022/3/28
# @Author  : LHB
# @Email   : 
# @File    : comment.py
# @Software: 测试脚本

js = """
!function() {
    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    #返回的就是加密参数
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    window.asrsea = d,
    window.ecnonasr = e
}();
"""
#
data = {
    'csrf_token':'',
    'cursor': '-1',
    'offset': '0',
    'orderType': '1',
    'pageNo': '1',
    'pageSize': '20',
    'rid': "R_SO_4_113936",
    'threadId': "R_SO_4_113936"
}
d = data
# bsR3x(["流泪", "强"])
e = '010001'
# bsR3x(Xp7i.md)
f='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
# bsR3x(["爱心", "女孩", "惊恐", "大笑"])
g = '0CoJUm6Qyw8W8jud'

iv = "0102030405060708"

from Crypto.Cipher import AES
from base64 import b64encode
import json
import requests

# def add_to_16(text):
#      if len(text.encode('utf-8')) % 16:
#          add = 16 - (len(text.encode('utf-8')) % 16)
#      else:
#          add = 0
#      text = text + ('\0' * add)
#
#      return text.encode('utf-8')


def add_to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad

    return data.encode('utf-8')

def encrypt(data,g):
    key = g.encode('utf-8')
    iv = "0102030405060708"
    cryptos = AES.new(key=key,mode=AES.MODE_CBC,iv=iv.encode('utf-8'))
    cipher_text = cryptos.encrypt(add_to_16(data))

    # return b64encode(cipher_text).decode('utf-8')
    # return b2a_hex(cipher_text).decode('utf-8')
    return str(b64encode(cipher_text),'utf-8')
def encSecKey():
    return "628a3106cd354eab10ed1a979f9c1f7959813f0b3f5f15191c0dd73e518b43879814f7c733cbacc736f995217313358d15c8c6e246d76743e07f759a1b6c322e583894aba31501c7eb7ca23d586ac867e995b22f35f567368cf5f323218a2d7ce04258a3a42d926aa0243ecdd0127c36ae3f0b6641f664b357f99ad732188ebc"
if __name__ == '__main__':
    encText = encrypt(json.dumps(data),g)
    encText = encrypt(encText,"KzHBzyHms7Mb31Eo")
    url = 'https://music.163.com/weapi/comment/resource/comments/get'
    res = requests.post(url,data={
        'params': encText,
        'encSecKey':encSecKey()
    })
    print(res.text)
