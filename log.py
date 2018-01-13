error_log_file = 'error_record.txt'
success_log_file = 'success_record.txt'


def error_log(username, reason):
	with open(error_log_file, 'a', encoding='UTF-8') as file:
		file.write(username+'  login error  '+reason)
		file.write('\n')
		file.close()

def success_log(username, score):
	with open(success_log_file, 'a', encoding='UTF-8') as file:
		file.write(username+'  has finish the test, score :  '+score)
		file.write('\n')
		file.close()