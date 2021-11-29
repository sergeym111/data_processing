# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить
# данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Chrome()
driver.get('https://account.mail.ru/login')
sleep(4)
elem = driver.find_element(By.XPATH, "//div[@id='login-content']//input[@name='username']")     #//div[@class='login-row username']//input[@name='username']")
sleep(1)
elem.send_keys('study.ai_172@mail.ru')
sleep(1)
elem = driver.find_element(By.XPATH, "//div[@id='login-content']//button[@data-test-id='next-button']")
sleep(1)
elem.send_keys(Keys.ENTER)
sleep(1)
elem = driver.find_element(By.XPATH, "//div[@class='login-row password']//input[@name='password']")
sleep(1)
elem.send_keys('NextPassword172#')
sleep(1)
elem = driver.find_element(By.XPATH, "//div[@id='login-content']//button[@data-test-id='submit-button']")
sleep(1)
elem.send_keys(Keys.ENTER)
