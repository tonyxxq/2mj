from urllib import request, parse


# with request.urlopen('https://www.baidu.com') as f:
#     data = f.read()
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', data.decode('utf-8'))

# 模拟浏览器发送 get 请求，使用 Request
# req = request.Request('http://www.douban.com/')
# req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
# with request.urlopen(req) as f:
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', f.read().decode('utf-8'))


# 输入用户名密码进行登录
# login_data = parse.urlencode([
#     ('userid', 'xiexq@edu-edu.com.cn'),
#     ('password', '******'),
# ])
#
# req = request.Request('http://www.edu-edu.com/cas/web/login/execute/save')
# req.add_header('Origin', 'http://www.edu-edu.com')
# req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
# req.add_header('Referer', 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2Fhttp://www.edu-edu.com/cas/web/login?service=http%3A%2F%2Fwww.edu-edu.com%2F%3Fst%3DST-602870-ShpuchaQB2KdAfssnNYx7pdVguy4xMvk7XW')
# with request.urlopen(req, data=login_data.encode('utf-8')) as f:
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', f.read().decode('utf-8'))

# proxy_handler = request.ProxyHandler({'http': 'http://www.example.com:3128/'})
# proxy_auth_handler = request.ProxyBasicAuthHandler()
# proxy_auth_handler.add_password('realm', 'host', 'username', 'password')

# from http.cookiejar import CookieJar
#
# # 获取 CookieJar 对象
# cookiejar = CookieJar()

# 获取 cookie 处理器对象
# 参数为 CookieJar 对象，将自动把第一次 POST 请求时，生成的 cookie 信息保存起来，
# 以后再请求同一服务器时，将自动提供该信息
# cookie_handler = request.HTTPCookieProcessor(cookiejar)
#
# # 构建opener
# opener = request.build_opener(cookie_handler)
#
# # 输入用户名密码进行登录
# login_data = parse.urlencode([
#     ('userid', 'xiexq@edu-edu.com.cn'),
#     ('password', 'qiangge115143'),
# ])
#
# req = request.Request('http://www.edu-edu.com/cas/web/login/execute/save')
# req.add_header('Origin', 'http://www.edu-edu.com')
# req.add_header('User-Agent',
#                'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
# req.add_header('Referer',
#                'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2Fhttp://www.edu-edu.com/cas/web/login?service=http%3A%2F%2Fwww.edu-edu.com%2F%3Fst%3DST-602870-ShpuchaQB2KdAfssnNYx7pdVguy4xMvk7XW')
#
# with opener.open(req) as f:
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', f.read().decode('utf-8'))
#
# for item in cookiejar:
#     print(item.name, item.value)
#
# #
# req = request.Request('http://www.edu-edu.com/cas/home/my/baseinfo/?__ajax=true&__isSearch=true&_=1557973663776')
# req.add_header('Origin', 'http://www.edu-edu.com')
# req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
# req.add_header('Referer',  'http://www.edu-edu.com/cas/home/index?_tenant=default#change_base_info')
# with opener.open(req) as f:
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', f.read().decode('utf-8'))

import json

# 访问 ajax 接口获取 json 数据，并转为 python 对象
# with request.urlopen("http://www.edu-edu.com/cas/web/login/execute?__isSearch=true") as f:
#     rs_raw = f.read().decode('utf-8')
#     rs_json = json.loads(rs_raw)
#     print(rs_json)

# 获取二进制流，两种方式
import requests


# from urllib.request import urlretrieve
# urlretrieve("http://www.edu-edu.com/cas/web/message/captcha.png", './img1.png')
#
# r = requests.get("http://www.edu-edu.com/cas/web/message/captcha.png")
# with open('./img2.png', 'wb') as f:
#     f.write(r.content)

# 创建验证码
# from PIL import Image, ImageDraw, ImageFont, ImageFilter
#
# import random
#
# # 随机字母:
# def rndChar():
#     return chr(random.randint(65, 90))
#
# # 随机颜色1:
# def rndColor():
#     return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
#
# # 随机颜色2:
# def rndColor2():
#     return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
#
# # 240 x 60:
# width = 60 * 4
# height = 60
# image = Image.new('RGB', (width, height), (255, 255, 255))
# # 创建Font对象:
# font = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', 36)
# # 创建Draw对象:
# draw = ImageDraw.Draw(image)
# # 填充每个像素:
# for x in range(width):
#     for y in range(height):
#         draw.point((x, y), fill=rndColor())
# # 输出文字:
# for t in range(4):
#     draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())
# # 模糊:
# # image = image.filter(ImageFilter.BLUR)
# image.save('code.jpg', 'jpeg')
def say_hello():
    print("hello!")

import sys

def print_argv():
    print(sys.argv)



if __name__ == '__main__':
    print_argv()