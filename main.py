from selenium import webdriver
from time import sleep
import auto_login
import time
import exception_handle
import do_quiz
import re
import http.cookiejar

if __name__ == "__main__":
	user_list = auto_login.get_user_info_from_txt()
	for user in user_list:
		driver = auto_login.login_with_chrome(user[0], user[1])

		#do_quiz.do_practice(driver)

		driver.quit()

		sleep(1)





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
'''
	driver = webdriver.Chrome()
	driver.get('http://xxjs.dtdjzx.gov.cn/')
	driver.find_element_by_class_name('lcors ').click()

	next_prob = driver.find_element_by_class_name('w_btn_tab_down')

	for i in range(20):
		radio_checker = driver.find_elements_by_name("%s%s"%('ra_',i))
		questions = driver.find_elements_by_xpath("//body/div[@class='l_box']/div/div[@class='W_ti W_mt22']/ul/li")
		items = questions[i].text.split('\n')
		index = items[0].find('题')
		question = re.sub('[、，《》（）。？：“”]', '', items[0][index+1:])
		print (question)
		answerA = re.sub('[、，《》（）。？：“”]', '', items[1][2:])
		answerB = re.sub('[、，《》（）。？：“”]', '', items[2][2:])
		answerC = re.sub('[、，《》（）。？：“”]', '', items[3][2:])
		answerD = re.sub('[、，《》（）。？：“”]', '', items[4][2:])
		prob = [question,[answerA,answerB,answerC,answerD]]
		print(prob)
		ans = do_quiz.get_ans(prob)

		for item in ans:
			radio_checker[ord(item)-ord('A')].click()
   		
		sleep(1)
		if i != 19:
			next_prob.click()
			sleep(1)
	
	submit_btn = submit_btn = driver.find_element_by_class_name('jiaojuan')
	submit_btn.click()

	sleep(10)
'''
