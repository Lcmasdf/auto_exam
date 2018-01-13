import hashlib
import urllib

from PIL import Image
from datetime import *
import requests
import xml.etree.ElementTree as ET
from PIL import Image
from selenium import webdriver
import configparser
import codecs

def get_val_img_pos_from_ini():
	config = configparser.ConfigParser()
	config.readfp(codecs.open('config.ini','r','utf-8-sig'))
	topleft_x = config.get('img', 'topleft_x')
	topleft_y = config.get('img', 'topleft_y')
	bottomright_x = config.get('img', 'bottomright_x')
	bottomright_y = config.get('img', 'bottomright_y')
	print(type(topleft_x))
	return int(topleft_x), int(topleft_y), int(bottomright_x), int(bottomright_y)


def turing_test_with_external_force(val_url, opener):
	html = opener.open(val_url).read()

	val_code = opener.open(val_url).read()

	val_file = open('val.jpeg', 'wb')
	val_file.write(val_code)
	val_file.close()
	url = 'http://api.ruokuai.com/create.xml'
	paramDict = {}
	paramDict['username'] = 'lcmasdf'
	paramDict['password'] = 'lcm123456'
	paramDict['typeid'] = 3040
	paramDict['timeout'] = 90
	paramDict['softid'] = 1
	paramDict['softkey'] = 'b40ffbee5c1cf4e38028c197eb2fc751'
	paramKeys = ['username',
				 'password',
				 'typeid',
				 'timeout',
				 'softid',
				 'softkey']
	imagePath = 'val.jpeg'
	img = Image.open(imagePath)
	if img is None:
		print ('get file error')

	img.save('upload.gif', format='gif')
	filebytes = open('upload.gif', 'rb').read()

	timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	boundary = '------------' + hashlib.md5(timestr.encode('utf8')).hexdigest().lower()
	boundarystr = '\r\n--%s\r\n' % (boundary)

	bs = b''
	for key in paramKeys:
		bs = bs + boundarystr.encode('ascii')
		param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s" % (key, paramDict[key])
		bs = bs + param.encode('utf8')
	bs = bs + boundarystr.encode('ascii')

	header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n' % (
		'sample')
	bs = bs + header.encode('utf8')

	bs = bs + filebytes
	tailer = '\r\n--%s--\r\n' % (boundary)
	bs = bs + tailer.encode('ascii')

	headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
			   'Connection': 'Keep-Alive',
			   'Expect': '100-continue',
			   }
	response = requests.post(url, params='', data=bs, headers=headers)
	print(response.text)

	# parse xml
	tree = ET.fromstring(response.text)
	return tree[0].text

def turing_test_with_external_force_screec_short():
	topleft_x, topleft_y, bottomright_x, bottomright_y = get_val_img_pos_from_ini()
	print(topleft_x, topleft_y, bottomright_x, bottomright_y)
	with Image.open('val.png') as img:
		img_val = img.crop((topleft_x,topleft_y,bottomright_x,bottomright_y))
		img_val.save('val.jpeg')

	url = 'http://api.ruokuai.com/create.xml'
	paramDict = {}
	paramDict['username'] = 'lcmasdf'
	paramDict['password'] = 'lcm123456'
	paramDict['typeid'] = 3040
	paramDict['timeout'] = 90
	paramDict['softid'] = 1
	paramDict['softkey'] = 'b40ffbee5c1cf4e38028c197eb2fc751'
	paramKeys = ['username',
				 'password',
				 'typeid',
				 'timeout',
				 'softid',
				 'softkey']
	imagePath = 'val.jpeg'
	img = Image.open(imagePath)
	if img is None:
		print ('get file error')

	img.save('upload.gif', format='gif')
	filebytes = open('upload.gif', 'rb').read()

	timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	boundary = '------------' + hashlib.md5(timestr.encode('utf8')).hexdigest().lower()
	boundarystr = '\r\n--%s\r\n' % (boundary)

	bs = b''
	for key in paramKeys:
		bs = bs + boundarystr.encode('ascii')
		param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s" % (key, paramDict[key])
		bs = bs + param.encode('utf8')
	bs = bs + boundarystr.encode('ascii')

	header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n' % (
		'sample')
	bs = bs + header.encode('utf8')

	bs = bs + filebytes
	tailer = '\r\n--%s--\r\n' % (boundary)
	bs = bs + tailer.encode('ascii')

	headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
			   'Connection': 'Keep-Alive',
			   'Expect': '100-continue',
			   }
	response = requests.post(url, params='', data=bs, headers=headers)
	print(response.text)

	# parse xml
	tree = ET.fromstring(response.text)
	return tree[0].text