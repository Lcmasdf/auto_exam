import re
from time import sleep

def init_prob_set(path):
	prob_set = {}
	with open('prob_set','r') as file:
		for i in range(200):
			prob = ''
			ans = []
			option = []
			for j in range(6):
				line = file.readline()
				if 0 == j :
					index = line.find('】')
					if (-1 != index):
						prob = line[index+1:-1]
						prob = re.sub('[、，《》（）。？：“”]', '', prob)
				elif 5 == j:
					index = line.find(':')
					if -1 != index:
						ans = line[index+2:-1].split(',')
				else:
					index = line.find('、')
					if -1 != index:
						option.append(re.sub('[、，《》（）。？：“”]', '', line[index+1:-1]))
			prob_set[prob]=[option,ans]
	return prob_set

def get_ans(prob, path='prob_set.dump'):
	#if False == prob_set_init:
	prob_set = init_prob_set(path)
	#	prob_set_init = True
	#	print('prob_set initialized!')
	if (prob_set.find(prob[0]))

	option_and_ans = prob_set.get(prob[0])

	if None == option_and_ans:
		return ['C']

	#print(option_and_ans)

	ans = []
	for item in option_and_ans[1]:
		option_desc = option_and_ans[0][ord(item)-ord('A')]
		for i in range(4):
			if (prob[1][i] == option_desc):
				ans.append(chr(i+ord('A')))
	return ans

def do_practice(driver, num_ques=20):
	#get next btn
	sleep(5)
	next_prob = driver.find_element_by_class_name('w_btn_tab_down')
	for i in range(num_ques):
		questions = driver.find_elements_by_xpath(
			"//body/div[@class='l_box']/div/div[@class='w_loads']/div/div[@class='W_ti W_mt22']/ul/li")
		print (questions[i].text)
		radio_checker = driver.find_elements_by_name("%s%s" % ('ra_', i))

		#items = questions[i].text.split('\n')
		items = questions[i].text.split('\n')
		index = items[0].find('题')
		question = re.sub('[、，《》（）。？：“”]', '', items[0][index + 1:])
		print (question)
		answerA = re.sub('[、，《》（）。？：“”]', '', items[1][2:])
		answerB = re.sub('[、，《》（）。？：“”]', '', items[2][2:])
		answerC = re.sub('[、，《》（）。？：“”]', '', items[3][2:])
		answerD = re.sub('[、，《》（）。？：“”]', '', items[4][2:])
		prob = [question, [answerA, answerB, answerC, answerD]]
		print(prob)
		ans = get_ans(prob)

		for item in ans:
			radio_checker[ord(item) - ord('A')].click()

		sleep(3)
		if i != 19:
			next_prob.click()
		sleep(3)

    # #get submit btn
	submit_btn = driver.find_element_by_class_name('W_fr')
	submit_btn.click()
	sleep(3)
	confirm_btn = driver.find_element_by_class_name('btn-danger')
	confirm_btn.click()
	sleep(3)
