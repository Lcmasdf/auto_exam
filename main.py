import auto_login
import time
import exception_handle

if __name__ == "__main__":
	user_list = auto_login.get_user_info_from_txt()

	for user in user_list:
		try:
			opener = auto_login.login(user)
		except auto_login.MyException as e:
			exception_handle.fail_login_record(e.message)
			print(e.message)

		# post score

		#log out

		time.sleep(3)