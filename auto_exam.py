import codecs
import re
from selenium import webdriver
from time import sleep
import random


import auto_login
import user_info
import easy_read
import log

#初始化题库，根据题目得到答案
class question_bank:
    prob_set = {}

    def __init__(self, bank_file_path='prob_set', total_question=200, option_num=4):
        self.file_path = bank_file_path
        self.total_question = total_question
        self.option_num = option_num

    #去除题目中标点符号，避免字符集不同产生问题
    @staticmethod
    def unpunctuate(line):
        return re.sub('[、，《》（）。？：“”]', '', line)

    def question_bank_init(self):
        data = easy_read.read_from_utf8(self.file_path)

        data_list = data.split('\n')
        self.total_question = int(len(data_list)/6)
        for prob_index in range(self.total_question):
            prob = ''
            ans = []
            option = []
            for prob_desc_index in range(6):
                index = prob_index*6 + prob_desc_index
                line = data_list[index]
                if 0 == prob_desc_index:
                    index = line.find('】')
                    if -1 != index:
                        prob = line[index+1:]
                        prob = self.unpunctuate(prob)
                elif 5 == prob_desc_index:
                    index = line.find(':')
                    if -1 != index:
                        #二月份题目答案没有用'，'隔开
                        ans = line[index+2:].split(',')
                        #ans = list(line[index+1:])
                else:
                    index = line.find('、')
                    if -1 != index:
                        option.append(question_bank.unpunctuate(line[index+1:]))
            self.prob_set[prob] = [option, ans]

    #根据题目找到答案
    #若找不到该题目，则返回E
    @staticmethod
    def get_answer(question):
        options_answers = question_bank.prob_set.get(question[0])
        if None == options_answers:
            return ['E']

        ans = []
        for item in options_answers[1]:
            print(item)
            option_desc = options_answers[0][ord(item) - ord('A')]
            for i in range(4):
                if question[1+i] == option_desc:
                    ans.append(chr(i + ord('A')))
        return ans

class auto_exam:

    def __init__(self):
        self.login = auto_login.auto_login()
        self.user = user_info.user_info()
        self.question_bank = question_bank()
        self.question_num = 0
        self.accuracy = 0

        self.login.load_configuration()
        pass

    def set_ans_property(self, question_num=20, accuracy=100):
        self.question_num = question_num
        self.accuracy = accuracy

    #答题主流程
    #1. 获取用户名密码
    #2. 登录
    #3. 答题
    def do_quiz(self, driver_type='Chrome'):
        #初始化题库
        self.question_bank.question_bank_init()

        while True:

            #获取用户名密码
            username, password = self.user.get_next_user()
            if username is None and password is None:
                break

            #根据driver_type创建对应的driver
            #目前在windows上只有Chrome可用，Ie待定
            #TODO ： 寻找一个好用的Ie版本，提高效率
            #DONE ： 答题页面不支持IE11
            driver = None
            if 'Chrome' == driver_type:
                driver = webdriver.Chrome()
            elif 'Firefox' == driver_type:
                pass
            elif 'Ie' == driver_type:
                pass

            #登录
            driver = self.login.login(username, password, driver)
            sleep(3)

            #答题
            self.__do_exam(driver)

            if None != driver:
                driver.close()

        pass

    #答测试题目
    #1. 跳转至答题页面
    #2. 答题
    def do_practice(self, driver_type='Chrome'):

        self.question_bank.question_bank_init()

        while True:
            #跳转至答题页面
            driver = None
            if 'Chrome' == driver_type:
                driver = webdriver.Chrome()
            elif 'Firefox' == driver_type:
                pass
            elif 'Ie' == driver_type:
                pass
            driver.get('http://xxjs.dtdjzx.gov.cn/')
            sleep(2)
            driver.find_element_by_class_name('lcors ').click()
            sleep(2)

            #答题
            self.__do_exam(driver)

            if None != driver:
                driver.close()

    #获取当前页面题目
    def __get_question(self, driver, index):
        questions = driver.find_elements_by_xpath(
            "//body/div[@class='l_box']/div/div[@class='w_loads']/div/div[@class='W_ti W_mt22']/ul/li")
            #"//body/div[@class='l_box']/div/div[@class='W_ti W_mt22']/ul/li")

        items = questions[index].text.split('\n')
        #TODO 为什么在网页获取的时候仍然要找到'题'的位置
        index = items[0].find('题')
        question = question_bank.unpunctuate(items[0][index+1:-1])
        answerA = question_bank.unpunctuate(items[1][2:])
        answerB = question_bank.unpunctuate(items[2][2:])
        answerC = question_bank.unpunctuate(items[3][2:])
        answerD = question_bank.unpunctuate(items[4][2:])

        return [question, answerA, answerB, answerC, answerD]


    #根据accuracy产生错误答案
    def __ans_dropout(self, ans):
        if random.randint(0,100) > self.accuracy:
            return ['C']
        else:
            return ans

    def __do_exam(self, driver):
        if None == driver:
            print('剩余答题次数为0')
            return

        error_cnt = 0
        #获取下一题按钮
        next_prob_btn = driver.find_element_by_class_name('w_btn_tab_down')
        for i in range(self.question_num):
            prob = self.__get_question(driver, i)
            ans = self.question_bank.get_answer(prob)
            #当找不到题目的答案时，get_answer返回E。
            # “我要的并不在这里，你给的答案没意义，都选C，都选C~”
            #                                        --大鹏
            if 'E' == ans[0]:
                error_cnt += 1
                ans[0] = 'C'
            ans = self.__ans_dropout(ans)

            radio_checker = driver.find_elements_by_name("%s%s" % ('ra_', i))
            for item in ans:
                radio_checker[ord(item) - ord('A')].click()

            sleep(1)
            if i != self.question_num -1:
                next_prob_btn.click()

            sleep(2)

        # get submit btn
        submit_btn = driver.find_element_by_class_name('W_fr')
        submit_btn.click()
        sleep(2)
        confirm_btn = driver.find_element_by_class_name('btn-danger')
        confirm_btn.click()
        log.success_log('score',str((20-error_cnt)*5))
        sleep(20)