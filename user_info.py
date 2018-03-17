import easy_read
import threading
import log

#TODO : 如何将user_info实现为线程安全
class user_info:

    #初始化user_info
    def __init__(self, user_info_file_path='user_name.txt',
                 login_record_file_path='local_file'):
        self.user_info_file_path = user_info_file_path
        self.login_record_file_path = login_record_file_path
        self.user_info = []
        self.pos = -1  #当前答题的位置
        self.md5 = 0  #当前答题时user_info文件的md5值
        self.mutex = threading.Lock()
        self.__init_user_info()

    def __init_user_info(self):
        #从文件读取
        data = easy_read.read_from_utf8(self.login_record_file_path)
        if data is None:
            last_pos = -1
            last_md5 = 0
        else:
            #local_file文件格式：第一行记录文件md5值，第二行记录上次答题最后答题用户的位置
            lines = data.split('\n')
            last_md5 = lines[0]
            if len(lines) == 2:
                last_pos = int(lines[1])
            else:
                last_pos = -1

        #计算当前user_info文件的md5值
        new_md5 = self.calc_md5(self.user_info_file_path)
        self.md5 = new_md5

        #新旧user_info不同，为了保证将所有用户都答题，讲user_info中的用户全部重新答
        if last_md5 != new_md5:
            self.pos = -1
            log.success_log('new','')
            log.error_log('','new')
        else:
            self.pos = last_pos

        data = easy_read.read_from_utf8(self.user_info_file_path)
        lines = data.split('\n')
        for line in lines:

            #跳过空行
            if len(line) == 0:
                continue

            username, password = line.split(' ')
            self.user_info.append([username, password])

    #提供一个多线程安全的获取未答题用户的方法
    def get_next_user(self):
        self.mutex.acquire()

        #判断是否已到最后
        if self.pos+1 == len(self.user_info):
            return None,None

        self.pos += 1
        username, password = self.user_info[self.pos]

        self.record_pos_2_local()

        self.mutex.release()

        return username, password

    #计算记录用户名密码文件的md5，用于判断是否发生改变
    def calc_md5(self, file):
        import hashlib
        md5_value = hashlib.md5()
        with open(file, 'rb') as f:
            while True:
                data = f.read(2048)
                if not data:
                    break
                md5_value.update(data)

        return md5_value.hexdigest()
        pass

    #记录最后一个答题用户的用户名密码在文件中的位置，用于断答继续
    def record_pos_2_local(self):
        with open(self.login_record_file_path, 'w') as file:
            file.write(str(self.md5))
            file.write('\n')
            file.write(str(self.pos))
            file.close()