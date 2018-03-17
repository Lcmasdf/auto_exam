# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep
import auto_login
import time
import re
import http.cookiejar
import log

import auto_exam


#import thread

#__name__ = 'test'

if __name__ == "__main__":
    easy_exam = auto_exam.auto_exam()

    easy_exam.set_ans_property(20, 100)

    easy_exam.do_quiz()

    print('所有用户都已完成答题')

if __name__ == 'test':
    easy_exam = auto_exam.auto_exam()

    easy_exam.set_ans_property(20, 100)

    easy_exam.do_practice()

