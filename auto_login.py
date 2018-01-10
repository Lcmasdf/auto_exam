import urllib
import sys
import http.cookiejar
import hashlib
from PIL import Image
import requests
import xml.etree.ElementTree as ET
import Parse_Code
import Parse_form

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

		processor = urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
		opener = urllib.request.build_opener(processor)
		code = Parse_Code.turing_test_with_external_force(url_code, opener)
		code = str(code)
		html = opener.open(url_login).read()
		data = Parse_form.parse_form(html)
		data['username'] = username
		data['password'] = password
		data['validateCode'] = code.upper()
		encode_data = urllib.parse.urlencode(data).encode('utf8')
		#print(encode_data)
		request = urllib.request.Request(url_login, data=encode_data)
		response = opener.open(request)
		if ('https://www.dtdjzx.gov.cn/member/' == response.geturl()):
			print(data['username'],'  login success!')
			return opener
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