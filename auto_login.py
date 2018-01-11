import urllib
import sys
import http.cookiejar
import hashlib
from PIL import Image
import requests
import xml.etree.ElementTree as ET
import Parse_Code
import Parse_form
from selenium import webdriver
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
		data['password'] = password
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

def get_user_info_from_txt(path=None):
	user_info = []
	
	if None == path:
		file_path = 'user_name.txt'
	else :
		file_path = path

	with open(file_path,'rt') as file:
		for line in file:
			user_info.append([line[0:-1], 'Aa'+line[0:-1]])

	return user_info

def login_with_chrome(username, password):
	driver = webdriver.Chrome()
	driver.get('http://xxjs.dtdjzx.gov.cn/')
	sleep(3)
	driver.find_element_by_id('lbuts').click()
	sleep(3)
	shenfen = driver.find_element_by_id('shenfen')
	shenfen.find_element_by_xpath("//option[@value='0']").click()
	btn_confirm = driver.find_element_by_id('bts')
	btn_confirm.click()
	driver.find_element_by_id("username").send_keys(username)
	driver.find_element_by_id("password").send_keys(password)
	driver.save_screenshot('val.png')
	val_code = Parse_Code.turing_test_with_external_force_screec_short()
	driver.find_element_by_id("validateCode").send_keys(val_code)
	sleep(1)
	driver.find_element_by_class_name('js-submit').click()
	sleep(3)
	if ('https://sso.dtdjzx.gov.cn/sso/login?error' == driver.current_url) :
		return driver
	driver.find_element_by_id("lbuts").click()
	sleep(3)
	return driver

