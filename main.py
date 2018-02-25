# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep
import auto_login
import time
import do_quiz
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

if __name__ == 'file_test':
	user_list, last_pos = auto_login.get_user_info_from_txt(path='utf8.txt')

	for pos in range(last_pos+1, len(user_list)):
		print(user_list[pos][0], ' ', user_list[pos][1])

	prob_set = do_quiz.init_prob_set('123')
	print(prob_set)

	'''
	user_list = auto_login.get_user_info_from_txt()

	for user in user_list:
		try:
			cj = auto_login.login(user)
			cookie_dict = {}
			for item in cj:
				cookie_dict[item.name] = item.value

			print(cookie_dict)

			driver = webdriver.Chrome()
			#driver.add_cookie(cookie_dict)
			driver.get('http://xxjs.dtdjzx.gov.cn/')
			cookie = driver.get_cookies()
			print (cookie)
			sleep(10)
		except auto_login.MyException as e:
			exception_handle.fail_login_record(e.message)
			print(e.message)

		# post score

		#log out

		time.sleep(3)
	'''


if __name__ == 'test':
	easy_exam = auto_exam.auto_exam()

	easy_exam.set_ans_property(20, 100)

	easy_exam.do_practice()

