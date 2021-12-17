import csv
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

complete_start = datetime.datetime.now()

header = ['riis on geniaaln', 'CPU Name', 'Cores', 'Price', 'CPU Mark', 'CPU Value', 'Thread Mark', 'Thread Value', 'TDP (W)',
          'Power Perf.', 'Test Date', 'Socket', 'Category']

data = []

options = Options()
driver_path = r"C:\Users\markr\PycharmProjects\eduardi_cpu_data\chromedriver.exe"

driver = webdriver.Chrome(driver_path, options=options)
driver.get("https://www.cpubenchmark.net/CPU_mega_page.html")

input("Press enter to continue... ")
print("Continuing...")
odd_cpu_nums = driver.find_elements(By.CLASS_NAME, "odd")
elem_num = 1
for element in odd_cpu_nums:
    time_start = datetime.datetime.now()
    print(elem_num, end=" > ")
    data_elem = []
    subelements = element.find_elements(By.TAG_NAME, "td")
    for elem in subelements:
        data_elem.append(elem.text)

    data.append(data_elem)
    time_delta = datetime.datetime.now() - time_start
    print(f"{time_delta}")
    elem_num += 1

print("Finished with odd numbers.")
print("Starting skimming even numbers.")

even_cpu_nums = driver.find_elements(By.CLASS_NAME, "even")
for element in odd_cpu_nums:
    time_start = datetime.datetime.now()
    print(elem_num, end=" > ")
    data_elem = []
    subelements = element.find_elements(By.TAG_NAME, "td")
    for elem in subelements:
        data_elem.append(elem.text)

    data.append(data_elem)
    time_delta = datetime.datetime.now() - time_start
    print(f"{time_delta}")
    elem_num += 1

print("Finished with even numbers.")

driver.close()

with open('cpu_data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)

print("Sucessfully wrote data to 'cpu_data.csv'.")
print(f"Ended program. Time: {datetime.datetime.now() - complete_start}")
