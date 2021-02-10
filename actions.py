# -*- coding: utf8 -*-
from datetime import datetime, timedelta, timezone
import time
import requests
import random
import muggle_ocr
import os
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

def run(txtUid,txtPwd):

    session = requests.session()
    url = 'http://202.118.120.21/SPCP/Web/'
    session.get(url)
    r = session.post(url, {'ReSubmiteFlag': 'flag',
                            'StuLoginMode': '5',
                            'txtUid': '',
                            'txtPwd': '',
                            'code': 'code'})

    cookies = r.cookies.get_dict()
    sessionId = 'ASP.NET_SessionId={}'.format(cookies['ASP.NET_SessionId'])
    print(sessionId)

    headers = {
        'Cookie': sessionId,
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
    }
    session.headers = headers
    r = session.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    flag = soup.input['value']

    now = datetime.now().astimezone(timezone(timedelta(hours=8)))
    timestamp = round(time.mktime(now.timetuple()) *
                          1000.0 + now.microsecond / 1000.0)
    imgurl = 'http://202.118.120.21/SPCP/Web/Account/GetLoginVCode?dt=' + \
            str(timestamp)
    # print(imgurl)

    img = requests.get(imgurl, headers=headers, stream=True)
    if img.status_code == 200:
        open('yzm.jpg', 'wb').write(img.content)  # 将内容写入图片
    del img

    with open(r"yzm.jpg", "rb") as f:
        captcha_bytes = f.read()

    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
    code = sdk.predict(image_bytes=captcha_bytes)
    # print(code)

    data = {
            'ReSubmiteFlag': flag,
            'StuLoginMode': '5',
            'txtUid': txtUid,
            'txtPwd': txtPwd,
            'code': code
    }
    r = session.post(url, data)
    cookies = session.cookies.get_dict()

    session = requests.session()
    for k, v in cookies.items():
        session.cookies[k] = v

    url = 'http://202.118.120.21/SPCP/Web/Temperature/StuTemperatureInfo'
    r = session.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    now = datetime.now().astimezone(timezone(timedelta(hours=8)))

    if soup.input == None:
        #qmsg_send('Cookies失效,重新获取Cookies')
        print('[Retry : '+now.strftime('%Y-%m-%d %H:%M:%S')+' ]')
        run(txtUid,txtPwd)
    else:
        data = {
            'TimeNowHour': now.hour,
            'TimeNowMinute': now.minute,
            'Temper1': '36',
            'Temper2': random.randint(0, 9),
            'ReSubmiteFlag': soup.input.attrs['value']
        }
        r = session.post(url, data)
        data1 = {
            'Time': '%s:%s' % (data['TimeNowHour'], data['TimeNowMinute']),
            'Temper': '%s:%s' % (data['Temper1'], data['Temper2']),
            'status_code': r.status_code
        }
        print('[ Success: '+now.strftime('%Y-%m-%d %H:%M:%S')+str(data1)+' ]')
        qmsg_send('Success: '+now.strftime('%Y-%m-%d %H:%M:%S')+str(data1))
        r = session.get('http://202.118.120.21/SPCP/Web/Account/Logout')

def qmsg_send(msg):
    requests.get(
        'https://qmsg.zendee.cn/send/{}?msg={}'.format(qmsgkey, msg))
