error_log_file = 'error_record.txt'
success_log_file = 'success_record.txt'

def error_log(username, reason):
    if 'new' == reason:
        with open(error_log_file, 'w', encoding='UTF-8') as file:
            file.write('this is the error file!\n')
            return

    with open(error_log_file, 'a', encoding='UTF-8') as file:
        file.write(username+'  login error  '+reason)
        file.write('\n')
        file.close()

def success_log(type, content):
    if 'new' == type:
        with open(success_log_file, 'w', encoding='UTF-8') as file:
            file.write('this is the score list\n')
            return

    with open(success_log_file, 'a', encoding='UTF-8') as file:
        if 'username' == type:
            file.write(content+' has finish the test, score :  ')
        else:
            file.write(content+'\n')