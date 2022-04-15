import selenium
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

stuudium_url = 'https://nrg.ope.ee/auth/'
webdriver_path = './chromedriver'
options = Options()
options.headless = True

driver_download = ChromeDriverManager().install()

class Homework:
    def __init__(self, name: str, date: str, desc: str) -> None:
        self.name = name
        self.date = date
        self.desc = desc

class Message:
    def __init__(self, name: str, date: str, author:str, desc: str) -> None:
        self.name = name
        self.date = date
        self.author = author
        self.desc = desc

class Grade:
    def __init__(self, name: str, grade: str) -> None:
        self.name = name
        self.grade = grade

def stuudium_return_homework_data(stuudium_username: str, stuudium_password: str, homework_filter=None) -> list:
        driver_homework = webdriver.Chrome(driver_download, options=options)
        driver_homework.get(stuudium_url)
        driver_homework.maximize_window()
        driver_homework.find_element(By.CLASS_NAME, "username").send_keys(stuudium_username)
        driver_homework.find_element(By.CLASS_NAME, "password").send_keys(stuudium_password)
        driver_homework.find_element(By.CLASS_NAME, "button").send_keys(selenium.webdriver.common.keys.Keys.ENTER)
        only_today = False
        only_all = False
        time.sleep(1)

        if homework_filter is None or homework_filter == "next_day":
            print("Filtering only tomorrow")
            todo_elements = driver_homework.find_elements(By.XPATH, "//*[contains(@class, \"todo_container\")]")
        elif homework_filter == "today":
            print("Filtering only today")
            only_today = True
            todo_elements = driver_homework.find_elements(By.XPATH, "//*[contains(@class, \"todo_container\")]")
        elif homework_filter == "all":
            print("Filtering only all")
            only_all = True
            todo_elements = driver_homework.find_elements(By.XPATH, "//*[contains(@class, \"todo_container\")]")

        try:
            # driver_hw.find_element_by_class_name("show-future").click()
            driver_homework.find_element(By.XPATH, "//*[contains(@class, \"show-future\")]").click()
        except:
            pass

        returned_homework = []
        for element in todo_elements:
            elem = element.find_element(By.CLASS_NAME, "todo")

            subject_date = element.get_attribute("data-date").replace(str(datetime.datetime.now().year), '')
            subject_date = subject_date.replace(str((datetime.datetime.now() + datetime.timedelta(days=365)).year), '')

            should_continue = False
            if homework_filter is None or only_today:
                today_day = str((datetime.date.today()).day)
                today_month = str((datetime.date.today()).month)
                tomorrow_day = str((datetime.date.today() + datetime.timedelta(days=1)).day)
                tomorrow_month = str((datetime.date.today() + datetime.timedelta(days=1)).month)

                if len(today_day) < 2:
                    today_day = "0" + today_day
                if len(today_month) < 2:
                    today_month = "0" + today_month
                if len(tomorrow_day) < 2:
                    tomorrow_day = "0" + tomorrow_day
                if len(tomorrow_month) < 2:
                    tomorrow_month = "0" + tomorrow_month

                if homework_filter is None and subject_date[:2] == tomorrow_month and subject_date[2:] == tomorrow_day:
                    should_continue = True
                elif only_today and int(subject_date[:2]) == today_month and int(subject_date[2:]) == int(today_day):
                    should_continue = True
            elif only_all:
                should_continue = True

            if should_continue:
                subject_name = elem.find_element(By.CLASS_NAME, "subject_name").text

                try:
                    subject_description = elem.find_element(By.CLASS_NAME, "todo_content").text
                except:
                    subject_description = " "
                if "Kontrolltöö" in elem.text:
                    subject_description = f"[KT] {subject_description}"
                returned_homework.append(
                    Homework(
                        name=subject_name, 
                        date=f"{subject_date[:2]}.{subject_date[2:]}", 
                        desc=subject_description
                        ),
                )
        driver_homework.close()
        return returned_homework

def stuudium_return_message_data(stuudium_username: str, stuudium_password: str, state: str, max_fields) -> list:
        driver = webdriver.Chrome(driver_download, options=options)
        final = []
        driver.get(f"{stuudium_url}/?return=%2Fopen-inbox%3Fapp-return%3D%252F")
        driver.find_element(By.CLASS_NAME, "username").send_keys(stuudium_username)
        driver.find_element(By.CLASS_NAME, "password").send_keys(stuudium_password)
        driver.find_element(By.CLASS_NAME, "button").send_keys(selenium.webdriver.common.keys.Keys.ENTER)

        time.sleep(1)
        messages = driver.execute_script("return document.getElementsByClassName('post-in-list')")

        if state == "only-unread":
            messages = driver.execute_script("return document.getElementsByClassName('post-in-list post-is-unread')")

        driver.execute_script("document.querySelectorAll('[data-suhtlus-action=post-list-load-older]')[0].click()")

        elem_counter = 0

        for message in messages:
            if elem_counter < max_fields:
                author = message.find_element(By.CLASS_NAME, "post-author").text
                date = message.find_element(By.CLASS_NAME, "post-date").text
                title = message.find_element(By.CLASS_NAME, "post-title").text
                short_description = message.find_element(By.CLASS_NAME, "post-body-preview").text
                href = message.find_element(By.CLASS_NAME, "post-in-list-expander").get_attribute("href")
                if date.split(" ") != ['']:
                    date_1 = date.split(" ")[0]
                    date_2 = date.split(" ")[1]
                    date = f"{date_1}{date_2}"

                    if short_description == '':
                        short_description = "No description provided."

                    final.append(
                        Message(
                            name=title,
                            date=date,
                            author=author,
                            desc = f"{short_description} \n Link: {href}"
                        )
                    )
                    elem_counter += 1
            return final

def stuudium_return_grade_data(stuudium_username: str, stuudium_password: str, max_fields=3) -> list:
        driver = webdriver.Chrome(driver_download, options=options)
        final = []
        driver.get(stuudium_url)
        driver.find_element(By.CLASS_NAME, "username").send_keys(stuudium_username)
        driver.find_element(By.CLASS_NAME, "password").send_keys(stuudium_password)
        driver.find_element(By.CLASS_NAME, "button").send_keys(selenium.webdriver.common.keys.Keys.ENTER)

        time.sleep(3)
        driver.execute_script("document.getElementsByClassName('new_button grey')[0].click()")

        cur_grades = 1

        time.sleep(1)

        try:
            driver.find_element(By.CLASS_NAME, "daily-summaries-navigate").click()
        except:
            pass

        grades = driver.find_elements(By.CLASS_NAME, "stream-entry")
        for element in grades:
            try:
                if cur_grades > max_fields:
                    break

                name = element.find_element(By.CLASS_NAME, "stream-entry-context").text
                grade = element.find_element(By.CLASS_NAME, "stream-entry-primary")

                if not "Ühiselamu" in name and "Hinne" in grade.text:
                    desc = grade.find_element(By.CLASS_NAME, "grade-current").text
                    final.append(
                        Grade(name=name, grade=desc)
                    )
                    cur_grades += 1
            finally:
                pass

        return final
