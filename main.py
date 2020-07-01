from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import tkinter as tk
from tkinter import *
import tkinter.messagebox
import time


def send_message():
    username_text = str(user_entry.get())
    password_text = str(pass_entry.get())

    people = str(recipients_box.get(0.0, 'end'))
    message = str(message_box.get(0.0, 'end'))

    # Check if a text field was left empty
    text_fields = [username_text, password_text, people, message]

    if '' in text_fields:
        tk.messagebox.showinfo('Messenger Bot', 'ERROR: You left a text field blank')
        return

    # Get a list of recipients
    people = people.split(',')
    people = [name.strip('\n') for name in people]

    # Open browser and login
    browser = webdriver.Chrome('/Users/georgiamartinez/Downloads/chromedriver')
    browser.get('https://www.messenger.com/t/')

    username = browser.find_element_by_id('email')
    password = browser.find_element_by_id('pass')
    login = browser.find_element_by_id('loginbutton')

    username.send_keys(username_text)
    password.send_keys(password_text)
    login.click()

    try:
        browser.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/h1')
    except NoSuchElementException:
        tk.messagebox.showinfo('Messenger Bot', 'ERROR: Failed to login')
        browser.quit()
        return

    # Send the message to each person
    found = []
    not_found = []

    for x in range(len(people)):
        # Find the person
        search_bar = browser.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[1]/span[1]/label/input')
        search_bar.send_keys(people[x])

        time.sleep(1)
        current_chat = browser.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[1]/span[1]/div/div/div['
            '2]/ul/li/a/div/div[2]/div/div')
        name = current_chat.text

        # Check if the person was found
        if people[x] == name:
            found.append(name)
            current_chat.click()

            print(name)

            # Send the message
            text_box = browser.find_element_by_css_selector('.notranslate')
            text_box.send_keys(message)

            text_box.send_keys(Keys.RETURN)
        else:
            not_found.append(people[x])

    if not not_found:
        tk.messagebox.showinfo('Messenger Bot', 'The message was sent successfully.')
    else:
        tk.messagebox.showinfo('Messenger Bot', f'ERROR: Not sent to {not_found}')

    browser.quit()


# Setting up GUI
size = 700
root = tk.Tk()
root.resizable(False, False)

root.title('Messenger Bot')
canvas = tk.Canvas(root, height=size, width=size)
canvas.pack()

# Login info
frame = tk.Frame(root)
frame.place(relx=.5, rely=.1, width=300, height=60, anchor='n')

user_label = tk.Label(frame, text='Username:')
user_label.grid(row=0, column=0)

user_entry = tk.Entry(frame)
user_entry.grid(row=0, column=1)

pass_label = tk.Label(frame, text='Password:')
pass_label.grid(row=1, column=0)

pass_entry = tk.Entry(frame)
pass_entry.config(show='*')
pass_entry.grid(row=1, column=1)

# Message info
lower_frame = tk.Frame(root)
lower_frame.place(relx=.5, rely=.3, relwidth=.75, relheight=.6, anchor='n')

recipients_label = tk.Label(lower_frame, text='Recipients (separated by commas):')
recipients_label.pack(anchor='nw')

recipients_box = Text(lower_frame, width=100, height=10, highlightbackground='#e8e8e8', font='arial')
recipients_box.pack()

message_label = tk.Label(lower_frame, text='Type your message:')
message_label.pack(anchor='nw')

message_box = Text(lower_frame, width=100, height=10, highlightbackground='#e8e8e8', font='arial')
message_box.pack()

button = tk.Button(lower_frame, text='Send Message', command=send_message)
button.place(relx=.5, rely=.9, width=120, height=30, anchor='center')

root.mainloop()
