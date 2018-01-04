from selenium import webdriver
from time import sleep

def do_practice(driver, num_ques=20):
	#get next btn
	next_prob = next_prob = driver.find_element_by_class_name('w_btn_tab_down')

	for i in range(20):
		radio_checker = driver.find_elements_by_name("%s%s"%('ra_',i))

		#get ans and trans to list of index
		ans_all = radio_checker[0].get_attribute('goright')
		ans_list = ans_all.split(',')

		#click 
		for ans_single in ans_list:
			radio_checker[ord(ans_single)-ord('A')].click() 

		sleep(1)
		if i != 19:
			next_prob.click()
		sleep(1)

	#get submit btn
	submit_btn = submit_btn = driver.find_element_by_class_name('jiaojuan')
	submit_btn.click()