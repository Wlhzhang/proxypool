import base64
import random
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = '13258387521'
PASSWORD = '142857Zj@.520'
BORDER = 6
INIT_LEFT = 60

class CrackGeetest():
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD

    def __del__(self):
        # 关闭浏览器
        self.browser.close()

    def get_login_button(self):
        '''
        获取登录按钮
        :return: 按钮对象
        '''
        button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'a.btn.btn-login')))
        return button

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.geetest_slider_button')))
        return slider

    def get_geetest_image(self):
        """
        获取验证码图片
        :return: 图片对象
        """
        # 带阴影的图片
        im = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.geetest_canvas_bg')))
        time.sleep(2)
        im.screenshot('captcha.png')

        # 执行 JS 代码并拿到图片 base64 数据
        JS = 'return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("image/png");'
        # 不带阴影的完整图片
        im_info = self.browser.execute_script(JS)  # 执行js文件得到带图片信息的图片数据
        # 拿到base64编码的图片信息
        im_base64 = im_info.split(',')[1]
        # 转为bytes类型
        captcha1 = base64.b64decode(im_base64)
        # 将图片保存在本地
        with open('captcha1.png', 'wb') as f:
            f.write(captcha1)
            # 执行 JS 代码并拿到图片 base64 数据
            JS = 'return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("image/png");'  # 带阴影的图片
            im_info = self.browser.execute_script(JS)  # 执行js文件得到带图片信息的图片数据
            # 拿到base64编码的图片信息
            im_base64 = im_info.split(',')[1]
            # 转为bytes类型
            captcha2 = base64.b64decode(im_base64)
            # 将图片保存在本地
            with open('captcha2.png', 'wb') as f:
                f.write(captcha2)

        captcha1 = Image.open('captcha1.png')
        captcha2 = Image.open('captcha2.png')
        return captcha1, captcha2

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        username.send_keys(self.username)
        password.send_keys(self.password)

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        # 设置一个阈值 允许有误差
        threshold = 60
        # 彩色图 每个位置的像素点有三个通道
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 1.5
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def login_successfully(self):
        """
        判断是否登陆成功
        :return:
        """
        try:
            # 登录成功后 界面上会有一个消息按钮
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@title="消息"]')))
            )
        except TimeoutException:
            return False

    def login(self):
        """
        登录
        :return: None
        """
        self.open()# 输入用户名和密码
        button = self.get_login_button()  # 找到登录按钮
        button.click()  # 点击
        image1, image2 = self.get_geetest_image() # 获取验证码图片
        gap = self.get_gap(image1, image2)# 找到缺口的左侧边界 在x方向上的位置
        print('缺口位置：', gap)
        gap -= BORDER # 减去滑块左侧距离图片左侧在x方向上的距离 即为滑块实际要移动的距离
        track = self.get_track(gap)# 获取移动轨迹
        print('滑动轨迹：', track)
        slider = self.get_slider() # 点按滑块
        self.move_to_gap(slider, track) # 按轨迹拖动滑块
        if self.login_successfully():
            print("登录成功")
        else:  # 可能不成功 再试一次
            time.sleep(5)
            self.login()

if __name__ == '__main__':
    crack = CrackGeetest()
    crack.login()