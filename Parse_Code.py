import hashlib
import urllib

from PIL import Image
from datetime import *
import requests
import xml.etree.ElementTree as ET


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

	# parse xml
	tree = ET.fromstring(response.text)
	return tree[0].text