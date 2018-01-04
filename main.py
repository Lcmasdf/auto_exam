from selenium import webdriver
from time import sleep
import doQuiz
driver = webdriver.Chrome()
driver.get('http://xxjs.dtdjzx.gov.cn/')
driver.find_element_by_class_name('lcors').click()

sleep(2)

doQuiz.do_practice(driver)

sleep(10)