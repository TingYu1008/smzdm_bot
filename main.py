"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

import config

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS
        self.secret_key = ""

    def __json_check(self, msg):
        """
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            self.on_failed(str(result))
            print(result)
            return True
        except Exception as e:
            self.on_failed(str(e))
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = cookies    

    def load_wechat_key(self, key):
        self.secret_key = key

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content

    def on_failed(self, error_msg):
        wechat_url = "https://sctapi.ftqq.com/"+ self.secret_key +".send";
        data = {"title":"smzdm签到失败了！",
                "desp":error_msg}
        requests.Session().post(wechat_url, data = data)


if __name__ == '__main__':
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["COOKIES"]
    SERVERCHAN_SECRETKEY = os.environ["SERVERCHAN_SECRETKEY"]
    sb.load_wechat_key(SERVERCHAN_SECRETKEY)
    sb.load_cookie_str(cookies)
    res = sb.checkin()
    print(res)
    print('代码完毕')
