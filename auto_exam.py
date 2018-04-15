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
    prob_desc = []

    def __init__(self, bank_file_path='prob_set', total_question=200, option_num=4):
        self.file_path = bank_file_path
        self.total_question = total_question
        self.option_num = option_num

    #去除题目中标点符号，避免字符集不同产生问题
    @staticmethod
    def unpunctuate(line):
        return re.sub('[、，《》。？：“”]', '', line)

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

            #将题目内容补全，用于模糊查找
            prob_desc_list = list(prob)
            npos = prob_desc_list.index('（')
            ans_str = ''.join(ans)
            if -1 != ans_str.find('D'):
                prob_desc_list.insert(npos+1, option[3])
            if -1 != ans_str.find('C'):
                prob_desc_list.insert(npos+1, option[2])
            if -1 != ans_str.find('B'):
                prob_desc_list.insert(npos+1, option[1])
            if -1 != ans_str.find('A'):
                prob_desc_list.insert(npos+1, option[0])

            prob_desc_str = ''.join(prob_desc_list)
            self.prob_desc.append(prob_desc_str)

            self.prob_set[prob] = [option, ans]

    #根据题目找到答案
    #若找不到该题目，则返回E
    @staticmethod
    def get_answer(question):
        options_answers = question_bank.prob_set.get(question[0])
        if None == options_answers:
            return ['E']

        ans = ['E']
        for item in options_answers[1]:
            print(item)
            option_desc = options_answers[0][ord(item) - ord('A')]
            for i in range(4):
                if question[1+i] == option_desc:
                    ans.append(chr(i + ord('A')))
        return ans

    #通过模糊查找匹配答案
    #若找不到该题目，则返回E
    #为了能够确定括号的位置，同时又不增加新参数，在处理题目时没有处理括号
    #在模糊匹配时需要将题目中括号去掉（因为两个括号位置不同，会造成匹配失败）
    #总的来说，模糊匹配的计算开销很大，只能够作为一种补充答题方法
    @staticmethod
    def get_ans_fuzzy(question):
        #构建正则查找字符串
        prob = question[0]
        opt = question[1:]
        regular_str = '(.*)'
        npos =  prob.find('（')
        prob_str_list = list(re.sub('[（）]', '',prob))
        prob_str_list.insert(npos, regular_str)
        prob_str_all = ''.join(prob_str_list)

        ret = []
        for item in question_bank.prob_desc:
            item = re.sub('[（）]', '', item)
            match_obj = re.match(prob_str_all, item)

            if match_obj:
                match_str = match_obj.group(1)
                if -1 != match_str.find(opt[0]):
                    ret.append('A')
                if -1 != match_str.find(opt[1]):
                    ret.append('B')
                if -1 != match_str.find(opt[2]):
                    ret.append('C')
                if -1 != match_str.find(opt[3]):
                    ret.append('D')

                if len(ret) == 0:
                    ret.append('C')

                return ret

        return ['E']

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
            #首先在原题库中寻找答案，如找不到则使用模糊查找，两者都找不到返回'E'
            # “我要的并不在这里，你给的答案没意义，都选C，都选C~”
            #                                        --大鹏
            if 'E' == ans[0]:
                ans = self.question_bank.get_ans_fuzzy(prob)
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
        sleep(2)

        '''
        share = driver.find_element_by_class_name('W_share">')
        if share:
            share.click()
            sleep(2)
            wechat = driver.find_element_by_class_name('jiathis_button_weixin" ')
            if wechat:
                wechat.click()
                sleep(2)
        '''