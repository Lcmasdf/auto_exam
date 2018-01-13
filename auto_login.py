import urllib
import sys
import http.cookiejar
import hashlib
from selenium import webdriver
from PIL import Image
import requests
import xml.etree.ElementTree as ET
import re

import Parse_Code
import Parse_form
import easy_read

from time import sleep

url_login = 'https://sso.dtdjzx.gov.cn/sso/login'
url_code = 'https://sso.dtdjzx.gov.cn/sso/validateCodeServlet?t=1.713432'

class MyException(Exception):
	def __init__(self,message):
		Exception.__init__(self)
		self.message=message 

def login(user):
	error_login_cnt = 0
	while (error_login_cnt < 3) : 
		username = user[0]
		password = user[1]

		cj = http.cookiejar.CookieJar()

		processor = urllib.request.HTTPCookieProcessor(cj)
		opener = urllib.request.build_opener(processor)
		code = Parse_Code.turing_test_with_external_force(url_code, opener)
		code = str(code)
		html = opener.open(url_login).read()
		data = Parse_form.parse_form(html)
		data['username'] = username
		print(username)
		data['password'] = password
		print(password)
		data['validateCode'] = code.upper()
		encode_data = urllib.parse.urlencode(data).encode('utf8')
		print(encode_data)
		request = urllib.request.Request(url_login, data=encode_data)
		response = opener.open(request)
		if ('https://www.dtdjzx.gov.cn/member/' == response.geturl()):
			print(data['username'],'  login success!')
			for item in cj:
				print (item.name, item.value)
			return cj
		else:
			error_login_cnt += 1
	raise MyException(user[0] + '  login error')

def calc_md5(file):
	import hashlib
	md5_value = hashlib.md5()
	with open(file,'rb') as f:
		while True:
			data = f.read(2048)
			if not data:
				break
			md5_value.update(data)

	return md5_value.hexdigest()

def record_pos_2_local(pos,local_path='local_file'):
	data = easy_read.read_from_utf8(local_path)
	lines = data.split('\n')
	md5 = lines[0]

	with open(local_path, 'w', encoding='UTF-8') as file:
		file.write(md5)
		file.write('\n')
		file.write(str(pos))
		file.close()

def get_user_info_from_txt(path=None,local_path='local_file'):
	user_info = []

	if None == path:
		user_name_path = 'user_name.txt'
	else :
		user_name_path = path


	'''
	with open(local_path,'rt',encoding='UTF-8') as file:
		last_md5 = re.sub('\n', '', file.readline())
		last_pos = re.sub('\n', '', file.readline())
		file.close()
	'''
	#获取上次答题时的md5校验码以及答题位置
	data = easy_read.read_from_utf8(local_path)
	if None == data:
		last_pos = -1
		last_md5 = 0
	else:
		lines = data.split('\n')
		last_md5 = lines[0]
		if (len(lines) == 2):
			last_pos = lines[1]
		else:
			last_pos = -1

	#计算本次答题的md5校验码
	new_md5 = calc_md5(user_name_path)

	if last_md5 != new_md5:
		last_pos = -1
		print('file change, do from the start!')

	with open(local_path,'w') as file:
		file.write(new_md5)
		file.close()


	data = easy_read.read_from_utf8(user_name_path)
	lines = data.split('\n')
	for line in lines:
		user_info.append([line, 'Aa'+line])

	if '' == last_pos:
		last_pos = -1
	print(last_pos)
	return user_info, int(last_pos)

def login_with_chrome(username, password):
	err_login_cnt = 0

	driver = webdriver.Chrome()
	driver.get('http://xxjs.dtdjzx.gov.cn/')
	sleep(3)
	driver.find_element_by_id('lbuts').click()
	sleep(3)
	shenfen = driver.find_element_by_id('shenfen')
	shenfen.find_element_by_xpath("//option[@value='0']").click()
	btn_confirm = driver.find_element_by_id('bts')
	btn_confirm.click()
	
	while err_login_cnt < 3:
		driver.find_element_by_id("username").send_keys(username)
		print(username)
		driver.find_element_by_id("password").send_keys(password)
		print(password)
		driver.save_screenshot('val.png')
		val_code = Parse_Code.turing_test_with_external_force_screec_short()
		driver.find_element_by_id("validateCode").send_keys(val_code)
		sleep(1)
		driver.find_element_by_class_name('js-submit').click()
		sleep(5)
		if ('https://sso.dtdjzx.gov.cn/sso/login?error' == driver.current_url) :
			err_login_cnt += 1
			continue

		left_opportunity = driver.find_element_by_class_name('l_jihui')
		#print(left_opportunity.text[2])
		print(left_opportunity.text)
		if ('0' == left_opportunity.text[2]):
			driver.quit()
			return None

		driver.find_element_by_id("lbuts").click()
		sleep(3)
		return driver
	driver.quit()
	return None