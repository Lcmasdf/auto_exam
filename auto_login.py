from time import sleep
import hashlib
import requests
from PIL import Image
import datetime
import xml.etree.ElementTree as ET
import configparser
import codecs
import log

class recognize_val_code:
    def __init__(self):
        self.top_left_x = 0
        self.top_left_y = 0
        self.bottom_right_x = 0
        self.bottom_right_y = 0
        pass

    #设置截取验证码的位置（左上角、右下角的坐标）
    def set_val_pos(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y

    #使用若快答题识别验证码
    def recognize(self, driver):
        #保存当前页面截图
        driver.save_screenshot('val.png')

        #从截图中剪切出验证码部分
        with Image.open('val.png') as img:
            img_val = img.crop((self.top_left_x, self.top_left_y, self.bottom_right_x, self.bottom_right_y))
            img_val.save('upload.gif', format='gif')

        #初始化使用若快识别验证码的API
        url = 'http://api.ruokuai.com/create.xml'
        imagePath = 'val.jpeg'
        paramDict = {'username':'lcmasdf',
                     'password':'lcm123456',
                     'typeid':3040,
                     'timeout':90,
                     'softid':1,
                     'softkey':'b40ffbee5c1cf4e38028c197eb2fc751'}
        paramKeys = ['username',
                     'password',
                     'typeid',
                     'timeout',
                     'softid',
                     'softkey']

        with open('upload.gif', 'rb') as file:
            filebytes = file.read()

            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            boundary = '------------' + hashlib.md5(time_str.encode('utf8')).hexdigest().lower()
            boundary_str = '\r\n--%s\r\n' % (boundary)

            bs = b''
            for key in paramKeys:
                bs = bs + boundary_str.encode('ascii')
                param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s" % (key, paramDict[key])
                bs = bs + param.encode('utf8')
            bs = bs + boundary_str.encode('ascii')

            header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n' % (
                'sample')
            bs = bs + header.encode('utf8')

            bs = bs + filebytes
            tailer = '\r\n--%s--\r\n' % (boundary)
            bs = bs + tailer.encode('ascii')

            headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
                       'Connection': 'Keep-Alive',
                       'Expect': '100-continue',
                       }
            response = requests.post(url, params='', data=bs, headers=headers)

            tree = ET.fromstring(response.text)
            return tree[0].text

class auto_login:
    def __init__(self, config_file_path='config.ini'):
        self.config_file_path = config_file_path
        self.recognize = recognize_val_code()

    #从配置文件中读取验证码的坐标
    def load_configuration(self):
        config = configparser.ConfigParser()
        config.read_file(codecs.open('config.ini', 'r', 'utf-8-sig'))
        top_left_x = int(config.get('img', 'topleft_x'))
        top_left_y = int(config.get('img', 'topleft_y'))
        bottom_right_x = int(config.get('img', 'bottomright_x'))
        bottom_right_y = int(config.get('img', 'bottomright_y'))
        self.recognize.set_val_pos(top_left_x,
                                   top_left_y,
                                   bottom_right_x,
                                   bottom_right_y)

    def login(self, username, password, driver):
        #登录三次失败后，放弃本次登录
        err_login_cnt = 0

        driver.get('http://xxjs.dtdjzx.gov.cn/')
        sleep(2)

        # 关闭提示框
        cancel_tip = driver.find_elements_by_xpath(
            "//body/div[@id='myxiaoxi']/div/div/div[@class='modal-header']/button")
        if cancel_tip[0]:
            cancel_tip[0].click()
            sleep(2)

        #点击左侧竞赛答题
        driver.find_element_by_id('lbuts').click()
        sleep(2)

        #选择党员身份
        shenfen = driver.find_element_by_id('shenfen')
        shenfen.find_element_by_xpath("//option[@value='0']").click()
        btn_confirm = driver.find_element_by_id('bts')
        btn_confirm.click()

        while err_login_cnt < 3:
            #填入用户名密码验证码
            driver.find_element_by_id('username').send_keys(username)
            sleep(1)
            driver.find_element_by_id('password').send_keys(password)
            sleep(1)
            val_code = self.recognize.recognize(driver)
            driver.find_element_by_id("validateCode").send_keys(val_code)
            sleep(1)

            #点击登录
            driver.find_element_by_class_name('js-submit').click()
            sleep(3)

            #若登录失败，增加失败计数，从新开始登录
            if ('https://sso.dtdjzx.gov.cn/sso/login?error' == driver.current_url):
                err_login_cnt += 1
                continue

            #关闭提示框

            cancel_tip = driver.find_elements_by_xpath(
                "//body/div[@id='myxiaoxi']/div/div/div[@class='modal-header']/button")
            if cancel_tip[0]:
                cancel_tip[0].click()
                sleep(2)

            #登录成功后获取答题次数
            opportunity = driver.find_element_by_class_name('l_jihui')
            #剩余答题次数为0，不进行后续操作
            if '0' == opportunity.text[2]:
                driver.quit()
                return None

            driver.find_element_by_id("lbuts").click()
            sleep(3)
            log.success_log('username', username)



            return driver

        #登录错误次数超过三次，可认为登录错误归因于用户名密码错误
        driver.quit()
        log.error_log(username, 'error username/password!')
        return None