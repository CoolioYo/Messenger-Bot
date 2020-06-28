from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Log in to messenger
username_text = input('Type in your username: ')
password_text = input('Type in your password: ')

browser = webdriver.Chrome('/Users/georgiamartinez/Downloads/chromedriver')
browser.get('https://www.messenger.com/t/')

username = browser.find_element_by_id('email')
password = browser.find_element_by_id('pass')
login = browser.find_element_by_id('loginbutton')

username.send_keys(username_text)
password.send_keys(password_text)
login.click()

chats = ['Georgia Martinez']

def send_message(text):
    for people in range(len(chats)):
        # Find the person
        search_bar = browser.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[1]/span[1]/label/input')
        search_bar.send_keys(chats[people])

        time.sleep(1)
        current_chat = browser.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[1]/span[1]/div/div/div[2]/ul/li/a/div/div[2]/div/div')
        current_chat.click()

        # Send the text
        text_box = browser.find_element_by_css_selector('.notranslate')
        print(text_box)
        text_box.send_keys(text)

        text_box.send_keys(Keys.RETURN)

    time.sleep(5)
    browser.quit()


# Message to be sent
text = 'Test - Sent from Georgia\'s bot'
send_message(text)

#schedule.every().day.at('06:03').do(send_message, text)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
