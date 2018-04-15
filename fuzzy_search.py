import auto_exam
import easy_read
import re

data = easy_read.read_from_utf8('prob_set')


prob_test = '我们将继续坚持以经济建设为中心致力于建设改革发展成果真正惠及人民()生态文明全面发展的小康社会'
test_opt_a = '经济'
test_opt_b = '政治'
test_opt_c = '文化'
test_opt_d = '社会'
test_ans = ['A','B','C','D']

prob_all = []

data_list = data.split('\n')
total_question = int(len(data_list)/6)
for prob_index in range(total_question):
    prob = ''

    prob_desc = data_list[prob_index * 6]
    index = prob_desc.find('】')
    if -1 != index:
        prob_desc = prob_desc[index + 1:]
    opt_a = data_list[prob_index * 6 + 1]
    opt_b = data_list[prob_index * 6 + 2]
    opt_c = data_list[prob_index * 6 + 3]
    opt_d = data_list[prob_index * 6 + 4]
    ans = data_list[prob_index * 6 + 5]

    prob_desc_list = list(prob_desc)
    npos = prob_desc_list.index('（')
    print(prob_index)

    index = opt_a.find('、')
    opt_a = opt_a[index+1:]
    opt_b = opt_b[index + 1:]
    opt_c = opt_c[index + 1:]
    opt_d = opt_d[index + 1:]

    if -1 != ans.find('A'):
        prob_desc_list.insert(npos+1, opt_a)
    if -1 != ans.find('B'):
        prob_desc_list.insert(npos+1, opt_b)
    if -1 != ans.find('C'):
        prob_desc_list.insert(npos+1, opt_c)
    if -1 != ans.find('D'):
        prob_desc_list.insert(npos+1, opt_d)

    prob_str = ''.join(prob_desc_list)
    prob_str = auto_exam.question_bank.unpunctuate(prob_str)

    prob_all.append(prob_str)

index_left = prob_test.find('(')
index_right = prob_test.find(')')
prob_test_list = list(prob_test)
npos = prob_test_list.index('(')
desc_left = prob_test_list[:npos]
desc_right = prob_test_list[npos+2:]
regular_match = '(.*)'
prob_regular = ''.join(desc_left+list(regular_match)+desc_right)


tttt = '我们将继续坚持以经济建设为中心致力于建设改革发展成果真正惠及人民经济政治文化社会生态文明全面发展的小康社会'

ttt = '我们将继续坚持以经济建设为中心致力于建设改革发展成果真正惠及人民(.*)生态文明全面发展的小康社会'

match_obj = re.match(ttt,tttt)


for line in prob_all:
    match_obj = re.match(prob_regular, line)

    if match_obj:
        print(match_obj.group(), match_obj.group(1))



    '''
    for prob_desc_index in range(6):
        index = prob_index*6 + prob_desc_index
        line = data_list[index]
        if 0 == prob_desc_index:
            index = line.find('】')
            if -1 != index:
                prob = line[index+1:]
                prob = self.unpunctuate(prob)
        elif 5 == prob_desc_index:
            index = line.find(':')
            if -1 != index:
                #二月份题目答案没有用'，'隔开
                ans = line[index+2:].split(',')
                #ans = list(line[index+1:])
        else:
            index = line.find('、')
            if -1 != index:
                option.append(question_bank.unpunctuate(line[index+1:]))
    self.prob_set[prob] = [option, ans]
    '''