# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить
# данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import datetime
from pymongo import MongoClient

def extract_number_of_mails(str):
    for word in str.split():
        try:
            number = int(word)
        except ValueError:
            pass
    return number

def date_extract(date_to_process):
    now = datetime.date.today()
    month = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
             'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря', ]
    date = date_to_process.split()
    try:
        a = int(date[0])
    except:
        if date[0] == 'Сегодня,':
            date[0] = f"{str(now.day)} {month[now.month-1]} "
        elif date[0] == 'Вчера,':
            date[0] = f"{str(now.day-1)} {month[now.month-1]} "
    finally:
        pass
    date.remove(date[len(date) - 1])
    date = ' '.join(date)[:-1]
    print(date)
    return(date)

client = MongoClient()
db = client['letters']
db.letters.drop
letters = db.letters


driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://account.mail.ru/login')
driver.implicitly_wait(7)
elem = driver.find_element(By.XPATH, "//div[@id='login-content']//input[@name='username']")     #//div[@class='login-row username']//input[@name='username']")
driver.implicitly_wait(1)
elem.send_keys('study.ai_172@mail.ru')
driver.implicitly_wait(1)
elem = driver.find_element(By.XPATH, "//div[@id='login-content']//button[@data-test-id='next-button']")
driver.implicitly_wait(1)
elem.send_keys(Keys.ENTER)
driver.implicitly_wait(2)
elem = driver.find_element(By.XPATH, "//div[@class='login-row password']//input[@name='password']")
driver.implicitly_wait(1)
elem.send_keys('NextPassword172#')
driver.implicitly_wait(1)
elem = driver.find_element(By.XPATH, "//div[@id='login-content']//button[@data-test-id='submit-button']")
driver.implicitly_wait(1)
elem.send_keys(Keys.ENTER)
driver.implicitly_wait(20)
links = []
number_of_emails = driver.find_element(By.XPATH, "//a[@href='/inbox/']").get_attribute('title')
number_of_emails = extract_number_of_mails(number_of_emails)
while len(links) <= number_of_emails:
# while len(links) <= 20: # для тестирования
    mails = driver.find_elements(By.XPATH, "//a[contains(@href, '/inbox/0')]")
    for mail in mails:
        link = mail.get_attribute('href')
        if not link in links:
            links.append(link)
    actions = ActionChains(driver)
    actions.move_to_element(mails[-1])
    actions.perform()
    sleep(1)
pprint(len(links))

for link in links:
    driver.get(link)
    from_who = driver.find_element(By.XPATH,
                                   "//div[@class='letter__author']//span[@class='letter-contact']").get_attribute("title")
    date = date_extract(
        driver.find_element(By.XPATH, "//div[@class='letter__date']").text
    )
    letter_theme = driver.find_element(By.XPATH, "//h2[@class='thread__subject']").text
    letter_text = driver.find_element(By.XPATH, "//div[@class='letter__body']").text
    letters_data = {}
    letters_data['from_who'] = from_who
    letters_data['date'] = date
    letters_data['letter_theme'] = letter_theme
    letters_data['letter_text'] = letter_text
    letters.insert_one(letters_data)

for letter in letters.find({}):
    pprint(letter)







