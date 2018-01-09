from selenium import webdriver
from time import sleep
import doQuiz
import auto_login

'''
driver = webdriver.Chrome()
driver.get('http://xxjs.dtdjzx.gov.cn/')
driver.find_element_by_class_name('lcors').click()

sleep(2)

doQuiz.do_practice(driver)

sleep(10)
'''

#auto_login.turing_test_with_external_force('https://sso.dtdjzx.gov.cn/sso/validateCodeServlet?t=5.920458341211418')
user_info = auto_login.get_user_info_from_txt()
for i in user_info:
	print (i[0], ' ' , i[1])