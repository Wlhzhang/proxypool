import requests
from lxml import etree


class Login(object):
    def __init__(self):
        self.headers = {
            'Referer':'https://github.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Host':'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.session()

    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div//input[2]/@value')[0]
        return token

    def login(self, email, password):
        post_data = {
            'commit':'Sign in',
            'utf8':'√',
            'authenticity_token':self.token(),
            'login':email,
            'password':password
        }
        response = self.session.post(self.post_url,data=post_data,headers=self.headers)
        if response.status_code == 200:
            print('1')
            self.dynamics(response.text)

        response = self.session.get(self.login_url,headers=self.headers)
        if response.status_code == 200:
            print('2')
            self.profile(response.text)

    def dynamics(self, html):
        print(html)
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class,"news")]//div[contains(@class,"alert")]')
        for item in dynamics:
            dynamic = ' '.join(item.xpath('.//div[@class="title"]//text()').strip())
            print(dynamic)

    def profile(self, html):
        print(html)
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name, email)

if __name__ == '__main__':
    login = Login()
    login.login(email='Wlhzhang',password='142857Zj@.520')