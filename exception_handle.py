

def fail_login_record(username):
	with open('fail_login.txt', 'a+') as file:
		file.write(username)